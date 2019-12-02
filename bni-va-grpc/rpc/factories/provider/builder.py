from rpc.lib.core.factory import Factory
from rpc.factories.provider.v1.provider import BNIVaProvider


def generate_provider(external_resource):
    """ generate provider object """
    factory = Factory()
    factory.register("BNI_VA", BNIVaProvider)

    service = factory.get(external_resource)
    return service
