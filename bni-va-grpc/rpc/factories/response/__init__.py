"""
    Response Factory
    __________________
    factory method to handle request creation
"""
from rpc.lib.core.factory import Factory
from rpc.factories.response.v1.response import (
    BNICreditEcollectionResponse,
    BNIDebitEcollectionResponse,
)


def generate_response(external_resource):
    """ generate response object """
    factory = Factory()
    factory.register("BNI_CREDIT_VA", BNICreditEcollectionResponse)
    factory.register("BNI_DEBIT_VA", BNIDebitEcollectionResponse)

    generator = factory.get(external_resource)
    return generator
