import pytest

from app.api.loan_request.modules.services import LoanRequestServices
from app.api.models.loan_request import LoanRequest


def test_build_invest_payload(setup_investment_with_loan):
    investment, loan_request = setup_investment_with_loan

    result = LoanRequestServices(
        str(loan_request.id)
    )._build_receive_repayment_payload()
    assert result["wallet_id"]
    assert result["source_id"] == str(loan_request.id)
    assert result["source_type"] == "MODANAKU"
    assert result["destination_id"] == str(loan_request.id)
    assert result["destination_type"] == "REPAYMENT"
    assert result["amount"] == loan_request.requested_loan_request
    assert result["transaction_type"] == "RECEIVE_REPAYMENT"


def test_process_repayment(setup_investment_with_loan):
    investment, loan_request = setup_investment_with_loan

    response, status_code = LoanRequestServices(
        str(loan_request.id)
    ).process_repayment()
    assert response["status"] == "PROCESS_REPAYMENT"
    assert response["receive_repayment"]
    assert response["send_invest"]
    # make sure repayment its updated
    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.status == "PAID"
