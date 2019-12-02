import pytest
import json
from datetime import datetime

from asynctest import CoroutineMock, patch


from rpc.lib.core.provider import ProviderError
from rpc.lib.helper import encrypt
from rpc.factories.provider.v1.provider import (
    BNIVaProvider
)

from rpc.config.external import BNI_ECOLLECTION


def encrypt_response(data, types):
    encrypted_data = encrypt(
        BNI_ECOLLECTION[f"{types}_CLIENT_ID"],
        BNI_ECOLLECTION[f"{types}_SECRET_KEY"],
        data
    )
    return encrypted_data


""" All test case for testing remote call utility"""
@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_create_va_success(mock_post):
    # payload needed to create virtual account
    data = {
        "trx_id": "1234",
        "amount": "1500",
        "name": "Jennie",
        "phone_number": "081234123111",
        "expired_at": datetime.now(),
        "account_no": "12345678",
    }

    # expected value from BNI server
    plain_data = {"trx_id": "1234", "virtual_account": "000211"}
    expected_data = {
        "status": "000",
        "data": encrypt_response(plain_data, "CREDIT"),
    }

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 200
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)

    provider = BNIVaProvider()
    provider.set("CREDIT")
    result = await provider.create_va(**data)
    assert result["trx_id"] == plain_data["trx_id"]
    assert result["account_no"] == plain_data["virtual_account"]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_create_va_failed(mock_post):
    """
        test function to try create va but failed using mock response
        from BNIVaProviderHelper._post
    """
    # payload needed to create a va
    data = {
        "trx_id": "1234",
        "amount": "1500",
        "name": "Jennie",
        "phone_number": "081234123111",
        "expired_at": datetime.now(),
        "account_no": "12345678",
    }

    # expected value from BNI server
    plain_data = {"trx_id": "1234", "virtual_account": "000211"}
    expected_data = {"status": "001", "message": "my cool error"}

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 400
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)

    with pytest.raises(ProviderError):
        provider = BNIVaProvider()
        provider.set("CREDIT")
        await provider.create_va(**data)

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_create_va_cardless_success(mock_post):
    """
        test function to create cardless va using mock response
        from BNIVaProviderHelper._post
    """
    # required paylod to create va
    data = {
        "amount": "1500",
        "name": "Jennie",
        "phone_number": "081234123111",
        "expired_at": datetime.now(),
        "account_no": "12345678",
        "trx_id": "12345678",
    }

    # expected value from BNI server
    plain_data = {"trx_id": "12345678", "virtual_account": "000211"}
    expected_data = {"status": "000", "data": encrypt_response(plain_data, "DEBIT")}

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 200
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)


    provider = BNIVaProvider()
    provider.set("DEBIT")
    result = await provider.create_va(**data)
    assert result["trx_id"] == plain_data["trx_id"]
    assert result["account_no"] == plain_data["virtual_account"]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_create_va_cardless_failed(mock_post):
    """
        test function to try create cardless va but failed using mock response
        from BNIVaProviderHelper._post
    """
    # required payload to create va
    data = {
        "amount": "1500",
        "name": "Jennie",
        "phone_number": "081234123111",
        "expired_at": datetime.now(),
        "account_no": "12345678",
        "trx_id": "12345678",
    }

    expected_data = {"status": "001", "message": "my cool error"}

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 400
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)

    with pytest.raises(ProviderError):
        provider = BNIVaProvider()
        provider.set("CREDIT")
        await provider.create_va(**data)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_get_inquiry_success(mock_post):
    """
        test function to get va inquiry using mock response
        from BNIVaProviderHelper._post
    """

    # expected_value from bni server
    plain_data = {
        "client_id": "99099",
        "trx_id": "121",
        "virtual_account": "9889909918102605",
        "trx_amount": "1",
        "customer_name": "Jennie",
        "customer_phone": "",
        "customer_email": "",
        "datetime_created": "2018-10-26 06:39:27",
        "datetime_expired": "2017-10-28 06:39:27",
        "datetime_payment": None,
        "datetime_last_updated": "2018-10-26 06:43:25",
        "payment_ntb": None,
        "payment_amount": "0",
        "va_status": "2",
        "description": "",
        "billing_type": "j",
        "datetime_created_iso8601": "2018-10-26T06:39:27+07:00",
        "datetime_expired_iso8601": "2017-10-28T06:39:27+07:00",
        "datetime_payment_iso8601": None,
        "datetime_last_updated_iso8601": "2018-10-26T06:43:25+07:00",
    }

    expected_data = {
        "status": "000",
        "data": encrypt_response(plain_data, "CREDIT"),
    }

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 200
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)


    provider = BNIVaProvider()
    provider.set("CREDIT")
    result = await provider.get_inquiry("121")

    assert result["trx_id"] == plain_data["trx_id"]
    assert result["account_no"] == plain_data["virtual_account"]
    assert str(result["trx_amount"]) == plain_data["trx_amount"]
    assert result["name"] == plain_data["customer_name"]
    assert result["phone_number"] == plain_data["customer_phone"]
    assert result["email"] == plain_data["customer_email"]
    assert result["created_at"] == plain_data["datetime_created_iso8601"]
    assert result["expired_at"] == plain_data["datetime_expired_iso8601"]
    assert result["paid_at"] == plain_data["datetime_payment_iso8601"]
    assert result["updated_at"] == plain_data["datetime_last_updated_iso8601"]
    assert result["ref_number"] == plain_data["payment_ntb"]
    assert str(result["paid_amount"]) == plain_data["payment_amount"]
    assert result["status"] == "INACTIVE"
    assert result["description"] == plain_data["description"]
    assert result["billing_type"] == plain_data["billing_type"]

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_get_inquiry_failed(mock_post):
    """
        test function to try get va inquiry but failed using mock response
        from BNIVaProviderHelper._post
    """

    expected_data = {"status": "001", "message": "super cool error"}

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 400
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)

    # dummy trx id
    with pytest.raises(ProviderError):
        provider = BNIVaProvider()
        provider.set("CREDIT")
        await provider.get_inquiry("123")

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_update_va_success(mock_post):
    """
        test function to try update va using mock response
        from BNIVaProviderHelper._post
    """
    data = {
        "trx_id": "627493687",
        "amount": "1000",
        "name": "Kelvin",
        "expired_at": datetime.now(),
    }

    plain_data = {
        "trx_id": "627493687",
        "virtual_account": "9889909918102605",
    }

    expected_data = {
        "status": "000",
        "data": encrypt_response(plain_data, "CREDIT"),
    }

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 200
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)

    provider = BNIVaProvider()
    provider.set("CREDIT")
    result = await provider.update_va(**data)
    assert result["trx_id"] == plain_data["trx_id"]
    assert result["account_no"] == plain_data["virtual_account"]

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.request")
async def test_mock_update_va_failed(mock_post):
    """
        test function to try update va but falied using mock response
        from BNIVaProviderHelper._post
    """
    data = {
        "trx_id": "627493687",
        "amount": "1000",
        "name": "Kelvin",
        "expired_at": datetime.now(),
    }

    expected_data = {"status": "00`", "message": "my cool error"}

    # replace return value using expected value here
    mock_post.return_value.__aenter__.return_value.status = 400
    mock_post.return_value.__aenter__.return_value.json = \
    CoroutineMock(return_value=expected_data)

    with pytest.raises(ProviderError):
        provider = BNIVaProvider()
        provider.set("CREDIT")
        await provider.update_va(**data)
