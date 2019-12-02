"""
    Factory modules that responsible for creating right gRPC message
"""
import grpc

from app.api.lib.core.factory import Factory
from app.config.worker import RPC

# MESSAGE DEFINITION
from task.external.factories.message.transfer_pb2 import TransferRequest

# RPC
from task.external.factories.grpc.bni_opg.transfer_pb2_grpc import OpgTransferStub
from task.external.factories.grpc.bni_rdl.transfer_pb2_grpc import RdlTransferStub


def generate_message(provider):
    """ based on provider that passed, we return the right message for each
    provider """
    factory = Factory()
    factory.register("BNI_OPG", TransferRequest)
    factory.register("BNI_RDL", TransferRequest)
    return factory.get(provider)


def generate_stub(provider):
    """ based on provider that passed, we return the right stub for each
    provider """
    factory = Factory()
    factory.register("BNI_OPG", OpgTransferStub)
    factory.register("BNI_RDL", RdlTransferStub)
    # establish channel connection via gRPC
    channel = grpc.insecure_channel(RPC[provider])
    return factory.get(provider, channel)
