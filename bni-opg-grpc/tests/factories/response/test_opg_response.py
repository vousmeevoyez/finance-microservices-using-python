"""
    Test BNI OPg Response
    ______________
"""
import pytest

from rpc.factories.response.v1.response import BNIOpgResponse
from rpc.lib.core.response import ResponseError

from tests.reusable.setup import create_http_response


@pytest.mark.asyncio
async def test_to_representation_success():
    """ test case wbere BNI OPG return success """
    # validate successfull http status code

    expected_data = {
        "getBalanceResponse": {
            "clientId": "BNISERVICE",
            "parameters": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2017-02-24T14:12:25.871Z",
                "customerName": "Bpk JONOMADE MADEMADEMADEMADE IMAMADE",
                "accountCurrency": "IDR",
                "accountBalance": 16732765949981,
            },
        }
    }

    mock_http_response = create_http_response(200, expected_data)

    response = BNIOpgResponse()
    await response.set(mock_http_response)
    assert response.to_representation() == expected_data


@pytest.mark.asyncio
async def test_to_representation_failed():
    """ test case wbere BNI VA return success """
    # validate successfull http status code

    expected_data = {
        "getBalanceResponse": {
            "clientId": "BNISERVICE",
            "parameters": {
                "responseCode": "0000",
                "errorMessage": "Unknown Output",
                "responseMessage": "Request failed",
                "responseTimestamp": "2017-02-24T14:12:25.871Z",
            },
        }
    }

    mock_http_response = create_http_response(200, expected_data)

    with pytest.raises(ResponseError):
        response = BNIOpgResponse()
        await response.set(mock_http_response)
        response.to_representation()
