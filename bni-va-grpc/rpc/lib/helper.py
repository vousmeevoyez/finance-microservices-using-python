"""
    BNI E-Collection Helper
    ________________________
"""
import json

from rpc.lib.BniEnc3 import BniEnc, BNIVADecryptError


class DecryptError(Exception):
    """ error raised to encapsulate decrypt error from BNI """


def encrypt(client_id, secret_key, data):
    """ encrypt data using BNI Client ID + Secret + data """
    return BniEnc().encrypt(json.dumps(data), client_id, secret_key).decode("utf-8")


def decrypt(client_id, secret_key, data):
    """ decrypt data using BNI Client ID + Secret + data """
    try:
        decrypted_data = BniEnc().decrypt(data, client_id, secret_key)
        return json.loads(decrypted_data)
    except BNIVADecryptError:
        raise DecryptError


def extract_error(obj):
    try:
        key = obj.original_exception["response"]
    except:
        error = obj.message
    return error
