"""
    This is Celery Task to help interacting with External API
    in the background
"""
from bson import ObjectId
from pymongo.errors import ConnectionFailure, OperationFailure
import grpc

from flask import current_app
from celery.exceptions import MaxRetriesExceededError

from app.api.models.transaction import Transaction

from app.api.lib.helper import generate_ref_number
from app.config.worker import RPC
from app.api.const import WORKER

from task.base import celery, backoff, fast_backoff, BaseTask

from task.external.factories.helper import generate_stub, generate_message


class ExternalTask(BaseTask):
    """Abstract base class for all tasks in my app."""

    """
        Any External API Call via gRPC
    """

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def transfer(self, transaction_id):
        """ execute any external API Transfer """
        # look up transaction infromation
        transaction = Transaction.find_one({"_id": ObjectId(transaction_id)})

        # we should build payment payload for actual transfer
        source_bank_acc = transaction.payment.source
        destination_bank_acc = transaction.payment.destination
        provider = transaction.payment.provider
        bank_code = transaction.payment.bank_code
        # convert amount to positive
        amount = abs(int(transaction.amount))

        # REQUIRED to make sure transfer idempotence
        inquiry_ref_number = generate_ref_number(provider, destination_bank_acc)
        transfer_ref_number = generate_ref_number(
            provider, destination_bank_acc, amount
        )

        # generate gRPC message
        message = generate_message(provider)
        # generate gRPC stub
        stub = generate_stub(provider)

        message.source = source_bank_acc
        message.destination = destination_bank_acc
        message.bank_code = bank_code
        message.amount = amount
        message.inquiry_uuid = inquiry_ref_number
        message.transfer_uuid = transfer_ref_number

        try:
            # execute gRPC transfer
            result = stub.Transfer(message)
            # get reference number from transfer response
            response_uuid = result.response_uuid
        except grpc.RpcError:
            # should handle duplicate request!
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                status = "FAILED"
                return transaction_id, status, None, transfer_ref_number
        # clear cache
        generate_ref_number.cache_clear()
        status = "COMPLETED"
        # we return all this information so it can be applied by another celery
        # task
        return transaction_id, status, response_uuid, transfer_ref_number

    @celery.task(
        bind=True,
        max_retries=WORKER["TRANSACTION_MAX_RETRIES"],
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"]
    )
    def apply_external(self, transfer):
        """ mark successful transfer as completed or failed """
        transaction_id, status, reference_no, transfer_ref_number = transfer

        # start session!
        with current_app.connection.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                # retrying transaction until it succeed
                try:
                    # try fetch bank reference if available
                    Transaction.collection.update_one(
                        {"_id": ObjectId(transaction_id)},
                        {
                            "$set": {
                                "payment.request_reference_no":
                                transfer_ref_number,
                                "payment.reference_no": reference_no,
                                "payment.status": status,
                            }
                        },
                        session=session,
                    )
                    # commit everything here
                    session.commit_transaction()
                except (ConnectionFailure, OperationFailure) as exc:
                    current_app.logger.info(str(exc))
                    current_app.logger.info(
                        "retry {} commit \
                                            ".format(
                            transaction_id
                        )
                    )
                    self.retry(countdown=fast_backoff())
                else:
                    if status == "FAILED":
                        # if the transaction was failed we refund trigger
                        # refund here
                        from app.api.transactions.services import refund

                        result = refund(transaction_id=transaction_id)
                        current_app.logger.info("REFUND {}".format(result))
