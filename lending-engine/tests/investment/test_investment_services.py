import pytest

from app.api.investment.modules.services import InvestmentServices


def test_build_invest_payload(setup_investment, setup_investor_wallet):
    result = InvestmentServices(
        str(setup_investment.id)
    )._build_invest_payload()
    assert result["wallet_id"]
    assert result["source_id"] == str(setup_investment.investor_id)
    assert result["source_type"] == "INVESTOR"
    assert result["destination_id"] == str(setup_investment.id)
    assert result["destination_type"] == "INVESTMENT"
    assert result["amount"] == -setup_investment.total_amount
    assert result["transaction_type"] == "INVEST"


def test_build_receive_invest_payload(setup_investment):
    result = InvestmentServices(
        str(setup_investment.id)
    )._build_receive_invest_payload()
    assert result["wallet_id"]
    assert result["source_id"] == str(setup_investment.investor_id)
    assert result["source_type"] == "INVESTOR"
    assert result["destination_id"] == str(setup_investment.id)
    assert result["destination_type"] == "INVESTMENT"
    assert result["amount"] == setup_investment.total_amount
    assert result["transaction_type"] == "RECEIVE_INVEST"


def test_build_disburse_payload(setup_investment_with_loan):
    investment, loan_request = setup_investment_with_loan

    result = InvestmentServices(
        str(investment.id)
    )._build_disburse_payload(loan_request.id,
                              loan_request.disburse_amount)
    assert result["wallet_id"]
    assert result["source_id"]
    assert result["source_type"] == "ESCROW"
    assert result["destination_id"]
    assert result["destination_type"] == "MODANAKU"
    assert result["amount"] == -int(loan_request.disburse_amount)
    assert result["transaction_type"] == "DISBURSE"


def test_build_send_receive_upfront_payload(setup_investment_with_loan, setup_profit_wallet):
    investment, loan_request = setup_investment_with_loan
    debit = InvestmentServices(
        str(investment.id)
    )._build_send_upfront_payload()
    assert debit["wallet_id"]
    assert debit["source_id"]
    assert debit["source_type"] == "ESCROW"
    assert debit["destination_id"]
    assert debit["destination_type"] == "PROFIT"
    #assert debit["amount"] == -22500
    assert debit["amount"]
    assert debit["transaction_type"] == "UPFRONT_FEE"

def test_prepare_investment(setup_investment):
    response, status_code = InvestmentServices(
        str(setup_investment.id)
    ).prepare_investment()
    assert status_code == 202
    assert response["status"] == "PROCESSING_INVESTMENT"
    assert response["investment"]["source_id"]
    assert response["investment"]["source_type"] == "INVESTOR"
    assert response["investment"]["destination_id"]
    assert response["investment"]["destination_type"] == "INVESTMENT"
    assert response["investment"]["amount"] == -setup_investment.total_amount


def test_continue_investment(setup_investment):
    response, status_code = InvestmentServices(
        str(setup_investment.id)
    ).continue_investment()
    assert status_code == 202
    assert response["upfront_fee"]
    assert response["receive_invest"]
    assert response["disbursements"]
