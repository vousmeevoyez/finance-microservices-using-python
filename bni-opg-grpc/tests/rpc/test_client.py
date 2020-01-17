import pytest
import grpc

from autogen import transfer_pb2, transfer_pb2_grpc


def test_transfer_inhouse(setup_local_client):
    stub = transfer_pb2_grpc.OpgTransferStub(setup_local_client)
    request = transfer_pb2.TransferRequest()
    request.source = "0115476117"
    request.destination = "1571491843"
    request.amount = 100
    request.bank_code = "009"

    try:
        response = stub.Transfer(request)
    except grpc.RpcError as error:
        print(error.code())
        print(error.details())
    print(response)


def test_transfer_interbank(setup_local_client):
    stub = transfer_pb2_grpc.OpgTransferStub(setup_local_client)
    request = transfer_pb2.TransferRequest()
    request.source = "0115476117"
    request.destination = "3333333333"
    request.amount = 100
    request.bank_code = "014"

    try:
        response = stub.Transfer(request)
    except grpc.RpcError as error:
        print(error.code())
        print(error.details())
    print(response)


def test_inquiry_transfer(setup_local_client):
    stub = transfer_pb2_grpc.OpgTransferStub(setup_local_client)
    request = transfer_pb2.TransferInquiryRequest()
    request.request_uuid = "2019101913351571100086"

    try:
        response = stub.TransferInquiry(request)
    except grpc.RpcError as error:
        print(error.code())
        print(error.details())
    print(response)
