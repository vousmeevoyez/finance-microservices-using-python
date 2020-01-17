import json
import grpc

from autogen import transfer_pb2_grpc, transfer_pb2

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

from rpc.factories.provider.builder import generate_provider
from rpc.lib.core.provider import ProviderError
from rpc.lib.helper import extract_error


class OpgTransfer(transfer_pb2_grpc.OpgTransferServicer):
    async def Transfer(self, request, context):
        """ handle RPC For transfer via OPG """
        # convert message to dict
        payload = MessageToDict(request, preserving_proto_field_name=True)

        response = transfer_pb2.TransferResponse()
        try:
            # based on request we generate the right provider!
            provider = await generate_provider("BNI_OPG")
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
            provider = await generate_provider("BNI_OPG")
            result = await provider.get_payment_status(request.request_uuid)
        except ProviderError as error:
            message = extract_error(error)
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(message)
        else:
            Parse(json.dumps(result), response)
        return response
