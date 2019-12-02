import uuid
import random

import grpc
import pytest

from asynctest import CoroutineMock, patch

from autogen import (
    rdl_account_pb2,
    transfer_pb2
)

from rpc.services import RdlAccount, RdlTransfer


@pytest.fixture
def setup_local_client():
    """ fixture to connect grpc client to grpc server """
    #return grpc.insecure_channel("127.0.0.1:5001")
    return grpc.insecure_channel("dev.modana.id:11001")


@pytest.fixture
def generate_dummy_user():
    fixed_npwp = "9999999"
    random_digit = random.randint(1000000, 99999999)
    npwp = fixed_npwp + str(random_digit)

    fixed_ktp = "331234766"
    random_digit = random.randint(1000000, 99999999)
    ktp = fixed_ktp + str(random_digit)
    return ktp, npwp


@pytest.fixture
def generate_fake_uuid():
    """ generate uuid for BNI """
    inquiry_uuid = str(uuid.uuid4()).replace("-", "").upper()[:16]
    trx_uuid = str(uuid.uuid4()).replace("-", "").upper()[:16]
    return inquiry_uuid, trx_uuid
