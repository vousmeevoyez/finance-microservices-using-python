"""
    gRPC Server
    ___________________
    this is where we register servicer class and start gRPC Server
"""
import time
import grpc

from rpc.lib.core.async_server import AsyncioExecutor

from autogen import (
    virtual_account_pb2_grpc
)

from rpc.handler import VirtualAccount

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def start(host, port):
    """ start Async gRPC Server"""
    server = grpc.server(AsyncioExecutor())
    # register GRPC Servicer here
    virtual_account_pb2_grpc.add_VirtualAccountServicer_to_server(
        VirtualAccount(), server
    )
    # start
    server.add_insecure_port("{}:{}".format(host, port))
    server.start()
    print("Listening gRPC server at {}:{}".format(host, port))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
