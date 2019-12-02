import pytest
from grpc import RpcError

from unittest.mock import Mock, patch

from app.api.models.investor import Investor
from app.api.models.investment import Investment
from app.api.models.wallet import Wallet
from task.investor.tasks import InvestorTask

from celery.exceptions import MaxRetriesExceededError


@patch("task.investor.rpc.email.email_pb2_grpc.EmailNotificationStub")
def test_send_approval_email(mock_email):
    mock_email.return_value.SendEmail.return_value = Mock(
        status="OK"
    )
    result = InvestorTask().send_approval_email("kelvin@modana.id")
    assert result


@patch("task.investor.rpc.bni_rdl.rdl_account_pb2_grpc.RdlAccountStub")
def test_create_rdl(mock_rdl, setup_investor_rdl, setup_investor):
    mock_rdl.return_value.CreateRdl.return_value = Mock(
        account_no="12345678123",
        journal_no="0000102312",
    )
    InvestorTask().create_rdl(setup_investor.id)

    investor = Investor.find_one({"id": setup_investor.id})
    assert len(investor.approvals) == 2
    assert investor.approvals[0].status == "PROCESSING"
    assert investor.approvals[1].status == "APPROVED"
    assert len(investor.bank_accounts) == 3

    assert investor.bank_accounts[2].account_type == "RDL_ACCOUNT"
    assert investor.bank_accounts[2].account_no == "12345678123"

    wallet = Wallet.find_one({"user_id": setup_investor.user_id})
    assert wallet.balance == 0


@patch("task.investor.rpc.bni_rdl.rdl_account_pb2_grpc.RdlAccountStub")
@patch("task.investor.tasks.InvestorTask.retry")
def test_create_rdl_failed(mock_rdl, mock_celery, setup_investor_rdl, setup_investor):
    mock_rdl.CreateRdl.side_effect = RpcError()
    mock_celery.side_effect = MaxRetriesExceededError()

    with pytest.raises(MaxRetriesExceededError):
        InvestorTask().create_rdl(setup_investor.id)

        investor = Investor.find_one({"id": setup_investor.id})
        assert len(investor.approvals) == 2
        # make sure status recorded!
        assert investor.approvals[0].status == "PROCESSING"
        assert investor.approvals[1].status == "FAILED"
