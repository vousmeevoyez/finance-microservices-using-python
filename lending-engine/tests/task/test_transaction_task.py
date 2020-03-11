import pytest
from grpc import RpcError
from bson import ObjectId

from unittest.mock import Mock, patch
from app.api.models.investment import Investment
from app.api.models.loan_request import LoanRequest
from task.transaction.tasks import TransactionTask
from celery.exceptions import MaxRetriesExceededError


@patch("requests.post")
def test_send_transaction(mock_post):
    mock_post.return_value.json.return_value = {"id": "some-trx-id"}
    payload = {
        "wallet_id": "some-wallet-id",
        "source_id": "some-source-id",
        "source_type": "some-valid-source-type",
        "destination_id": "some-destination-id",
        "destination_type": "some-destination-type",
        "amount": 100000,
        "transaction_type": "TOP_UP_RDL",
        "reference_no": "1231231312312",
    }
    result = TransactionTask().send_transaction(**payload)
    assert result


@patch("requests.post")
@patch("task.transaction.tasks.TransactionTask.retry")
def test_send_transaction_retry(mock_post, mock_celery):
    mock_post.return_value.json.return_value = {"id": "some-trx-id"}
    mock_celery.side_effect = MaxRetriesExceededError()
    payload = {
        "wallet_id": "some-wallet-id",
        "source_id": "some-source-id",
        "source_type": "some-valid-source-type",
        "destination_id": "some-destination-id",
        "destination_type": "some-destination-type",
        "amount": 100000,
        "transaction_type": "TOP_UP_RDL",
        "reference_no": "1231231312312",
    }
    with pytest.raises(MaxRetriesExceededError):
        TransactionTask().send_transaction(**payload)


@patch("requests.post")
def test_send_transaction_with_models(mock_post,
                                      setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction

    mock_post.return_value.json.return_value = {"id": transactions[0].id}
    payload = {
        "wallet_id": "some-wallet-id",
        "source_id": "some-source-id",
        "source_type": "some-valid-source-type",
        "destination_id": "some-destination-id",
        "destination_type": "some-destination-type",
        "amount": -100000,
        "transaction_type": "INVEST",
        "model": "Investment",
        "model_id": str(investment.id),
        "status": "SEND_TO_INVESTMENT_REQUESTED"
    }
    result = TransactionTask().send_transaction(**payload)
    assert result["transaction_id"]
    assert result["model"]
    assert result["model_id"]
    assert result["status"]


def test_map_bulk_transaction(make_loan_request):
    loan_request = make_loan_request()
    loan_request2 = make_loan_request()

    fake_trx_id = ObjectId()
    transaction_result = {
        "transaction_ids": [fake_trx_id],
        "update_records": [{
            "model": "LoanRequest",
            "model_id": str(loan_request.id),
            "status": "SEND_TO_PROFIT_REQUESTED"
        }, {
            "model": "LoanRequest",
            "model_id": str(loan_request2.id),
            "status": "SEND_TO_PROFIT_REQUESTED"
        }]
    }
    TransactionTask().map_bulk_transaction(transaction_result)

    # make sure transaction id is added
    loan_requests = list(LoanRequest.collection.find(
        {"lst.transaction_id": fake_trx_id}
    ))
    assert len(loan_requests) == 2
