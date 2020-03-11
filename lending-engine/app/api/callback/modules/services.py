"""
    Callback Services
    _________________
    This is module to process business logic from routes and return API
    response
"""
from bson import ObjectId
from flask import current_app

# model
from app.api.models.investor import Investor, InvestorNotFound
from app.api.models.wallet import Wallet
from app.api.models.investment import Investment, InvestmentNotFound
from app.api.models.loan_request import LoanRequest, LoanRequestNotFound

# factories
from app.api.callback.factories.factory import CallbackInfo, generate_internal_callback

from app.api.investment.modules.services import InvestmentServices
from app.api.loan_request.modules.services import (
    LoanRequestServices,
    LoanRequestServicesError,
)

from app.api.const import TRANSACTION_TYPE_TO_STATUS
from app.api.lib.core.http_error import UnprocessableEntity, RequestNotFound
from app.api.lib.helper import send_notif

from app.api.lib.core.message import RESPONSE as error
from task.transaction.tasks import TransactionTask


def top_up_rdl(rdl_account, amount, journal_no):
    """ trigger credit balance for rdl account """
    # first we need to get investor from his rdl account no
    try:
        investor = Investor.get_investor_by_rdl(rdl_account)
    except InvestorNotFound:
        raise RequestNotFound(
            error["INVESTOR_NOT_FOUND"]["TITLE"], error["INVESTOR_NOT_FOUND"]["MESSAGE"]
        )

    wallet = investor.get_wallet()

    # second we need to build the right payload to create transaction
    payload = {
        "wallet_id": str(wallet["investor_wallet"]["_id"]),
        "source_id": str(investor.id),
        "source_type": "INVESTOR_RDL_ACC",
        "destination_id": str(investor.id),
        "destination_type": "INVESTOR",
        "transaction_type": "TOP_UP_RDL",
        "amount": amount,
        "reference_no": journal_no,
    }

    TransactionTask().send_transaction.apply_async(kwargs=payload, queue="transaction")
    # send top up rdl notif
    send_notif(
        recipient=investor.email,
        user_id=investor.user_id,
        notif_type="INVESTOR_TOPUP",
        platform="web",
    )

    response = {"status": "000"}
    return response


def top_up_va(account_no, amount, payment_ntb, va_type):
    """ trigger credit balance for escrow via virtual account """
    # first we need to get escrow wallet
    escrow_wallet = Wallet.find_one({"label": "ESCROW"})
    if escrow_wallet is None:
        raise RequestNotFound(
            error["ESCROW_NOT_FOUND"]["TITLE"], error["ESCROW_NOT_FOUND"]["MESSAGE"]
        )

    # second we need to get investment based on virtual account
    if va_type == "INVESTMENT":
        try:
            investment = Investment.get_by_va(account_no)
        except InvestmentNotFound:
            raise RequestNotFound(
                error["INVESTMENT_NOT_FOUND"]["TITLE"],
                error["INVESTMENT_NOT_FOUND"]["MESSAGE"],
            )
        else:
            # continue investment flow!
            result = InvestmentServices(
                investment["id"], payment_ntb
            ).continue_investment()
            current_app.logger.info("Continue investment")
            current_app.logger.info(result)

    elif va_type == "REPAYMENT":
        try:
            loan_request = LoanRequest.get_by_va(account_no)
        except LoanRequestNotFound:
            raise RequestNotFound(
                error["LOAN_REQUEST_NOT_FOUND"]["TITLE"],
                error["LOAN_REQUEST_NOT_FOUND"]["MESSAGE"],
            )
        except LoanRequestServicesError as exc:
            raise UnprocessableEntity(exc.message, exc.original_exception)
        else:
            # continue investment flow!
            result = LoanRequestServices(
                loan_request["id"], payment_ntb
            ).process_repayment()
            current_app.logger.info("Receive repayment")
            current_app.logger.info(result)

    response = {"status": "000"}
    return response


def update_transaction(transaction_id, transaction_type, status):
    """ update transaction id to notify its already success or failed """
    modified_status = TRANSACTION_TYPE_TO_STATUS[transaction_type] + "_" + status
    # create callback contract
    callback_info = CallbackInfo(
        transaction_id=transaction_id,
        transaction_type=transaction_type,
        status=modified_status,
    )
    internal_callback = generate_internal_callback(callback_info)
    internal_callback.update()
    return {"status": modified_status}
