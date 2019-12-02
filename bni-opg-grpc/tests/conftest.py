import uuid
import random

import grpc
import pytest


@pytest.fixture
def setup_local_client():
    """ fixture to connect grpc client to grpc server """
    #return grpc.insecure_channel("127.0.0.1:5001")
    #return grpc.insecure_channel("127.0.0.1:11000")
    return grpc.insecure_channel("dev.modana.id:11002")
