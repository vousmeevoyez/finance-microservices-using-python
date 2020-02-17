"""
    Investment Services
    _________________
    This is module to process business logic from routes and return API
    response
"""
from bson import ObjectId
from celery import chain
from string import Template

# models
from app.api.models.file import Article
from app.api.models.investment import Investment, InvestmentNotFound
from app.api.models.investor import Investor, InvestorNotFound
from app.api.models.wallet import Wallet
from app.api.models.loan_request import LoanRequest
from app.api.models.user import User

# task
from task.investment.tasks import InvestmentTask
from task.virtual_account.tasks import VirtualAccountTask
from task.transaction.tasks import TransactionTask
from task.utility.tasks import UtilityTask

# services
from app.api.batch.modules.services import schedule_transaction

# core
from app.api.lib.helper import send_notif
from app.api.lib.core.message import RESPONSE as error
from app.api.lib.core.exceptions import BaseError
from app.api.const import TRANSACTION_TYPE_TO_STATUS


class InvestmentServiceError(BaseError):
    """ raised when investment services error """


class InvestmentServices:
    def __init__(self, investment_id):
        investment = Investment.find_one({"id": ObjectId(investment_id)})
        if investment is None:
            raise InvestmentNotFound()

        investor = Investor.find_one({"id": investment.investor_id})
        escrow_wallet = Wallet.find_one({"label": "ESCROW"})
        self.user = User.find_one({"id": investor.user_id})
        self.investment = investment
        self.investor = investor
        self.escrow_wallet = escrow_wallet

    def _build_invest_payload(self):
        """ request payload for investing"""
        wallet = self.investor.get_wallet()
        # must return in following order -> investor wallet, investor id,
        # investor, investment id, investment, amount, transaction type
        transaction_type = "INVEST"
        transaction_payload = {
            "wallet_id": str(wallet["investor_wallet"]["_id"]),
            "source_id": str(self.investor.id),
            "source_type": "INVESTOR",
            "destination_id": str(self.investment.id),
            "destination_type": "INVESTMENT",
            "amount": -int(self.investment.total_amount),
            "transaction_type": "INVEST",
            "model": "Investment",
            "model_id": str(self.investment.id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] + "_REQUESTED",
        }
        return transaction_payload

    def _build_receive_invest_payload(self):
        """ request payload for when callabck received to increase escrow
        balance internally """
        transaction_type = "RECEIVE_INVEST"
        transaction_payload = {
            "wallet_id": str(self.escrow_wallet.id),
            "source_id": str(self.investor.id),
            "source_type": "INVESTOR",
            "destination_id": str(self.investment.id),
            "destination_type": "INVESTMENT",
            "amount": int(self.investment.total_amount),
            "transaction_type": "RECEIVE_INVEST",
            "model": "Investment",
            "model_id": str(self.investment.id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] + "_REQUESTED",
        }
        return transaction_payload

    def _build_disburse_payload(self, loan_request_id, amount):
        """ request payload for when callabck received to increase escrow
        balance internally """
        transaction_type = "DISBURSE"
        transaction_payload = {
            "wallet_id": str(self.escrow_wallet.id),
            "source_id": str(self.escrow_wallet.id),
            "source_type": "ESCROW",
            "destination_id": str(loan_request_id),
            "destination_type": "MODANAKU",
            "amount": -int(amount),
            "transaction_type": transaction_type,
            "model": "LoanRequest",
            "model_id": str(loan_request_id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] + "_REQUESTED",
        }

        return transaction_payload

    def _build_send_upfront_payload(self):
        """ request payload to transfer from escrow to modanaku """
        profit_wallet = Wallet.find_one({"label": "PROFIT"})

        loan_requests = self.investment.loan_requests

        total_profit = 0
        for loan_request in loan_requests:
            total_profit = total_profit + loan_request.total_fee

        transaction_type = "UPFRONT_FEE"
        debit_transaction = {
            "wallet_id": str(self.escrow_wallet.id),
            "source_id": str(self.escrow_wallet.id),
            "source_type": "ESCROW",
            "destination_id": str(profit_wallet.id),
            "destination_type": "PROFIT",
            "amount": -int(total_profit),
            "transaction_type": transaction_type,
            "model": "Investment",
            "model_id": str(self.investment.id),
            "status": TRANSACTION_TYPE_TO_STATUS[transaction_type] + "_REQUESTED",
        }

        return debit_transaction

    def prepare_investment(self):
        """ prepare investment """
        investment_va = {
            "model_name": "Investment",
            "model_id": str(self.investment.id),
            "va_type": "INVESTMENT",
            "label": "INVESTMENT"
        }
        # must be chained otherwise there's possibility when execute transfer
        # to investment va the va itself hasn't been created

        invest_payload = self._build_invest_payload()

        chain(
            # create investment va in background!
            VirtualAccountTask()
            .create_va.si(**investment_va)
            .set(queue="virtual_account"),
            # send money to investment va
            TransactionTask()
            .send_transaction.si(**invest_payload)
            .set(queue="transaction"),
            # map successful transaction into designated object
            TransactionTask().map_transaction.s().set(queue="transaction"),
        ).apply_async()

        return {"status": "PROCESSING_INVESTMENT", "investment": invest_payload}, 202

    def send_to_profit(self):
        """ wrapper function to wrap all background task to send and receive money to
        profit master """
        """ to reduce cost instead of sending it directly we put the
        transaction into batch and later it will be executed by the worker """
        upfront_fee_payload = self._build_send_upfront_payload()

        # schedule upfront fee to batch
        upfront_fee_payload["schedule_name"] = "UPFRONT_FEE"
        queue_id = schedule_transaction(**upfront_fee_payload)
        self.investment.list_of_status.append(
            {"status": "SEND_TO_PROFIT_QUEUED", "queue_id": queue_id}
        )
        self.investment.commit()
        return upfront_fee_payload

    def execute_disbursements(self):
        """ execute disbursments to all designated bank account asynchronous"""
        disbursements = []
        for loan_request in self.investment.loan_requests:
            # disburse loan
            disbursement = self._build_disburse_payload(
                loan_request.loan_request_id, loan_request.disburse_amount
            )
            disbursements.append(disbursement)
            TransactionTask().send_transaction.apply_async(
                kwargs=disbursement,
                queue="transaction",
                link=TransactionTask().map_transaction.s().set(queue="transaction"),
            )

            # update tnc
            loan_request = LoanRequest.find_one({"id": loan_request.loan_request_id})
            article = Article.find_one({"id": loan_request.tnc.file_id})
            # convert to template
            template = Template(article.content)
            # investor name
            investor_name = (
                self.investor.first_name
                + self.investor.middle_name
                + self.investor.last_name
            )
            parsed_template = template.substitute(PEMBERI_PINJAMAN=investor_name)
            article.content = parsed_template
            article.commit()
        return disbursements

    def increase_escrow_balance(self):
        receive_invest_payload = self._build_receive_invest_payload()
        TransactionTask().send_transaction.apply_async(
            kwargs=receive_invest_payload,
            queue="transaction",
            link=TransactionTask().map_transaction.s().set(queue="transaction"),
        )
        return receive_invest_payload

    def continue_investment(self):
        """ after we successfully receive callback to escrow we continue investment
        flow execution """
        # need to increase escrow balance
        receive_invest_payload = self.increase_escrow_balance()

        # need to disable investment va
        VirtualAccountTask().disable_va.apply_async(
            kwargs={
                "model_name": "Investment",
                "model_id": str(self.investment.id),
                "label": "INVESTMENT",
            },
            queue="virtual_account",
        )

        # send upfront and receive here
        upfront_fee = self.send_to_profit()

        disbursements = self.execute_disbursements()

        # send email to investor
        self.send_disburse_notif()

        return (
            {
                "status": "PROCESSING_DISBURSEMENT",
                "upfront_fee": upfront_fee,
                "receive_invest": receive_invest_payload,
                "disbursements": disbursements,
            },
            202,
        )

    def send_disburse_notif(self):
        email_notif, in_app_notif = send_notif(
            recipient=self.investor.email,
            user_id=self.investor.user_id,
            notif_type="INVESTOR_DISBURSE",
            platform="mobile",
            device_token=self.user.device_id,
        )
        return email_notif, in_app_notif
