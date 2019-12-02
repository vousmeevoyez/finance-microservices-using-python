"""
    FACTORY PACKAGE INIT
    _______________________
"""
from rpc.factories.request import generate_request
from rpc.factories.response import generate_response


def generate_request_response(external_resource):
    """ handle request and response object creation """
    request = generate_request(external_resource)
    response = generate_response(external_resource)
    return request, response
