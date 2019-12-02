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
    """ test case wbere BNI RDL auth return success """
    # validate successfull http status code

    expected_data = {
        "access_token": "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2",
        "token_type": "Bearer",
        "expires_in": 3599,
        "scope": "resource.WRITE resource.READ",
    }

    mock_http_response = create_http_response(200, expected_data)

    bni_response = BNIRdlAuthResponse()
    await bni_response.set(mock_http_response)
    assert bni_response.to_representation() == expected_data


@pytest.mark.asyncio
async def test_to_representation_failed():
    """ test case wbere BNI RDL return failed """
    # validate successfull http status code

    expected_data = {"error": "unauthorized error"}

    mock_http_response = create_http_response(401, expected_data)

    with pytest.raises(ResponseError):
        bni_response = BNIRdlAuthResponse()
        await bni_response.set(mock_http_response)
        bni_response.to_representation()
