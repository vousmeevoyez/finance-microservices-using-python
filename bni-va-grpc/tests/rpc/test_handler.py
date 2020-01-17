import pytest

from asynctest import CoroutineMock, patch

from datetime import datetime
from rpc.models import VirtualAccount
from rpc.services import BNIVaServices
from rpc.services import ServicesError


@pytest.mark.asyncio
@patch("rpc.factories.provider.v1.provider.BNIVaProvider.create_va")
async def test_create_virtual_account(mock_provider):
    payload = {
        "trx_id": "some-trx-id",
        "amount": 0,
        "name": "some-va-name",
        "phone_number": "081219644314",
        "account_no": "123312312312312",
        "expired_at": datetime.utcnow(),
    }
    expected_value = {"virtual_account": "123312312312312", "trx_id": "1231231231"}
    mock_provider.return_value = expected_value

    result = await BNIVaServices("CREDIT").create_va(payload)
    assert result == expected_value


@pytest.mark.asyncio
@patch("rpc.factories.provider.v1.provider.BNIVaProvider.get_inquiry")
async def test_inquiry_va(mock_provider, setup_va_object):
    expected_value = {
        "email": "",
        "paid_amount": 0,
        "trx_amount": 1,
        "created_at": "2018-10-26T06:39:27+07:00",
        "billing_type": "j",
        "account_no": "9889909918102605",
        "description": "",
        "status": "INACTIVE",
        "trx_id": "121",
        "updated_at": "2018-10-26T06:43:25+07:00",
        "phone_number": "",
        "paid_at": None,
        "name": "Jennie",
        "ref_number": None,
        "expired_at": "2017-10-28T06:39:27+07:00",
    }

    mock_provider.return_value = expected_value

    result = await BNIVaServices("CREDIT", setup_va_object.account_no).inquiry_va()
    assert result == expected_value


@pytest.mark.asyncio
async def test_inquiry_va_not_found():
    with pytest.raises(ServicesError):
        result = await BNIVaServices("CREDIT", "9889909918102605").inquiry_va()


@pytest.mark.asyncio
@patch("rpc.factories.provider.v1.provider.BNIVaProvider.update_va")
async def test_update_va(mock_provider, setup_va_object):
    payload = {
        "trx_id": "some-trx-id",
        "amount": 0,
        "name": "updated-va-name",
        "expired_at": datetime.utcnow(),
    }

    expected_value = {"virtual_account": "123312312312312", "trx_id": "1231231231"}

    mock_provider.return_value = expected_value

    result = await BNIVaServices("CREDIT", setup_va_object.account_no).update_va(
        payload
    )
    assert result == expected_value


@pytest.mark.asyncio
@patch("rpc.factories.provider.v1.provider.BNIVaProvider.update_va")
async def test_update_va(mock_provider, setup_va_object):
    payload = {
        "trx_id": "0010203012030",
        "amount": 0,
        "name": "updated-va-name",
        "expired_at": datetime.utcnow(),
    }

    expected_value = {"virtual_account": "123312312312312", "trx_id": "1231231231"}

    mock_provider.return_value = expected_value

    result = await BNIVaServices("CREDIT", setup_va_object.account_no).update_va(
        payload
    )
    assert result == expected_value

    va = VirtualAccount.objects.get(account_no=setup_va_object.account_no)
    assert va.trx_id == "0010203012030"
    assert va.name == "updated-va-name"


@pytest.mark.asyncio
@patch("rpc.factories.provider.v1.provider.BNIVaProvider.update_va")
async def test_disable_va(mock_provider, setup_va_object):
    expected_value = {"virtual_account": "123312312312312", "trx_id": "1231231231"}

    mock_provider.return_value = expected_value

    result = await BNIVaServices("CREDIT", setup_va_object.account_no).disable_va()

    assert result == {"status": "OK"}

    va = VirtualAccount.objects(account_no=setup_va_object.account_no).first()
    assert va is None
