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

from app.api.models.base import StatusEmbed
from app.api.models.investor import (
    Investor,
    InvestorRdl,
    ApprovalEmbed
)
from app.api.models.investment import (
    Investment
)
from app.api.models.loan_request import LoanRequest

from app.api.lib.utils import backoff

from app.config.external.bank import MODANAKU
from app.config.worker import WORKER, RPC

from task.investment.rpc.modanaku import (
    payment_plan_pb2_grpc,
    payment_plan_pb2,
    plan_pb2_grpc,
    plan_pb2
)


class InvestmentTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        sentry.captureException(exc)
        super(InvestmentTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        sentry.captureException(exc)
        # end with
        super(InvestmentTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def create_payment_plan(self, loan_request_id):
        """ background task to create payment plan for modanaku """
        # fetch investment id
        loan_request = LoanRequest.find_one({"id": ObjectId(loan_request_id)})
        if loan_request is None:
            current_app.logger.info("{} loan request not \
                                    found".format(loan_request_id))
            celery.control.revoke(self.request.id)

        request = payment_plan_pb2.CreatePaymentPlanRequest()
        request.header.api_key = MODANAKU["API_KEY"]
        request.body.wallet_id = loan_request.modanaku.wallet_id
        request.body.destination = loan_request.bank_accounts[1].account_no
        plan = request.body.plans.add()
        plan.amount = str(loan_request.requested_loan_request)
        plan.due_date = str(loan_request.due_date)
        plan.type = "MAIN"

        try:
            # establish connection
            channel = grpc.insecure_channel(RPC["MODANAKU"])
            stub = payment_plan_pb2_grpc.PaymentPlanStub(channel)
            response = stub.CreatePaymentPlan(request)
        except grpc.RpcError as error:
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                # create entry on investment indicate
                current_app.logger.info("{} payment plan creation \
                                        failed".format(loan_request_id))
                # creation failed
                failed_rec = StatusEmbed(
                    status="PAYMENT_PLAN_FAILED",
                    message=error.details()
                )
                loan_request.list_of_status.append(failed_rec)
                loan_request.commit()
        else:
            current_app.logger.info(response)
            # create entry on investment indicate
            # creation success
            success_rec = StatusEmbed(
                status="PAYMENT_PLAN_CREATED",
            )
            loan_request.list_of_status.append(success_rec)
            loan_request.modanaku.bank_account_id = response.body.bank_account_id
            loan_request.modanaku.payment_plan_id = \
                response.body.payment_plan_id
            loan_request.commit()
