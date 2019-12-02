from unittest.mock import Mock
from app.api.models.investment import Investment
from app.api.models.loan_request import LoanRequest
from app.api.callback.factories.products import (
    InvestCallback,
    DisburseCallback
)


def test_invest_callback(setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction

    callback_info = Mock(
        transaction_id=transactions[0].id,
        status="SEND_TO_INVESTMENT_COMPLETED"
    )
    callback = InvestCallback()
    callback.set(callback_info)
    callback.update()

    invest = Investment.find_one({"_id": investment.id})
    assert any("SEND_TO_INVESTMENT_COMPLETED" in iv.status for iv in invest.list_of_status)


def test_disburse_callback(setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction

    callback_info = Mock(
        transaction_id=transactions[3].id,
        status="SEND_TO_MODANAKU_COMPLETED"
    )
    callback = DisburseCallback()
    callback.set(callback_info)
    callback.update()

    loan_request = LoanRequest.find_one(
        {"_id": loan_request.id}
    )
    assert loan_request.status == "DISBURSED"
    assert any("SEND_TO_MODANAKU_COMPLETED" in lr.status for lr in loan_request.list_of_status)
