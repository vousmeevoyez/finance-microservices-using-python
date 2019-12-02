import pytest
import grpc

from autogen import (
    rdl_account_pb2,
    rdl_account_pb2_grpc,
    transfer_pb2,
    transfer_pb2_grpc,
)

def test_create_rdl(setup_local_client, generate_dummy_user):
    stub = rdl_account_pb2_grpc.RdlAccountStub(setup_local_client)
    request = rdl_account_pb2.CreateRdlRequest()

    ktp, npwp_no = generate_dummy_user

    request.title = "01"
    request.first_name = "Juan"
    request.middle_name = ""
    request.last_name = "Daniel"
    request.npwp_option = "1"
    request.npwp_no = npwp_no
    request.nationality = "ID"
    request.country = "ID"
    request.religion = "2"
    request.birth_place = "Semarang"
    request.birth_date = "26111980"
    request.gender = "M"
    request.is_married = "L"
    request.mother_maiden_name = "Dina Maryati"
    request.job_code = "01"
    request.education = "07"
    request.id_number = ktp
    request.id_issuing_city = "Jakarta Barat"
    request.id_expire_date = "26102099"
    request.address_street = "Jalan Mawar Melati"
    request.address_rt_rw_perum = "003009Sentosa"
    request.address_kelurahan = "Cengkareng Barat"
    request.address_kecamatan = "Cengkareng/Jakarta Barat"
    request.zip_code = "11730"
    request.home_phone_ext = "021"
    request.home_phone = "745454545"
    request.office_phone_ext = ""
    request.office_phone = ""
    request.mobile_phone_ext = "0812"
    request.mobile_phone = "323232"
    request.fax_ext = ""
    request.fax = ""
    request.email = "juan.daniel@gmail.com"
    request.monthly_income = "8000000"
    request.branch_opening = "0259"
    request.reason = "2"
    request.source_of_fund = "4"

    try:
        response = stub.CreateRdl(request)
    except grpc.RpcError as error:
        print(error.code())
        print(error.details())
    print(response)


def test_transfer_inhouse(setup_local_client, generate_fake_uuid):
    inquiry_uuid, transfer_uuid = generate_fake_uuid

    stub = transfer_pb2_grpc.RdlTransferStub(setup_local_client)
    request = transfer_pb2.TransferRequest()
    request.source = "0317246673"
    request.destination = "0115471119"
    request.amount = 100
    request.bank_code = "009"
    request.transfer_uuid = transfer_uuid

    try:
        response = stub.Transfer(request)
    except grpc.RpcError as error:
        print(error.code())
        print(error.details())
    print(response)


def test_transfer_interbank(setup_local_client, generate_fake_uuid):
    inquiry_uuid, transfer_uuid = generate_fake_uuid

    stub = transfer_pb2_grpc.RdlTransferStub(setup_local_client)
    request = transfer_pb2.TransferRequest()
    request.source = "0317246673"
    request.destination = "11223344"
    request.amount = 100
    request.bank_code = "542"
    request.inquiry_uuid = inquiry_uuid
    request.transfer_uuid = transfer_uuid

    try:
        response = stub.Transfer(request)
    except grpc.RpcError as error:
        print(error.code())
        print(error.details())


def test_inquiry_transfer(setup_local_client):
    stub = transfer_pb2_grpc.RdlTransferStub(setup_local_client)
    request = transfer_pb2.TransferInquiryRequest()
    request.request_uuid = "13C4CC6A6B4843B6"

    try:
        response = stub.TransferInquiry(request)
    except grpc.RpcError as error:
        print(error.code())
        print(error.details())
    print(response)
