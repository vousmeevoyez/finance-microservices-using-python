# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from task.investment.rpc.modanaku import plan_pb2 as plan__pb2


class PlanStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreatePlan = channel.unary_unary(
        '/Plan/CreatePlan',
        request_serializer=plan__pb2.CreatePlanRequest.SerializeToString,
        response_deserializer=plan__pb2.CreatePlanResponse.FromString,
        )
    self.GetPlan = channel.unary_unary(
        '/Plan/GetPlan',
        request_serializer=plan__pb2.GetPlanRequest.SerializeToString,
        response_deserializer=plan__pb2.GetPlanResponse.FromString,
        )
    self.GetPlans = channel.unary_unary(
        '/Plan/GetPlans',
        request_serializer=plan__pb2.GetPlansRequest.SerializeToString,
        response_deserializer=plan__pb2.GetPlansResponse.FromString,
        )
    self.UpdatePlan = channel.unary_unary(
        '/Plan/UpdatePlan',
        request_serializer=plan__pb2.UpdatePlanRequest.SerializeToString,
        response_deserializer=plan__pb2.UpdatePlanResponse.FromString,
        )
    self.UpdatePlanStatus = channel.unary_unary(
        '/Plan/UpdatePlanStatus',
        request_serializer=plan__pb2.UpdatePlanStatusRequest.SerializeToString,
        response_deserializer=plan__pb2.UpdatePlanStatusResponse.FromString,
        )
    self.RemovePlan = channel.unary_unary(
        '/Plan/RemovePlan',
        request_serializer=plan__pb2.RemovePlanRequest.SerializeToString,
        response_deserializer=plan__pb2.RemovePlanResponse.FromString,
        )


class PlanServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def CreatePlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPlans(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdatePlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdatePlanStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemovePlan(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PlanServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreatePlan': grpc.unary_unary_rpc_method_handler(
          servicer.CreatePlan,
          request_deserializer=plan__pb2.CreatePlanRequest.FromString,
          response_serializer=plan__pb2.CreatePlanResponse.SerializeToString,
      ),
      'GetPlan': grpc.unary_unary_rpc_method_handler(
          servicer.GetPlan,
          request_deserializer=plan__pb2.GetPlanRequest.FromString,
          response_serializer=plan__pb2.GetPlanResponse.SerializeToString,
      ),
      'GetPlans': grpc.unary_unary_rpc_method_handler(
          servicer.GetPlans,
          request_deserializer=plan__pb2.GetPlansRequest.FromString,
          response_serializer=plan__pb2.GetPlansResponse.SerializeToString,
      ),
      'UpdatePlan': grpc.unary_unary_rpc_method_handler(
          servicer.UpdatePlan,
          request_deserializer=plan__pb2.UpdatePlanRequest.FromString,
          response_serializer=plan__pb2.UpdatePlanResponse.SerializeToString,
      ),
      'UpdatePlanStatus': grpc.unary_unary_rpc_method_handler(
          servicer.UpdatePlanStatus,
          request_deserializer=plan__pb2.UpdatePlanStatusRequest.FromString,
          response_serializer=plan__pb2.UpdatePlanStatusResponse.SerializeToString,
      ),
      'RemovePlan': grpc.unary_unary_rpc_method_handler(
          servicer.RemovePlan,
          request_deserializer=plan__pb2.RemovePlanRequest.FromString,
          response_serializer=plan__pb2.RemovePlanResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Plan', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
