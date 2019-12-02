from rpc.lib.helper import send_email

def test_send_email(encode_data):
    recipient = "kelvin@modana.id"
    product_type = "MOPINJAM"
    email_type = "INVESTOR_APPROVE"
    #fake_content = encode_data(fake_content)
    status_code = send_email(
        recipient,
        product_type,
        email_type
    )
    assert status_code == 202
