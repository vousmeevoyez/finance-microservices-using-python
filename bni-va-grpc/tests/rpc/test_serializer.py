from rpc.serializer import CreateVaSchema
from rpc.models import VirtualAccount


def test_load_virtual_account(setup_flask_app):
    data = {"name": "only name"}
    CreateVaSchema().load(data)
    result = VirtualAccount.objects(name="only name")
    assert result
