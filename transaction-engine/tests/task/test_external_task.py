import pytest
from grpc import RpcError
from pymongo.errors import OperationFailure
from celery.exceptions import Retry, MaxRetriesExceededError

from unittest.mock import Mock, patch

from app.api.models.transaction import Transaction
from app.api.models.wallet import Wallet
from task.external.tasks import ExternalTask


@patch("task.external.factories.helper.RdlTransferStub")
def test_external_transfer(mock_transfer, setup_debit_transaction):
    mock_transfer.return_value.Transfer.return_value = Mock(response_uuid="12345678910")

    transaction_id, result, reference_no = ExternalTask().transfer(setup_debit_transaction.id)
    # make sure transaction applied
    assert transaction_id == setup_debit_transaction.id
    assert result == "COMPLETED"
    assert reference_no == "12345678910"


@patch("task.external.factories.helper.RdlTransferStub")
@patch("task.transaction.tasks.TransactionTask.retry")
def test_external_transfer_rpc_error(
    mock_transfer, mock_celery, setup_debit_transaction
):
    # set side effect
    mock_transfer.Transfer.side_effect = RpcError()
    mock_celery.side_effect = Retry()

    with pytest.raises(Retry):
        ExternalTask().transfer(setup_debit_transaction.id)


@patch("task.external.factories.helper.RdlTransferStub")
@patch("task.transaction.tasks.TransactionTask.retry")
def test_external_transfer_max_rpc_error(mock_rdl, mock_celery, setup_debit_transaction):
    # set side effect
    mock_rdl.Transfer.side_effect = RpcError()
    mock_celery.side_effect = MaxRetriesExceededError()

    with pytest.raises(MaxRetriesExceededError):
        transaction_id, result, reference_no = ExternalTask().transfer(setup_debit_transaction.id)
        # make sure transaction applied
        assert transaction_id == str(setup_debit_transaction.id)
        assert result == "FAILED"


def test_apply_external(setup_debit_transaction):
    transfer = str(setup_debit_transaction.id), "COMPLETED", "12345678910"
    ExternalTask().apply_external(transfer)

    # make sure transaction applied
    transaction = Transaction.find_one({"_id": setup_debit_transaction.id})
    assert transaction.payment.status == "COMPLETED"
    assert transaction.payment.reference_no == "12345678910"


def test_apply_external_failed(setup_debit_transaction):
    transfer = str(setup_debit_transaction.id), "FAILED", None
    ExternalTask().apply_external(transfer)

    # make sure trigger refund
    transaction = Transaction.find_one({"_id": setup_debit_transaction.id})
    assert transaction.status == "CANCELLED"
    assert transaction.payment.status == "FAILED"

    # make sure wallet not deducted
    wallet = Wallet.find_one({"_id": transaction.wallet_id})
    assert wallet.balance == 1000

    refund = Transaction.find_one({
        "transaction_type": "DEBIT_REFUND",
        "wallet_id": wallet.id
    })
    assert refund

'''
@patch("pymongo.mongo_client.MongoClient")
@patch("task.transaction.tasks.TransactionTask.retry")
def test_apply_external_commit_error(mock_pymongo, mock_celery, setup_debit_transaction):
    # set side effect
    mock_pymongo.commit_transaction.side_effect = OperationFailure("test")
    mock_celery.side_effect = Retry()

    with pytest.raises(Retry):
        ExternalTask().apply_external(
            str(setup_debit_transaction.id), "COMPLETED", "12345678910"
        )
'''
