from app.api.investor.modules.services import approve_investor, withdraw


def test_approve_investor(setup_investor):
    response, status_code = approve_investor(str(setup_investor.id))
    assert status_code == 202


def test_withdraw_investor(setup_investor, setup_investor_wallet):
    response, status_code = withdraw(str(setup_investor.id),
                                     str(setup_investor.bank_accounts[1].id),
                                     10000)
    assert status_code == 202
