"""
    Callable API for testing purpose
"""
import json


BASE_URL = "/api/v1"


def create_transaction(client, payload):
    """ api call to get access token """
    return client.post(
        BASE_URL + "/transaction/",
        data=payload
    )
