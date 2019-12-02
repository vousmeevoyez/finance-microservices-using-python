import pytest

from app.api.callback.modules.services import (
    top_up_rdl,
    top_up_va,
    update_transaction
)
from app.api.models.wallet import Wallet
from app.api.lib.core.http_error import UnprocessableEntity


def test_top_up_rdl(setup_investor, setup_investor_wallet):
    investor_rdl_account_no = setup_investor.bank_accounts[0].account_no

    response = top_up_rdl(investor_rdl_account_no, 1000, "12345678910")
    assert response["status"] == "000"


def test_top_up_va_for_investment(setup_escrow_wallet, setup_investor,
                                  setup_investor_wallet, setup_investment):

    investment_account_no = setup_investment.bank_accounts[0].account_no

    response = top_up_va(investment_account_no, 1000, "12345678911",
                         "INVESTMENT")
    assert response["status"] == "000"


def test_top_up_va_for_repayment(setup_escrow_wallet,
                                 setup_investment_with_loan):
    # create loan request with bank account and map with a investment
    investment, loan_request = setup_investment_with_loan

    loan_account_no = loan_request.bank_accounts[0].account_no

    response = top_up_va(loan_account_no, 1000, "12345678911", "REPAYMENT")
    assert response["status"] == "000"


def test_update_transaction(setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction

    # we use transactions with invest
    response = update_transaction(
        str(transactions[0].id),
        transactions[0].transaction_type,
        "SUCCESS"
    )
    assert response["status"] == "SEND_TO_INVESTMENT_SUCCESS"
