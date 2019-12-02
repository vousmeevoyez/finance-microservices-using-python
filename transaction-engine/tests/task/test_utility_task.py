import pytest
from grpc import RpcError

from unittest.mock import Mock, patch
from app.api.models.transaction import Transaction
from task.utility.tasks import UtilityTask
from celery.exceptions import MaxRetriesExceededError


@patch("requests.post")
def test_callback_transaction(mock_post, setup_debit_transaction):
    mock_post.return_value.json.return_value = {
        "status": "SEND_INVESTMENT_SUCCESS"
    }
    result = UtilityTask().notify(str(setup_debit_transaction.id))
    assert result


@patch("requests.post")
@patch("task.transaction.tasks.TransactionTask.retry")
def test_send_transaction_retry(mock_post, mock_celery, setup_debit_transaction):
    mock_post.return_value.json.return_value = {"id": "some-trx-id"}
    mock_celery.side_effect = MaxRetriesExceededError()
    with pytest.raises(MaxRetriesExceededError):
        UtilityTask().notify(str(setup_debit_transaction.id))
