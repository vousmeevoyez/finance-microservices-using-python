from rpc.lib.helper import encrypt, decrypt
from rpc.config.external import BNI_ECOLLECTION


def test_encrypt_decrypt():
    payload = {
        "type": "createbilling",
        "trx_id": "41980682",
        "trx_amount": "100000",
        "billing_type": "d",
        "customer_name": "BL652M",
        "customer_email": "",
        "customer_phone": "628797655047",
        "virtual_account": "9889909667037879",
        "datetime_expired": "2019-09-12 11:45:07",
    }
    result = encrypt(
        BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        BNI_ECOLLECTION["CREDIT_SECRET_KEY"],
        payload,
    )

    result = decrypt(
        BNI_ECOLLECTION["CREDIT_CLIENT_ID"],
        BNI_ECOLLECTION["CREDIT_SECRET_KEY"],
        result,
    )
    assert result == payload
