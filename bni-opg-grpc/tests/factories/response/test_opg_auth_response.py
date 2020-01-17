"""
    Test BNI OPG Auth Response
    ______________
"""
from unittest.mock import Mock
import pytest

from rpc.factories.response.v1.response import BNIOpgAuthResponse
from rpc.lib.core.response import ResponseError

from tests.reusable.setup import create_http_response


@pytest.mark.asyncio
async def test_to_representation_success():
    """ test case wbere BNI VA return success """
    # validate successfull http status code

    expected_data = {
        "access_token": "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2",
        "token_type": "Bearer",
        "expires_in": 3599,
        "scope": "resource.WRITE resource.READ",
    }

    mock_http_response = create_http_response(200, expected_data)

    response = BNIOpgAuthResponse()
    await response.set(mock_http_response)
    assert response.to_representation() == expected_data


@pytest.mark.asyncio
async def test_to_representation_failed():
    """ test case wbere BNI VA return success """
    # validate successfull http status code

    expected_data = {"error": "unauthorized error"}

    mock_http_response = create_http_response(403, expected_data)

    with pytest.raises(ResponseError):
        response = BNIOpgAuthResponse()
        await response.set(mock_http_response)
        response.to_representation()
