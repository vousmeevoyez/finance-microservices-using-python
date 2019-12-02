"""
    gRPC Server
    ___________________
    this is where we register servicer class and start gRPC Server
"""
import time
import grpc

from autogen import rdl_account_pb2_grpc, transfer_pb2_grpc

from rpc.lib.core.async_server import AsyncioExecutor
from rpc.services import RdlAccount, RdlTransfer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def start(host, port):
    """ start Async gRPC Server"""
    server = grpc.server(AsyncioExecutor())
    # register GRPC Servicer here
    rdl_account_pb2_grpc.add_RdlAccountServicer_to_server(RdlAccount(), server)
    transfer_pb2_grpc.add_RdlTransferServicer_to_server(RdlTransfer(), server)
    # start
    server.add_insecure_port("{}:{}".format(host, port))
    server.start()
    print("Listening gRPC server at {}:{}".format(host, port))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    start()
