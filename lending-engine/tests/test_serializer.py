import pytest
from marshmallow.exceptions import ValidationError
from app.api.serializer import BniVaCallbackSchema


def test_load():
    data = {
        "virtual_account": "9889909600023000",
        "customer_name": "jennie",
        "trx_id": "12312312312",
        "trx_amount": "0",
        "payment_amount": "50000",
        "cumulative_payment_amount": "50000",
        "payment_ntb": "12345",
        "datetime_payment": "2018-12-20 11:16:00",
    }
    with pytest.raises(ValidationError):
        result = BniVaCallbackSchema(strict=True).load(data)
