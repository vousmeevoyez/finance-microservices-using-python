"""
    Response Factory
    __________________
    factory method to handle request creation
"""
from rpc.lib.core.factory import Factory
from rpc.factories.response.v1.response import BNIOpgAuthResponse, BNIOpgResponse


def generate_response(external_resource):
    """ generate response object """
    factory = Factory()
    factory.register("BNI_AUTH_OPG", BNIOpgAuthResponse)
    factory.register("BNI_OPG", BNIOpgResponse)

    generator = factory.get(external_resource)
    return generator
