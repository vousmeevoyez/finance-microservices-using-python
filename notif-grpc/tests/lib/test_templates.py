"""
    Testing Template Engine
"""
from rpc.lib.template import TemplateEngine, decode_content, generate_email_template


def test_decode_content(encode_data):
    raw = {"message": "Hello World!"}
    result = decode_content(encode_data(raw))
    assert result == raw


def test_generate_email_template(encode_data):
    result = generate_email_template("MOPINJAM", "INVESTOR_APPROVE")
    assert result
