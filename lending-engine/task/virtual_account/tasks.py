import grpc
from bson import ObjectId

from flask import current_app
from google.protobuf.json_format import Parse
from celery.exceptions import (
    MaxRetriesExceededError
)

from task.tasks import BaseTask

from app.api import (
    celery
)

from app.api.lib.helper import str_to_class
from app.api.lib.utils import backoff

from app.config.worker import WORKER, RPC

from task.virtual_account.rpc.bni_va import (
    virtual_account_pb2_grpc,
    virtual_account_pb2
)


class VirtualAccountTask(BaseTask):
    """Abstract base class for all tasks related to virtual account """

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def create_va(self, model_name=None, model_id=None,
                  custom_status=None, va_type="CREDIT", label=None):
        """ background task to create investment va """
        # fetch investment id
        model_ = str_to_class(model_name)
        object_ = model_.find_one({"id": ObjectId(model_id)})
        if object_ is None:
            current_app.logger.info("{} {} not \
                                    found".format(model_name, model_id))
            celery.control.revoke(self.request.id)

        request = virtual_account_pb2.CreateVaRequest()
        request.name = "{} for {}".format(model_name, model_id)
        request.va_type = va_type

        try:
            # establish connection
            channel = grpc.insecure_channel(RPC["BNI_VA"])
            stub = virtual_account_pb2_grpc.VirtualAccountStub(channel)
            response = stub.CreateVa(request)
        except grpc.RpcError as error:
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                current_app.logger.info("{} {} not \
                                        found".format(model_name, model_id))
                # create entry on investment indicate
                # creation failed
                status = str_to_class("StatusEmbed")
                model_name = model_name.upper()
                string_status = model_name + "_VA_FAILED"
                failed_rec = status(
                    status=string_status,
                    message=error.details()
                )
                object_.list_of_status.append(failed_rec)
                object_.commit()
        else:
            current_app.logger.info(response)
            # create bank account information on investment
            bank_model = str_to_class("Bank")
            bank = bank_model.find_one(
                {"bank_name": "PT BANK NEGARA INDONESIA 1946 (Persero) Tbk"}
            )
            bank_acc = str_to_class("BankAccEmbed")
            va = bank_acc(
                bank_id=bank.id,
                bank_name=bank.bank_name,
                account_no=response.account_no,
                account_name="{} Va for {}".format(model_name, str(model_id)),
                account_type="VIRTUAL_ACCOUNT",
                label=label
            )
            object_.bank_accounts.append(va)

            # create entry on investment indicate
            # creation success
            status = str_to_class("StatusEmbed")
            model_name = model_name.upper()

            string_status = model_name + "_VA_CREATED"
            if custom_status is not None:
                string_status = custom_status + "_VA_CREATED"

            success_rec = status(
                status=string_status,
            )
            object_.list_of_status.append(success_rec)
            object_.commit()
            return model_id

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def disable_va(self, model_name=None, model_id=None, label=None):
        """ background task to disable va """
        # fetch investment id
        model_ = str_to_class(model_name)
        object_ = model_.find_one({"id": ObjectId(model_id)})
        if object_ is None:
            current_app.logger.info("{} {} not \
                                    found".format(model_name, model_id))
            celery.control.revoke(self.request.id)

        request = virtual_account_pb2.DisableVaRequest()
        request.va_type = "CREDIT"

        account_no = object_.bank_accounts[0].account_no
        if label is not None:
            bank_accounts = list(filter(
                lambda bank: bank.label ==
                label, object_.bank_accounts
            ))
            account_no = bank_accounts[0].account_no

        request.account_no = account_no

        try:
            # establish connection
            channel = grpc.insecure_channel(RPC["BNI_VA"])
            stub = virtual_account_pb2_grpc.VirtualAccountStub(channel)
            response = stub.DisableVa(request)
        except grpc.RpcError as error:
            self.retry(countdown=backoff(self.request.retries))
        else:
            current_app.logger.info(response)
