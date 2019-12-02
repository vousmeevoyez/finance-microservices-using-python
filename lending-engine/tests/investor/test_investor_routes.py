from tests.api_list import approve_investor, withdraw_rdl


def test_approve_investor(setup_client, setup_investor):
    result = approve_investor(setup_client, str(setup_investor.id))
    response = result.get_json()
    assert response["id"]
    assert result.status_code == 202


def test_withdraw_investor(setup_client, setup_investor, setup_investor_wallet):
    payload = {
        "destination_id": str(setup_investor.bank_accounts[1].id),
        "amount": 1000
    }
    result = withdraw_rdl(setup_client, str(setup_investor.id), payload)
    response = result.get_json()
    assert response["id"]
    assert result.status_code == 202
