"""
    Request Factory
    __________________
    factory method to handle request creation
"""
from rpc.lib.core.factory import Factory
from rpc.factories.request.v1.request import BNIRdlAuthRequest, BNIRdlRequest


def generate_request(external_resource):
    """ generate request object """
    factory = Factory()
    factory.register("BNI_AUTH_RDL", BNIRdlAuthRequest)
    factory.register("BNI_RDL", BNIRdlRequest)

    generator = factory.get(external_resource)
    return generator
