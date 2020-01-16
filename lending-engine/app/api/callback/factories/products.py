"""
    implementation for every specific internal callback
"""
import pytz
from datetime import datetime
from bson import ObjectId
from flask import current_app

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


def get_investment_investor_loan_fee(loan_request):
    """ using loan request we get investment and loan fee information """
    investment_model = str_to_class("Investment")
    investment_info = investment_model.get_by_loan_request(
        loan_request.id
    )
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
    return investment, investor, loan_request_fee


class BaseSingleTrxCallback:
    """ using this base class when we receive a internal callback transaction
    it automatically update single record but multiple model that have transaction id either to
    completed or failed """
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

            # ADD  COMPLETED STATUS HERE
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


class BaseMultipleTrxCallback(BaseSingleTrxCallback):
    """ using this base class when we receive a internal callback bulk transaction
    it automatically update multiple record and possible multiple model that have transaction id either to
    completed or failed """

    def update(self):
        for item in self.__models__:
            try:
                model = str_to_class(item)
                _ids = model().get_by_transactions(
                    self.callback_info.transaction_id
                )
            except TransactionStatusNotFound:
                raise RequestNotFound(
                    RESPONSE["TRANSACTION_STATUS_NOT_FOUND"]["TITLE"],
                    RESPONSE["TRANSACTION_STATUS_NOT_FOUND"]["MESSAGE"]
                )
            # end try
            for _id in _ids:
                # ADD  COMPLETED STATUS HERE
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
            # end for
        # end for
        self.post_update()

    def post_update(self):
        pass


"""
    Investment Internal Callback Flow:
        1. Trigger Sending from rdl to investment va
        (SEND_TO_INVESTMENT_REQUESTED)
        2. after the transaction successfully completed we will get notified
        via InvestCallback (SEND_TO_INVESTMENT_COMPLETED)
        3. we will receive external callback from BNI and continue the
        investment
        4. trigger sending from escrow to n modanaku (disbursements)
        (SEND_TO_MODANAKU_REQUESTED)
        5. after the transaction successfully completed we will get notified
        via DisburseCallback (SEND_TO_MODANAKU_COMPLETED)
        6. trigger sending from escrow to profit (send upfront fee)
        (SEND_TO_PROFIT_REQUESTED)
        7. after the transaction successfully completed we will get notified
        via ReceiveUpfrontFeeCallback (SEND_TO_PROFIT_COMPLETED)
"""


class WithdrawCallback(BaseSingleTrxCallback):
    """ Handle what to do when we receive withdraw callback from transaction
    engine """
    def update(self):
        # currently we dont do anything!
        pass


class InvestCallback(BaseSingleTrxCallback):
    __models__ = ["Investment"]


class ReceiveInvestCallback(BaseSingleTrxCallback):
    __models__ = ["Investment"]


class UpfrontFeeCallback(BaseMultipleTrxCallback):
    __models__ = ["Investment"]

    def post_update(self):
        """ we update multiple investment that have same transaction
        id, but only trigger increasing profit balance once """
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


class ReceiveUpfrontFeeCallback(BaseSingleTrxCallback):
    __models__ = ["Investment"]


class DisburseCallback(BaseSingleTrxCallback):
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


"""
    Repayment Internal Callback Flow:
        1. Trigger Sending Invest fee from Profit to Escrow
        on process repayment
        (SEND_INVEST_FEE_REQUESTED)
        2. after the transaction successfully completed we will get notified
        via InvestFeeCallback (SEND_INVEST_FEE_COMPLETED)
        3. now we need to trigger increase profit balannce
        (RECEIVE_FEE_FROM_PROFIT_REQUESTED)
        4. after the transaction successfully completed we will get notified
        via ReceiveInvestFeeCallback (RECEIVE_FEE_FROM_PROFIT_COMPLETED)
        5. now we need to trigger sending bulk investor repayment
        (SEND_TO_RDL_REQUESTED)
        6. after the transaction successfully completed we will get notified
        via InvestRepaymentCallback (SEND_TO_RDL_COMPLETED)
"""


class InvestFeeCallback(BaseMultipleTrxCallback):

    __models__ = ["LoanRequest"]

    """
        trigger callback after successfully invest a fee
        should trigger increasing escrow balance
    """

    def post_update(self):
        wallet_model = str_to_class("Wallet")
        escrow_wallet = wallet_model.find_one({"label": "ESCROW"})
        profit_wallet = wallet_model.find_one({"label": "PROFIT"})

        # fetch object from properties
        loan_requests = self.objects

        # get transaction information
        transaction_type = "RECEIVE_INVEST_FEE"
        transaction = Transaction.find_one(
            {"id": ObjectId(self.callback_info.transaction_id)}
        )

        transactions = []
        update_records = []

        for loan_request in loan_requests:
            trx_payload = {
                "wallet_id": str(escrow_wallet.id),
                "source_id": str(profit_wallet.id),
                "source_type": "PROFIT",
                "destination_id": str(escrow_wallet.id),
                "destination_type": "ESCROW",
                "amount": abs(transaction.amount),
                "transaction_type": transaction_type,
            }

            update_payload = {
                "model": "LoanRequest",
                "model_id": str(loan_request.id),
                "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] +
                "_REQUESTED"
            }
            transactions.append(trx_payload)
            update_records.append(update_payload)
        # end for
        task_payload = {
            "transactions": transactions,
            "update_records": update_records  # rcrd that need t updates
        }

        TransactionTask().send_bulk_transaction.apply_async(
            kwargs=task_payload,
            queue="transaction",
            link=TransactionTask().map_bulk_transaction.s().set(queue="transaction")
        )


class ReceiveInvestFeeCallback(BaseMultipleTrxCallback):
    __models__ = ["LoanRequest"]
    """
        trigger callback after successfully receive a invest fee
        should trigger investor repayment
    """

    def post_update(self):
        wallet_model = str_to_class("Wallet")
        escrow_wallet = wallet_model.find_one({"label": "ESCROW"})

        # fetch object from properties
        loan_requests = self.objects
        # after we know which loan request we need to know which investment and
        # investor
        transactions = []
        update_records = []
        for loan_request in loan_requests:
            # get all required info (investment, investor, loan request fee )
            investment, investor, loan_request_fee = \
                get_investment_investor_loan_fee(loan_request)

            """
                we pick the last element of fees because potentially
                there are late fees
            """
            repayment_amount = loan_request_fee[0].disburse_amount \
                + loan_request_fee[0].total_fee \
                + loan_request_fee[0].fees[-1].investor_fee

            transaction_type = "INVEST_REPAYMENT"
            send_invest_fee = {
                "wallet_id": str(escrow_wallet.id),
                "source_id": str(escrow_wallet.id),
                "source_type": "ESCROW",
                "destination_id": str(investor.id),
                "destination_type": "INVESTOR_RDL_ACC",
                "amount": -repayment_amount,
                "transaction_type": transaction_type,
            }
            update_record = {
                "model": "LoanRequest",
                "model_id": str(loan_request.id),
                "status":
                TRANSACTION_TYPE_TO_STATUS[transaction_type]+"_REQUESTED"
            }
            # populate transaction to be bulked
            transactions.append(send_invest_fee)
            update_records.append(update_record)
        # end for

        task_payload = {
            "transactions": transactions,
            "update_records": update_records  # rcrd that need t updates
        }

        TransactionTask().send_bulk_transaction.apply_async(
            kwargs=task_payload,
            queue="transaction",
            link=TransactionTask().map_bulk_transaction.s().set(queue="transaction")
        )


class InvestRepaymentCallback(BaseSingleTrxCallback):
    __models__ = ["LoanRequest"]
    """
        trigger callback after successfully send invest
    """

    def post_update(self):
        # get loan request from class property
        loan_request = self.objects[0]

        # get all required info (investment, investor, loan request fee )
        investment, investor, loan_request_fee = \
            get_investment_investor_loan_fee(loan_request)

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
