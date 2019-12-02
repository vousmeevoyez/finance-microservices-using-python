"""
    implementation for every specific internal callback
"""
import pytz
from datetime import datetime
from bson import ObjectId

from app.api.models.base import (
    StatusEmbed,
    TransactionStatusNotFound
)

from app.api.lib.helper import str_to_class, send_notif
from app.api.lib.core.http_error import RequestNotFound
from app.api.lib.core.message import RESPONSE
from app.api.const import TRANSACTION_TYPE_TO_STATUS

from app.api.models.transaction import Transaction

from task.transaction.tasks import TransactionTask
from task.virtual_account.tasks import VirtualAccountTask
from task.investment.tasks import InvestmentTask
from task.utility.tasks import UtilityTask


LOCAL_TIMEZONE = pytz.timezone("Asia/Jakarta")


class BaseCallback:

    __models__ = []

    def __init__(self):
        self.callback_info = None
        self.objects = []

    def set(self, callback_info):
        self.callback_info = callback_info

    def update(self):
        for item in self.__models__:
            try:
                model = str_to_class(item)
                _id = model().get_by_transaction(
                    self.callback_info.transaction_id
                )
            except TransactionStatusNotFound:
                raise RequestNotFound(
                    RESPONSE["TRANSACTION_STATUS_NOT_FOUND"]["TITLE"],
                    RESPONSE["TRANSACTION_STATUS_NOT_FOUND"]["MESSAGE"]
                )

            # begin mongo session here
            transaction_status = StatusEmbed(
                transaction_id=self.callback_info.transaction_id,
                status=self.callback_info.status
            )

            object_ = model.find_one({"id": _id})
            object_.list_of_status.append(transaction_status)
            object_.commit()
            # insert object into propery array
            self.objects.append(object_)

        self.post_update()

    def post_update(self):
        pass

class WithdrawCallback(BaseCallback):

    def update(self):
        pass

class InvestCallback(BaseCallback):
    __models__ = ["Investment"]


class ReceiveInvestCallback(BaseCallback):
    __models__ = ["Investment"]


class UpfrontFeeCallback(BaseCallback):
    __models__ = ["Investment"]

    def post_update(self):
        """ we only trigger increasing profit balance after upfront fee sended
        succcessfully """
        transaction = Transaction.find_one(
            {"id": ObjectId(self.callback_info.transaction_id)}
        )
        transaction_type = "RECEIVE_UPFRONT_FEE"

        wallet_model = str_to_class("Wallet")
        profit_wallet = wallet_model.find_one({"label": "PROFIT"})
        escrow_wallet = wallet_model.find_one({"label": "ESCROW"})
        investment = self.objects[0]

        credit_transaction = {
            "wallet_id": str(profit_wallet.id),
            "source_id": str(escrow_wallet.id),
            "source_type": "ESCROW",
            "destination_id": str(profit_wallet.id),
            "destination_type": "PROFIT",
            "amount": abs(transaction.amount),
            "transaction_type": transaction_type,
            "model": "Investment",
            "model_id": str(investment.id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] +
            "_REQUESTED"
        }

        TransactionTask().send_transaction.apply_async(
            kwargs=credit_transaction,
            queue="transaction",
            link=TransactionTask().map_transaction.s().set(queue="transaction")
        )


class ReceiveUpfrontFeeCallback(BaseCallback):
    __models__ = ["Investment"]


class DisburseCallback(BaseCallback):
    __models__ = ["LoanRequest"]

    def post_update(self):
        """ after we receive disburse was success we need to update the loan
        request into disburse !"""
        loan_request = self.objects[0]

        status = "PROCESSING"
        if self.callback_info.status == "SEND_TO_MODANAKU_COMPLETED":
            status = "DISBURSED"

            # create virtual account for repayment purpose
            # after that we set payment plan
            repayment_va = {
                "model_name": "LoanRequest",
                "model_id": str(loan_request.id),
                "va_type": "REPAYMENT",
                "custom_status": "REPAYMENT",
                "label": "REPAYMENT"
            }
            VirtualAccountTask().create_va.apply_async(
                kwargs=repayment_va,
                queue="virtual_account",
                link=InvestmentTask().create_payment_plan.si(
                    str(loan_request.id)
                ).set(queue="investment")
            )

            # send email to all borrower
            borrower_model = str_to_class("Borrower")
            borrower = borrower_model.find_one(
                {"id": loan_request.borrower_id}
            )
            user_model = str_to_class("User")
            user = user_model.find_one(
                {"id": borrower.user_id}
            )

            # send borrower notif through email and in app
            send_notif(
                recipient=borrower.email,
                user_id=borrower.user_id,
                notif_type="LOAN_REQUEST_DISBURSE",
                platform="mobile",
                custom_content={
                    "loan_request_code": loan_request.loan_request_code
                },
                device_token=user.device_id
            )

            loan_request.status = status
            loan_request.commit()


class InvestFeeCallback(BaseCallback):

    __models__ = ["LoanRequest"]

    """
        trigger callback after successfully invest a fee
        should trigger increasing escrow balance
    """

    def post_update(self):
        wallet_model = str_to_class("Wallet")
        escrow_wallet = wallet_model.find_one({"label": "ESCROW"})
        profit_wallet = wallet_model.find_one({"label": "PROFIT"})

        transaction_type = "RECEIVE_INVEST_FEE"
        transaction = Transaction.find_one(
            {"id": ObjectId(self.callback_info.transaction_id)}
        )

        send_invest_fee = {
            "wallet_id": str(profit_wallet.id),
            "source_id": str(profit_wallet.id),
            "source_type": "PROFIT",
            "destination_id": str(escrow_wallet.id),
            "destination_type": "ESCROW",
            "amount": transaction.amount,
            "transaction_type": transaction_type,
            "model": "LoanRequest",
            "model_id": str(self.objects[0].id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type]
        }

        TransactionTask().send_transaction.apply_async(
            kwargs=send_invest_fee,
            queue="transaction",
            link=TransactionTask().map_transaction.s().set(queue="transaction")
        )


class ReceiveInvestFeeCallback(BaseCallback):
    __models__ = ["LoanRequest"]
    """
        trigger callback after successfully receive a invest fee
        should trigger investor repayment
    """

    def post_update(self):
        wallet_model = str_to_class("Wallet")
        escrow_wallet = wallet_model.find_one({"label": "ESCROW"})

        # fetch object from properties
        loan_request = self.objects[0]
        # after we know which loan request we need to know which investment and
        # investor
        investment_model = str_to_class("Investment")
        investment_info = investment_model.get_by_loan_request(loan_request.id)
        investment = investment_model.find_one(
            {"id": ObjectId(investment_info["id"])}
        )
        # get investor
        investor_model = str_to_class("Investor")
        investor = investor_model.find_one({"id": investment.investor_id})
        #  we need to know how much investor repayment
        loan_request_fee = list(filter(
            lambda loan: loan.loan_request_id ==
            loan_request.id, investment.loan_requests
        ))

        repayment_amount = loan_request_fee[0].disburse_amount \
            + loan_request_fee[0].total_fee \
            + loan_request_fee[0].fees[0].investor_fee

        transaction_type = "INVEST_REPAYMENT"
        send_invest_fee = {
            "wallet_id": str(escrow_wallet.id),
            "source_id": str(escrow_wallet.id),
            "source_type": "ESCROW",
            "destination_id": str(investor.id),
            "destination_type": "INVESTOR_RDL_ACC",
            "amount": repayment_amount,
            "transaction_type": transaction_type,
            "model": "LoanRequest",
            "model_id": str(self.objects[0].id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type]
        }

        TransactionTask().send_transaction.apply_async(
            kwargs=send_invest_fee,
            queue="transaction",
            link=TransactionTask().map_transaction.s().set(queue="transaction")
        )

        # trigger email to borrower
        current_time = datetime.utcnow()
        current_local_time = LOCAL_TIMEZONE.localize(current_time)
        repayment_date = current_local_time.strftime("%Yi-%m-%d %H:%M")
        # get product name
        product_model = str_to_class("Product")
        product = product_model.find_one(
            {"_id": loan_request.product_id}
        )

        # send investor notif through email and in app
        send_notif(
            recipient=investor.email,
            user_id=investor.user_id,
            notif_type="INVESTOR_REPAYMENT",
            platform="web",
            custom_content={
                "repayment_date": repayment_date,
                "repayment_amount": loan_request.requested_loan_request,
                "product": product.product_name
            }
        )


class InvestRepaymentCallback(BaseCallback):
    __models__ = ["LoanRequest"]
    """
        trigger callback after successfully send invest
    """
