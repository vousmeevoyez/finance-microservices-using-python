from app.lib.remote_call import fetch
from app.factories.factory import generate_request_response

# base exceptions
from app.lib.exceptions import BaseError

# response exceptions
from app.lib.response import (
    StatusCodeError,
    FailedResponseError,
    InvalidResponseError,
    ResponseError,
)

# remote call exceptions
from app.lib.remote_call import FetchError


class BaseBuilder:

    service_url = None
    service_port = None
    contract = None

    def __init__(self, *args, **kwargs):
        # generate request response
        request, response = generate_request_response(self.contract)
        self._request_contract = request
        self._response_contract = response
        # build url
        self._url = self.build_url()

    def build_url(self, *args, **kwargs):
        """ method to build right service url!"""
        url = self.service_url
        if self.service_port is not None:
            # if we connect to specific port we need to add it as path to
            url = self.service_url + ":" + self.service_port
        return url
