# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from task.investment.rpc.modanaku import payment_plan_pb2 as payment__plan__pb2


class PaymentPlanStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreatePaymentPlan = channel.unary_unary(
        '/PaymentPlan/CreatePaymentPlan',
        request_serializer=payment__plan__pb2.CreatePaymentPlanRequest.SerializeToString,
        response_deserializer=payment__plan__pb2.CreatePaymentPlanResponse.FromString,
        )
    self.GetPaymentPlan = channel.unary_unary(
        '/PaymentPlan/GetPaymentPlan',
        request_serializer=payment__plan__pb2.GetPaymentPlanRequest.SerializeToString,
        response_deserializer=payment__plan__pb2.GetPaymentPlanResponse.FromString,
        )
    self.GetPaymentPlans = channel.unary_unary(
        '/PaymentPlan/GetPaymentPlans',
        request_serializer=payment__plan__pb2.GetPaymentPlansRequest.SerializeToString,
        response_deserializer=payment__plan__pb2.GetPaymentPlansResponse.FromString,
        )
    self.UpdatePaymentPlan = channel.unary_unary(
        '/PaymentPlan/UpdatePaymentPlan',
        request_serializer=payment__plan__pb2.UpdatePaymentPlanRequest.SerializeToString,
        response_deserializer=payment__plan__pb2.UpdatePaymentPlanResponse.FromString,
        )
    self.RemovePaymentPlan = channel.unary_unary(
        '/PaymentPlan/RemovePaymentPlan',
        request_serializer=payment__plan__pb2.RemovePaymentPlanRequest.SerializeToString,
        response_deserializer=payment__plan__pb2.RemovePaymentPlanResponse.FromString,
        )


class PaymentPlanServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CreatePaymentPlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPaymentPlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPaymentPlans(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdatePaymentPlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemovePaymentPlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PaymentPlanServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreatePaymentPlan': grpc.unary_unary_rpc_method_handler(
          servicer.CreatePaymentPlan,
          request_deserializer=payment__plan__pb2.CreatePaymentPlanRequest.FromString,
          response_serializer=payment__plan__pb2.CreatePaymentPlanResponse.SerializeToString,
      ),
      'GetPaymentPlan': grpc.unary_unary_rpc_method_handler(
          servicer.GetPaymentPlan,
          request_deserializer=payment__plan__pb2.GetPaymentPlanRequest.FromString,
          response_serializer=payment__plan__pb2.GetPaymentPlanResponse.SerializeToString,
      ),
      'GetPaymentPlans': grpc.unary_unary_rpc_method_handler(
          servicer.GetPaymentPlans,
          request_deserializer=payment__plan__pb2.GetPaymentPlansRequest.FromString,
          response_serializer=payment__plan__pb2.GetPaymentPlansResponse.SerializeToString,
      ),
      'UpdatePaymentPlan': grpc.unary_unary_rpc_method_handler(
          servicer.UpdatePaymentPlan,
          request_deserializer=payment__plan__pb2.UpdatePaymentPlanRequest.FromString,
          response_serializer=payment__plan__pb2.UpdatePaymentPlanResponse.SerializeToString,
      ),
      'RemovePaymentPlan': grpc.unary_unary_rpc_method_handler(
          servicer.RemovePaymentPlan,
          request_deserializer=payment__plan__pb2.RemovePaymentPlanRequest.FromString,
          response_serializer=payment__plan__pb2.RemovePaymentPlanResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'PaymentPlan', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))