import grpc
import json

from marshmallow import ValidationError

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

from autogen import virtual_account_pb2_grpc
from autogen import virtual_account_pb2

from rpc.serializer import (
    CreateVaSchema, UpdateVaSchema
)
from rpc.services import BNIVaServices
from rpc.services import ServicesError


class VirtualAccount(virtual_account_pb2_grpc.VirtualAccountServicer):

    async def CreateVa(self, request, context):
        """ handle RPC For creating VA """
        # initialize response
        response = virtual_account_pb2.CreateVaResponse()

        # convert message to dict
        payload = MessageToDict(request, preserving_proto_field_name=True)
        # serialized using marshmallow
        try:
            serialized_payload = CreateVaSchema().load(payload)
        except ValidationError as error:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(error.messages)

        # execute actual logic through services
        try:
            services_result = await BNIVaServices(
                request.va_type
            ).create_va(serialized_payload)
        except ServicesError as error:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(error.original_exception)
        else:
            Parse(json.dumps(services_result), response)
        return response

    async def InquiryVa(self, request, context):
        """ handle RPC for get va information """
        response = virtual_account_pb2.InquiryVaResponse()
        try:
            result = await BNIVaServices(
                request.va_type, request.account_no
            ).inquiry_va()
        except ServicesError as error:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(error.original_exception)
        else:
            Parse(json.dumps(result), response)
        return response

    async def UpdateVa(self, request, context):
        """ handle RPC for updating va information """
        # init response
        response = virtual_account_pb2.UpdateVaResponse()

        payload = MessageToDict(request, preserving_proto_field_name=True)
        try:
            serialized_payload = UpdateVaSchema().load(payload)
        except ValidationError as error:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(error.messages)

        try:
            result = await BNIVaServices(
                request.va_type, request.account_no
            ).update_va(serialized_payload)
        except ServicesError as error:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(error.original_exception)
        else:
            Parse(json.dumps(result), response)
        return response

    async def DisableVa(self, request, context):
        """ handle RPC for disabling va """
        response = virtual_account_pb2.DisableVaResponse()

        try:
            result = await BNIVaServices(
                request.va_type, request.account_no
            ).disable_va()
        except ServicesError as error:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(error.original_exception)
        else:
            Parse(json.dumps(result), response)
        return response
