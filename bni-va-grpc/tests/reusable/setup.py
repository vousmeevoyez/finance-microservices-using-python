"""
    Fixtures
"""
from unittest.mock import Mock
import asyncio


@asyncio.coroutine
def json_coroutine(response):
    """ coroutine used by aiohttp """
    return response


@asyncio.coroutine
def raise_coroutine(exception):
    """ raise coroutine used by aiohttp """
    raise exception


def create_http_response(status_code, response=None, exception=None):
    """ fixture to create http response """
    http_response = Mock(status=status_code)
    if http_response is not None:
        http_response.json = lambda: json_coroutine(response)
    if exception is not None:
        http_response.json = lambda: raise_coroutine(exception)
    return http_response
