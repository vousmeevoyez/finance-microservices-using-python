import json
import grpc

from autogen import (
    rdl_account_pb2_grpc,
    rdl_account_pb2,
    transfer_pb2_grpc,
    transfer_pb2,
)

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

from rpc.factories.provider.builder import generate_provider
from rpc.serializer import RdlAccountSchema
from rpc.lib.core.provider import ProviderError
from rpc.lib.helper import extract_error


class RdlAccount(rdl_account_pb2_grpc.RdlAccountServicer):
    async def CreateRdl(self, request, context):
        """ handle RPC For creating RDL """
        # convert message to dict
        payload = MessageToDict(request, preserving_proto_field_name=True)
        serialized_payload = RdlAccountSchema().load(payload)

        response = rdl_account_pb2.CreateRdlResponse()
        try:
            # based on request we generate the right provider!
            provider = await generate_provider("BNI_RDL")
            result = await provider.create_rdl(**serialized_payload)
        except ProviderError as error:
            message = extract_error(error)
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(message)
        else:
            Parse(json.dumps(result), response)
        return response

    async def GetHistory(self, request, context):
        """ handle RPC For getting RDL history """
        response = rdl_account_pb2.GetHistoryResponse()
        try:
            # based on request we generate the right provider!
            provider = await generate_provider("BNI_RDL")
            result = await provider.inquiry_account_history(request.account_no)
        except ProviderError as error:
            message = extract_error(error)
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(message)
        else:
            Parse(json.dumps(result), response)
        return response


class RdlTransfer(transfer_pb2_grpc.RdlTransferServicer):
    async def Transfer(self, request, context):
        """ handle RPC For transfer via RDL """
        # convert message to dict
        payload = MessageToDict(request, preserving_proto_field_name=True)

        response = transfer_pb2.TransferResponse()
        try:
            # based on request we generate the right provider!
            provider = await generate_provider("BNI_RDL")
            result = await provider.transfer(**payload)
        except ProviderError as error:
            message = extract_error(error)
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(message)
        else:
            Parse(json.dumps(result), response)
        return response

    async def TransferInquiry(self, request, context):
        """ handle RPC For transfer inquiry via RDL """
        response = transfer_pb2.TransferInquiryResponse()
        try:
            # based on request we generate the right provider!
            provider = await generate_provider("BNI_RDL")
            result = await provider.inquiry_payment_status(request.request_uuid)
        except ProviderError as error:
            message = extract_error(error)
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(message)
        else:
            Parse(json.dumps(result), response)
        return response
