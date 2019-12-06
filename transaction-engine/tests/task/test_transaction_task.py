import pytest
from pymongo.errors import ConnectionFailure, OperationFailure
from celery.exceptions import Retry, MaxRetriesExceededError

from unittest.mock import Mock, patch

from app.api.models.transaction import Transaction
from app.api.models.wallet import Wallet
from task.transaction.tasks import TransactionTask


def test_apply_transaction(setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction
    transaction = transactions[0]

    TransactionTask().apply(transaction.id)
    # make sure transaction applied
    transaction = Transaction.find_one({"_id": transaction.id})
    assert transaction.status == "APPLIED"
    assert transaction.balance == 0
    # make sure wallet deducted
    wallet = Wallet.find_one({"_id": transaction.wallet_id})
    assert wallet.balance == 0


@patch("pymongo.client_session.ClientSession")
@patch("task.transaction.tasks.TransactionTask.retry")
def test_apply_transaction_connection_failure(
    mock_pymongo, mock_celery, setup_investment_with_transaction
):
    investment, loan_request, transactions = setup_investment_with_transaction
    transaction = transactions[0]

    # set side effect
    mock_pymongo.commit_transaction.side_effect = ConnectionFailure()
    mock_celery.side_effect = Retry()

    with pytest.raises(Retry):
        TransactionTask().apply(transaction.id)

        # make sure transaction not applied
        transaction = Transaction.find_one({"_id": transaction.id})
        assert transaction.status == "APPLYING"
        assert transaction.balance == 0

        # make sure wallet not deducted
        wallet = Wallet.find_one({"_id": transaction.wallet_id})
        assert wallet.balance == 1000


@patch("pymongo.client_session.ClientSession")
@patch("task.transaction.tasks.TransactionTask.retry")
def test_apply_transaction_operation_failure(
    mock_pymongo, mock_celery, setup_investment_with_transaction
):
    investment, loan_request, transactions = setup_investment_with_transaction
    transaction = transactions[0]

    # set side effect
    mock_pymongo.commit_transaction.side_effect = OperationFailure(Mock())
    mock_celery.side_effect = Retry()

    with pytest.raises(Retry):
        TransactionTask().apply(transaction.id)

        # make sure transaction not applied
        transaction = Transaction.find_one({"_id": transaction.id})
        assert transaction.status == "APPLYING"
        assert transaction.balance == 0

        # make sure wallet not deducted
        wallet = Wallet.find_one({"_id": transaction.wallet_id})
        assert wallet.balance == 1000
