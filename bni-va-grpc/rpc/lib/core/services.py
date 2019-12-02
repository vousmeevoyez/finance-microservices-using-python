"""
    Base Services
    _____________________
"""
from aiohttp import web

from ecollection.app.factories import generate_provider
from ecollection.app.lib.core.provider import ProviderError
from ecollection.app.lib.helper import extract_error


class BaseServices:
    """ base services class """

    provider_name = None

    async def execute(self, method_name, **params):
        """ execute designated method_name and convert it
        into right response """
        status = 200
        try:
            provider = await generate_provider(self.provider_name)
            provider_method = getattr(provider, method_name)
            response = await provider_method(**params)
        except ProviderError as error:
            message = extract_error(error)
            response = {"error": message}
            status = 400
        return web.json_response(response, status=status)
