from grpc import RpcError

from unittest.mock import Mock, patch

from app.api.models.loan_request import LoanRequest
from task.investment.tasks import InvestmentTask


@patch("task.investment.rpc.modanaku.payment_plan_pb2_grpc.PaymentPlanStub")
def test_create_payment_plan(mock_modanaku, make_loan_request):
    inner_obj = Mock(payment_plan_id="payment_plan_id",
                     bank_account_id="bank_account_id")
    mock_modanaku.return_value.CreatePaymentPlan.return_value = Mock(
        body=inner_obj
    )

    loan_request = make_loan_request()

    InvestmentTask().create_payment_plan(loan_request.id)

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    # make sure loan_request status added!
    assert loan_request.list_of_status[0].status == "PAYMENT_PLAN_CREATED"
    assert loan_request.modanaku.bank_account_id == "bank_account_id"
    assert loan_request.modanaku.payment_plan_id == "payment_plan_id"
