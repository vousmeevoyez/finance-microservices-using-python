# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from autogen import rdl_account_pb2 as autogen_dot_rdl__account__pb2


class RdlAccountStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateRdl = channel.unary_unary(
        '/RdlAccount/CreateRdl',
        request_serializer=autogen_dot_rdl__account__pb2.CreateRdlRequest.SerializeToString,
        response_deserializer=autogen_dot_rdl__account__pb2.CreateRdlResponse.FromString,
        )
    self.GetHistory = channel.unary_unary(
        '/RdlAccount/GetHistory',
        request_serializer=autogen_dot_rdl__account__pb2.GetHistoryRequest.SerializeToString,
        response_deserializer=autogen_dot_rdl__account__pb2.GetHistoryResponse.FromString,
        )


class RdlAccountServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CreateRdl(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetHistory(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RdlAccountServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateRdl': grpc.unary_unary_rpc_method_handler(
          servicer.CreateRdl,
          request_deserializer=autogen_dot_rdl__account__pb2.CreateRdlRequest.FromString,
          response_serializer=autogen_dot_rdl__account__pb2.CreateRdlResponse.SerializeToString,
      ),
      'GetHistory': grpc.unary_unary_rpc_method_handler(
          servicer.GetHistory,
          request_deserializer=autogen_dot_rdl__account__pb2.GetHistoryRequest.FromString,
          response_serializer=autogen_dot_rdl__account__pb2.GetHistoryResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'RdlAccount', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
