from app.api.callback.factories.factory import CallbackInfo
from app.api.callback.factories.factory import generate_internal_callback

from app.api.models.investment import Investment


def test_generate_internal_callback(setup_investment_with_transaction):
    investment, loan_request, transactions = setup_investment_with_transaction

    callback_info = CallbackInfo(
        transaction_id=str(transactions[0].id),
        transaction_type=transactions[0].transaction_type,
        status="SUCCESS"
    )
    callback = generate_internal_callback(callback_info)
    callback.update()

    investment = Investment.find_one({"id": investment.id})
    assert any("SUCCESS" in iv.status for iv in investment.list_of_status)
