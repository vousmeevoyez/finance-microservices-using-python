"""
    Excute Async HTTP Call
    ____________________
"""
import logging

import aiohttp
import asyncio

from rpc.logger import logger as fetch_logger
from rpc.lib.core.exceptions import BaseError


class FetchError(BaseError):
    """ raised when aiohttp error """


async def fetch(request, response, connector=None):
    """ async call using request and response """

    fetch_logger.setLevel(logging.INFO)

    async with aiohttp.ClientSession() as session:
        try:
            # logging request
            fetch_logger.info("REQUEST: {} - {}".format(request.method, request.url))

            async with session.request(**request.to_representation()) as resp:
                data = await resp.json()
                await response.set(resp)

            # logging response
            fetch_logger.info("STATUS CODE: {}".format(resp.status))
            fetch_logger.info("RESPONSE: {}".format(data))
        except asyncio.TimeoutError as error:
            raise FetchError("TIMEOUT", error)
        else:
            return response.to_representation()
