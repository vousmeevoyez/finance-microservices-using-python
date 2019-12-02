import json
import random

import grpc
from bson import ObjectId

from flask import current_app
from google.protobuf.json_format import Parse
from celery.exceptions import (
    MaxRetriesExceededError
)

from app.api import (
    celery,
    sentry
)

from app.api.models.base import (
    BankAccEmbed,
    StatusEmbed
)
from app.api.models.investor import (
    Investor,
    InvestorRdl,
    ApprovalEmbed
)
from app.api.models.investment import (
    Investment
)
from app.api.models.bank import Bank
from app.api.models.wallet import Wallet

from app.api.lib.helper import send_notif

from app.config.worker import WORKER, RPC
# RPC
from task.investor.rpc.email import (
    email_pb2_grpc,
    email_pb2
)
from task.investor.rpc.bni_rdl import (
    rdl_account_pb2_grpc,
    rdl_account_pb2
)


def backoff(attempts):
    """ prevent hammering service with thousand retry"""
    return random.uniform(2, 4) ** attempts


class InvestorTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        sentry.captureException(exc)
        super(InvestorTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        sentry.captureException(exc)
        # end with
        super(InvestorTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def create_rdl(self, investor_id):
        """ background task to create investor RDL """
        # fetch investor rdl data
        rdl_data = InvestorRdl.find_one({"investor_id": ObjectId(investor_id)})
        if rdl_data is None:
            current_app.logger.info("{} rdl data not found".format(investor_id))
            celery.control.revoke(self.request.id)

        # fetch investor
        investor = Investor.find_one({"id": ObjectId(investor_id)})
        if investor is None:
            current_app.logger.info("{} investor not found".format(investor_id))
            celery.control.revoke(self.request.id)

        result = list(filter(
            lambda approval: approval.status == 'PROCESSING', investor.approvals
        ))
        if len(result) == 0:
            # create onprocessing entry on investor
            processing_rec = ApprovalEmbed(
                status="PROCESSING",
                user_id=investor.user_id,
            )
            investor.approvals.append(processing_rec)
            investor.commit()
        # end if

        request = rdl_account_pb2.CreateRdlRequest()
        Parse(json.dumps(rdl_data.dump()), request, ignore_unknown_fields=True,)

        try:
            # establish connection
            channel = grpc.insecure_channel(RPC["BNI_RDL"])
            stub = rdl_account_pb2_grpc.RdlAccountStub(channel)
            response = stub.CreateRdl(request)
        except grpc.RpcError as error:
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                current_app.logger.info("{} rdl creation failed".format(investor_id))
                # create failed entry on investor
                failed_rec = ApprovalEmbed(
                    status="FAILED",
                    user_id=investor.user_id,
                    message=error.details()
                )
                investor.approvals.append(failed_rec)
                investor.commit()
        else:
            # create approval entry
            approved_rec = ApprovalEmbed(
                status="APPROVED",
                user_id=investor.user_id,
                approval_by=investor.approver_info.approver_id,
                reason_id=investor.approver_info.reason_id,
                message=investor.approver_info.message
            )
            investor.approvals.append(approved_rec)
            # create rdl account entry
            bank = Bank.find_one({"bank_name": "PT BANK NEGARA INDONESIA 1946 (Persero) Tbk"})
            bank_account = BankAccEmbed(
                bank_id=bank.id,
                bank_name=bank.bank_name,
                account_type="RDL_ACCOUNT",
                account_no=response.account_no,
                account_name=investor.first_name + " " + investor.last_name,
            )
            investor.bank_accounts.append(bank_account)
            investor.commit()
            # should trigger investor wallet creation
            wallet = Wallet(user_id=investor.user_id)
            wallet.commit()

            # for sending email purpose we return investor email
            send_notif(
                recipient=investor.email,
                user_id=investor.user_id,
                notif_type="INVESTOR_APPROVE",
                platform="web"
            )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def send_approval_email(self, recipient, product_type="MOPINJAM", email_type="INVESTOR_APPROVE"):
        """ background task to create investor approval email """
        # send email via gRPC
        request = email_pb2.SendEmailRequest()
        request.recipient = recipient
        request.product_type = "MOPINJAM"
        request.email_type = "INVESTOR_APPROVE"
        try:
            channel = grpc.insecure_channel(RPC["NOTIFICATION"])
            stub = email_pb2_grpc.EmailNotificationStub(channel)
            stub.SendEmail(request)
        except grpc.RpcError:
            self.retry(countdown=backoff(self.request.retries))
        return True
