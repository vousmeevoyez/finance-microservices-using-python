"""
    Callable API for testing purpose
"""

BASE_URL = "/api/v1"


def create_transaction(client, payload):
    """ api call to reate single transaction """
    return client.post(
        BASE_URL + "/transaction/",
        data=payload
    )


def create_bulk_transaction(client, payload):
    """ api call to create bulk transaction """
    return client.post(
        BASE_URL + "/transaction/bulk",
        json=payload
    )
