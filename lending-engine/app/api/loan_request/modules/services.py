"""
    Loan Request Services
    _________________
    This is module to process business logic from routes and return API
    response
"""
import pytz
from datetime import datetime

from bson import ObjectId
from flask import current_app
# models
from app.api.models.investment import Investment
from app.api.models.borrower import Borrower
from app.api.models.loan_request import LoanRequest, LoanRequestNotFound
from app.api.models.product import Product
from app.api.models.wallet import Wallet
from app.api.models.user import User
# task
from task.transaction.tasks import TransactionTask
from task.virtual_account.tasks import VirtualAccountTask
from task.utility.tasks import UtilityTask
# core
from app.api.lib.helper import send_notif
from app.api.lib.core.exceptions import BaseError
from app.api.const import TRANSACTION_TYPE_TO_STATUS


LOCAL_TIMEZONE = pytz.timezone("Asia/Jakarta")


class LoanRequestServicesError(BaseError):
    """ raised when loan request services error """


class LoanRequestServices:

    def __init__(self, loan_request_id):
        loan_request = LoanRequest.find_one({"id": ObjectId(loan_request_id)})
        if loan_request is None:
            raise LoanRequestNotFound()
        if loan_request.status == "PAID":
            raise LoanRequestServicesError("Loan Already paid",
                                           "LOAN_ALREADY_PAID")
        # we link loan request to investment here
        invest_info = Investment.get_by_loan_request(loan_request.id)
        # convert it into investment object so it easier to deal
        investment = Investment.find_one({"id": ObjectId(invest_info["id"])})
        # fetch borrower info
        borrower = Borrower.find_one({"id": loan_request.borrower_id})
        user = User.find_one({"id": borrower.user_id})
        # fetch profit and escrow object
        profit_wallet = Wallet.find_one({"label": "PROFIT"})
        escrow_wallet = Wallet.find_one({"label": "ESCROW"})

        self.loan_request = loan_request
        self.investment = investment
        self.user = user
        self.borrower = borrower
        self.profit_wallet = profit_wallet
        self.escrow_wallet = escrow_wallet

    def _build_receive_repayment_payload(self):
        """ request payload for receiving repayment """
        transaction_type = "RECEIVE_REPAYMENT"
        transaction_payload = {
            "wallet_id": str(self.escrow_wallet.id),
            "source_id": str(self.loan_request.id),
            "source_type": "MODANAKU",
            "destination_id": str(self.loan_request.id),
            "destination_type": "REPAYMENT",
            "amount": int(self.loan_request.requested_loan_request),
            "transaction_type": transaction_type,
            "model": "LoanRequest",
            "model_id": str(self.loan_request.id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] +
            "_REQUESTED"
        }
        return transaction_payload

    def _build_invest_fee_payload(self):
        """ request payload for investing"""
        # must return in following order -> investor wallet, investor id,
        # investor, investment id, investment, amount, transaction type
        transaction_type = "INVEST_FEE"

        # we extract only loan request fee that we need
        loan_request_fee = list(filter(
            lambda loan_request: loan_request.loan_request_id ==
            self.loan_request.id, self.investment.loan_requests
        ))
        fee = loan_request_fee[0].fees[0].investor_fee

        send_invest_fee = {
            "wallet_id": str(self.profit_wallet.id),
            "source_id": str(self.profit_wallet.id),
            "source_type": "PROFIT",
            "destination_id": str(self.escrow_wallet.id),
            "destination_type": "ESCROW",
            "amount": -fee,
            "transaction_type": transaction_type,
            "model": "LoanRequest",
            "model_id": str(self.loan_request.id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] +
            "_REQUESTED"
        }

        return send_invest_fee

    def process_repayment(self):
        """ process repayment """
        # disable repayment virtual account
        VirtualAccountTask().disable_va.apply_async(
            kwargs={
                "model_name": "LoanRequest",
                "model_id": str(self.loan_request.id)
            },
            queue="virtual_account",
        )

        # update loan request as repaid
        self.loan_request.status = "PAID"
        self.loan_request.payment_date = datetime.utcnow()
        self.loan_request.commit()

        # trigger credit transaction to increase escrow balance
        receive_repayment_payload = self._build_receive_repayment_payload()
        TransactionTask().send_transaction.apply_async(
            kwargs=receive_repayment_payload,
            queue="transaction",
            link=TransactionTask().map_transaction.s().set(queue="transaction"),
        )

        # we dont have enough balance yet to repay investor
        # trigger send money from profit to escrow
        send_invest_payload = self._build_invest_fee_payload()
        TransactionTask().send_transaction.apply_async(
            kwargs=send_invest_payload,
            queue="transaction",
            link=TransactionTask().map_transaction.s().set(queue="transaction"),
        )

        # trigger email to borrower
        current_time = datetime.utcnow()
        current_local_time = LOCAL_TIMEZONE.localize(current_time)
        repayment_date = current_local_time.strftime("%Y-%m-%d %H:%M")
        # get product name
        product = Product.find_one(
            {"_id": self.loan_request.product_id}
        )
        # send repayment email to borrower
        send_notif(
            recipient=self.borrower.email,
            user_id=self.borrower.user_id,
            notif_type="LOAN_REQUEST_REPAYMENT",
            platform="mobile",
            custom_content={
                "repayment_date": repayment_date,
                "loan_request_code": self.loan_request.loan_request_code,
                "repayment_amount": self.loan_request.requested_loan_request,
                "product": product.product_name
            },
            device_token=self.user.device_id
        )

        # later after we receive callback that invest successfully sent we
        # increase the escrow balance
        # after escrow balance we have enough balance to repay investor

        return {
            "status": "PROCESS_REPAYMENT",
            "receive_repayment": receive_repayment_payload,
            "send_invest": send_invest_payload
        }, 202
