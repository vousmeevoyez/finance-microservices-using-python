"""
    Response Factory
    __________________
    factory method to handle request creation
"""
from rpc.lib.core.factory import Factory
from rpc.factories.response.v1.response import BNIRdlAuthResponse, BNIRdlResponse


def generate_response(external_resource):
    """ generate response object """
    factory = Factory()
    factory.register("BNI_AUTH_RDL", BNIRdlAuthResponse)
    factory.register("BNI_RDL", BNIRdlResponse)

    generator = factory.get(external_resource)
    return generator
