import grpc
import pytest
import random
from pymongo import MongoClient


from rpc import create_app
from rpc.models import VirtualAccount
from rpc.config.external import BNI_ECOLLECTION


@pytest.fixture(autouse=True)
def setup_flask_app():
    flask_app = create_app("test")
    ctx = flask_app.app_context()
    ctx.push()
    yield flask_app
    # drop collection on tear down
    client = MongoClient(flask_app.config["MONGO_URI"])
    client.drop_database("db_virtual_account_test")
    ctx.pop()


@pytest.fixture
def setup_local_client():
    """ fixture to connect grpc client to grpc server """
    #return grpc.insecure_channel("127.0.0.1:5001")
    return grpc.insecure_channel("127.0.0.1:11000")
    #return grpc.insecure_channel("dev.modana.id:11000")


@pytest.fixture
def setup_dummy_va_trx_id():
    trx_id = random.randint(100000000, 999999999)
    return str(trx_id)


@pytest.fixture
def setup_dummy_va(setup_dummy_va_trx_id):
    fixed = BNI_ECOLLECTION["VA_PREFIX"]
    client_id = BNI_ECOLLECTION["CREDIT_CLIENT_ID"]
    length = BNI_ECOLLECTION["VA_LENGTH"]

    # calculate fixed length first
    prefix = len(fixed) + len(client_id)
    # calulcate free number
    random_length = length - prefix
    # generate 00000000 + 1
    zeroes = "0" * (int(random_length) - 1)
    start_point = int("1" + zeroes)
    # generate 999999999999
    end_point = int("9" * random_length)
    # generate random number between
    suffix = random.randint(start_point, end_point)
    account_no = str(fixed) + str(client_id) + str(suffix)
    return account_no, setup_dummy_va_trx_id


@pytest.fixture
def setup_va_object():
    va = VirtualAccount(name="Kelvin")
    va.generate_trx_id()
    va.generate_va_number()
    va.save()
    return va
