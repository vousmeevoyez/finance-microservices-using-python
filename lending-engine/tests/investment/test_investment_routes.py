from tests.api_list import process_invest


def test_process_invest(setup_client, setup_investment_with_loan, setup_investor_wallet):
    investment, loan_request = setup_investment_with_loan
    result = process_invest(setup_client, str(investment.id))
    assert result.status_code == 202
