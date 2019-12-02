"""
    Request Factory
    __________________
    factory method to handle request creation
"""
from rpc.lib.core.factory import Factory
from rpc.factories.request.v1.request import (
    BNICreditEcollectionRequest,
    BNIDebitEcollectionRequest,
)


def generate_request(external_resource):
    """ generate request object """
    factory = Factory()
    factory.register("BNI_CREDIT_VA", BNICreditEcollectionRequest)
    factory.register("BNI_DEBIT_VA", BNIDebitEcollectionRequest)

    generator = factory.get(external_resource)
    return generator
