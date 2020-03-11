from datetime import datetime
import pytest
from bson.json_util import dumps

from app.api.models.investor import (
    Investor,
    InvestorRdl,
    ApprovalEmbed,
    InvestorNotFound
)
from app.api.models.loan_request import LoanRequest
from app.api.models.investment import Investment


def test_create_investor(setup_investor):
    investor_count = Investor.count_documents()
    assert investor_count == 1


def test_create_investor_rdl(setup_investor_rdl, setup_investor):
    investor_count = InvestorRdl.count_documents()
    assert investor_count == 1


def test_approve_investor(setup_investor):
    investor = Investor.find_one({"id": setup_investor.id})
    # create onboarding approval
    onboarding_approval = ApprovalEmbed(
        status="ONBOARDING",
        user_id=setup_investor.user_id
    )

    investor.approvals.append(onboarding_approval)
    investor.commit()

    # create pending approval
    pending_approval = ApprovalEmbed(
        status="PENDING",
        user_id=setup_investor.user_id
    )

    investor.approvals.append(pending_approval)
    investor.commit()

    # create approved approval
    pending_approval = ApprovalEmbed(
        status="APPROVAL",
        user_id=setup_investor.user_id
    )

    investor.approvals.append(pending_approval)
    investor.commit()

    result = investor.dump()
    assert len(result["approvals"]) == 3


def test_get_investor_by_rdl(setup_investor):
    investor = Investor.get_investor_by_rdl(setup_investor.bank_accounts[0].account_no)
    assert investor["bank_accounts"][0]["account_no"] == \
        setup_investor.bank_accounts[0].account_no


def test_get_investor_by_rdl_not_found(setup_investor):
    with pytest.raises(InvestorNotFound):
        investor = Investor.get_investor_by_rdl("123123")


def test_get_investor_wallet(setup_investor, setup_investor_wallet):
    result = setup_investor.get_wallet()
    assert result["investor_wallet"]["_id"] == setup_investor_wallet.id


def test_look_up_va(setup_investment):
    result = Investment.get_by_va(setup_investment.bank_accounts[0].account_no)
    assert result


def test_investment_get_status_by_transaction(
    setup_investment_with_transaction
):
    investment, loan_request, transactions = setup_investment_with_transaction

    investment = Investment().get_by_transactions(
        transactions[0].id
    )
    assert investment[0]


def test_investment_get_by_loan_request(
    setup_investment_with_transaction
):
    investment, loan_request, transactions = setup_investment_with_transaction

    investment = Investment.get_by_loan_request(
        str(loan_request.id)
    )
    assert investment


def test_loan_request_get_status_by_transaction(
    setup_investment_with_transaction
):
    investment, loan_request, transactions = setup_investment_with_transaction

    loan_request = LoanRequest().get_by_transactions(
        transactions[3].id
    )
    assert loan_request[0]


def test_loan_request_with_product(
    setup_investment_with_transaction
):
    loan_requests = LoanRequest.get_with_product_info({"st": "DISBURSED"})
    assert loan_requests == []
