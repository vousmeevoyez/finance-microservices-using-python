import pytest
from grpc import RpcError

from unittest.mock import Mock, patch

from app.api.models.investment import Investment
from app.api.models.base import StatusEmbed
from app.api.models.loan_request import LoanRequest
from task.virtual_account.tasks import VirtualAccountTask

from celery.exceptions import MaxRetriesExceededError


@patch("task.virtual_account.rpc.bni_va.virtual_account_pb2_grpc.VirtualAccountStub")
def test_create_investment_va(mock_rdl, setup_investment):
    mock_rdl.return_value.CreateVa.return_value = Mock(
        account_no="9889909611123123",
        trx_id="0000102312"
    )
    VirtualAccountTask().create_va(**{
        "model_name": "Investment",
        "model_id": str(setup_investment.id),
        "va_type": "INVESTMENT"
    })

    investment = Investment.find_one({"id": setup_investment.id})
    # make sure investment va created!
    assert investment.bank_accounts[0].account_no
    assert investment.bank_accounts[0].account_type == "VIRTUAL_ACCOUNT"
    assert investment.bank_accounts[0].bank_name
    # make sure investment status added!
    assert investment.list_of_status[0].status == "INVESTMENT_VA_CREATED"


@patch("task.virtual_account.rpc.bni_va.virtual_account_pb2_grpc.VirtualAccountStub")
@patch("task.virtual_account.tasks.VirtualAccountTask.retry")
def test_create_investment_va_failed(mock_va, mock_celery, setup_investment):
    mock_va.CreateVa.side_effect = RpcError()
    mock_celery.side_effect = MaxRetriesExceededError()

    with pytest.raises(MaxRetriesExceededError):
        VirtualAccountTask().create_va(**{
            "model_name": "Investment",
            "model_id": str(setup_investment.id),
            "va_type": "INVESTMENT"
        })

        investment = Investment.find_one({"id": setup_investment.id})
        # make sure investment status added!
        assert investment.list_of_status[0].status == "INVESTMENT_VA_FAILED"


@patch("task.virtual_account.rpc.bni_va.virtual_account_pb2_grpc.VirtualAccountStub")
def test_create_repayment_va(mock_rdl, make_loan_request):
    mock_rdl.return_value.CreateVa.return_value = Mock(
        account_no="123119978123",
        trx_id="110102312"
    )

    loan_request = make_loan_request()

    VirtualAccountTask().create_va(**{
        "model_name": "LoanRequest",
        "model_id": str(loan_request.id),
        "va_type": "REPAYMENT",
        "custom_status": "REPAYMENT"
    })

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    # make sure investment va created!
    assert loan_request.bank_accounts[2].account_no == "123119978123"
    assert loan_request.bank_accounts[2].account_type == "VIRTUAL_ACCOUNT"
    assert loan_request.bank_accounts[2].bank_name
    # make sure loan_request status added!
    assert loan_request.list_of_status[0].status == "REPAYMENT_VA_CREATED"


@patch("task.virtual_account.rpc.bni_va.virtual_account_pb2_grpc.VirtualAccountStub")
@patch("task.virtual_account.tasks.VirtualAccountTask.retry")
def test_create_repayment_va_failed(mock_va, mock_celery, make_loan_request):
    mock_va.CreateVa.side_effect = RpcError()
    mock_celery.side_effect = MaxRetriesExceededError()

    loan_request = make_loan_request()

    with pytest.raises(MaxRetriesExceededError):
        VirtualAccountTask().create_va(**{
            "model_name": "LoanRequest",
            "model_id": str(loan_request.id),
            "va_type": "REPAYMENT"
        })

        loan_request = LoanRequest.find_one({"id": loan_request.id})
        # make sure investment status added!
        assert loan_request.list_of_status[0].status == "REPAYMENT_VA_FAILED"
