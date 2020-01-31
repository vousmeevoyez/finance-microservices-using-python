from unittest.mock import Mock, patch

from celery.result import AsyncResult

from app.api.investor.modules.services import (
    approve_investor,
    withdraw,
    sync_balance
)


def test_approve_investor(setup_investor):
    response, status_code = approve_investor(str(setup_investor.id))
    assert status_code == 202


def test_withdraw_investor(setup_investor, setup_investor_wallet):
    response, status_code = withdraw(str(setup_investor.id),
                                     str(setup_investor.bank_accounts[1].id),
                                     10000)
    assert status_code == 202


'''
@patch("task.investor.tasks.InvestorTask.sync_rdl")
def test_sync_balance_investor(
        mock_sync,
        setup_investor,
):
    result = {
        "wallet_id": "wallet-id",
        "source_id": "source-id",
        "source_type": "INVESTOR_RDL_ACC",
        "destination_id": "destination-id",
        "destination_type": "INVESTOR",
        "amount": -100,
        "transaction_type": "CREDIT_ADJUSTMENT",
    }

    mock_sync.apply_async.return_value = result

    response, status_code = sync_balance(
        str(setup_investor.id),
    )
    assert status_code == 202
'''
