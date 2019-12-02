"""
    Request Factory
    __________________
    factory method to handle request creation
"""
from rpc.lib.core.factory import Factory
from rpc.factories.request.v1.request import BNIOpgAuthRequest, BNIOpgRequest


def generate_request(external_resource):
    """ generate request object """
    factory = Factory()
    factory.register("BNI_AUTH_OPG", BNIOpgAuthRequest)
    factory.register("BNI_OPG", BNIOpgRequest)

    generator = factory.get(external_resource)
    return generator
