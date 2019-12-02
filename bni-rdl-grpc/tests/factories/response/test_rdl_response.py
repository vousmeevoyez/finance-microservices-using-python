"""
    Test BNI RDL REsponse
    ______________
"""
import pytest
from unittest.mock import Mock

from rpc.factories.response.v1.response import BNIRdlAuthResponse, BNIRdlResponse
from rpc.lib.core.response import ResponseError

from tests.reusable.setup import create_http_response


@pytest.mark.asyncio
async def test_to_representation_success():
    """ test case where BNI RDL return success """
    # validate successfull http status code

    expected_data = {
        "response": {
            "responseCode": "0001",
            "responseMessage": "Request has been processed successfully",
            "responseTimestamp": "2018-12-06 23:11:44.226",
            "responseUuid": "29FCB72E71D34C48",
            "journalNum": "000000",
            "cifNumber": "9100749959",
            "mobilePhone": "0812323232",
            "branchOpening": "00259",
            "idNumber": "331234766887878518",
            "customerName": "JUAN DANIEL",
        }
    }

    mock_http_response = create_http_response(200, expected_data)

    bni_response = BNIRdlResponse()
    await bni_response.set(mock_http_response)
    assert bni_response.to_representation() == expected_data["response"]


@pytest.mark.asyncio
async def test_to_representation_failed():
    """ test case wbere BNI RDL return success """
    # validate successfull http status code

    expected_data = {
        "response": {
            "responseCode": "0007",
            "responseMessage": "Request has been processed unsuccessfully",
            "errorMessage": "Request can not be authenticated",
            "responseTimestamp": "2019-10-03 14:26:09.460",
        }
    }

    mock_http_response = create_http_response(401, expected_data)

    with pytest.raises(ResponseError):
        bni_response = BNIRdlResponse()
        await bni_response.set(mock_http_response)
        bni_response.to_representation()
