import pytest
import grpc

from autogen import virtual_account_pb2, virtual_account_pb2_grpc

from google.protobuf.json_format import Parse


def test_create_va(setup_local_client):
    stub = virtual_account_pb2_grpc.VirtualAccountStub(setup_local_client)
    request = virtual_account_pb2.CreateVaRequest()

    request.va_type = "CREDIT"
    request.name = "my cool"
    request.phone_number = "62812341259"

    response = stub.CreateVa(request)
    print(response)


def test_inquiry_va(setup_local_client, setup_dummy_va):
    stub = virtual_account_pb2_grpc.VirtualAccountStub(setup_local_client)
    request = virtual_account_pb2.InquiryVaRequest()
    account_no, trx_id = setup_dummy_va

    request.va_type = "CREDIT"
    request.account_no = account_no

    response = stub.InquiryVa(request)
    print(response)


def test_update_va(setup_local_client, setup_dummy_va):
    stub = virtual_account_pb2_grpc.VirtualAccountStub(setup_local_client)
    request = virtual_account_pb2.UpdateVaRequest()

    account_no, trx_id = setup_dummy_va

    request.va_type = "CREDIT"
    request.account_no = account_no
    request.amount = 0
    request.name = "Kelvin Desman"
    request.expired_at = "2019-12-12"

    response = stub.UpdateVa(request)
    print(response)
