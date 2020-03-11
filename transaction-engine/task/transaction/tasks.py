"""
    This is Celery Task that actually apply transaction
"""
import random
from bson import ObjectId
from bson.decimal128 import Decimal128

import pymongo
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

from celery.exceptions import MaxRetriesExceededError

from flask import current_app

from app.api.models.transaction import Transaction, PaymentEmbed
from app.api.models.wallet import Wallet

# const
from app.api.const import WORKER

from task.base import celery, fast_backoff, BaseTask


class InsufficientBalance(Exception):
    """ raised when insufficient balance """


class TransactionTask(BaseTask):
    """Abstract base class for all tasks in my app."""

    @celery.task(
        bind=True,
        max_retries=WORKER["TRANSACTION_MAX_RETRIES"],
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"]
    )
    def apply(self, transaction_id):
        """ background to really apply the transaction to completed and deduct
        balance """

        # begin mongo session here
        with current_app.connection.start_session(
            causal_consistency=True
        ) as session:
            with session.start_transaction(
                    read_concern=ReadConcern("majority"),
                    write_concern=WriteConcern("majority")
            ):
                try:
                    # start locking the transaction
                    transaction_lock = ObjectId()
                    transaction = Transaction.collection.find_one_and_update(
                        {"_id": ObjectId(transaction_id)},
                        {
                            "$set": {
                                "lock": transaction_lock
                            }
                        }
                    )

                    # deduct wallet balance based on how much the transactioin
                    wallet = Wallet.collection.find_one_and_update(
                        {"_id": transaction["wallet_id"]},
                        {
                            "$set": {
                                "lock": ObjectId(),
                            },
                            "$inc": {
                                "balance": transaction["amount"]
                            }
                        },
                        session=session
                    )

                    # finally apply balance based on current balance -
                    # transaction amount
                    after_balance = wallet["balance"].to_decimal() + \
                        transaction["amount"].to_decimal()
                    if after_balance < 0:
                        raise InsufficientBalance

                    Transaction.collection.find_one_and_update(
                        {"_id": ObjectId(transaction_id)},
                        {
                            "$set": {
                                "status": "APPLIED",
                                "balance": Decimal128(after_balance)
                            },
                            "$unset": {"lock": transaction_lock}
                        },
                        session=session
                    )

                    session.commit_transaction()

                except (
                        pymongo.errors.ConnectionFailure,
                        pymongo.errors.OperationFailure,
                        pymongo.errors.InvalidOperation,
                        InsufficientBalance
                ) as exc:
                    current_app.logger.info("retry.{}".format(transaction_id))
                    try:
                        self.retry(
                            exc=exc,
                            countdown=fast_backoff()
                        )
                    except MaxRetriesExceededError:
                        # if transaction still can be applied, we mark it as
                        # failed
                        Transaction.collection.find_one_and_update(
                            {"_id": ObjectId(transaction_id)},
                            {
                                "$set": {
                                    "status": "FAILED"
                                }
                            },
                            session=session
                        )
