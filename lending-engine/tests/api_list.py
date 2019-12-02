"""
    Callable API for testing purpose
"""
import json


BASE_URL = "/api/v1"


def va_deposit_callback(client, payload):
    """ api call to get access token """
    return client.post(
        BASE_URL + "/callback/bni/va/deposit",
        data=json.dumps(payload),
        content_type="application/json",
    )


def rdl_deposit_callback(client, payload):
    """ api call to get access token """
    return client.post(
        BASE_URL + "/callback/bni/rdl/deposit",
        data=json.dumps(payload),
        content_type="application/json",
    )


def internal_callback(client, payload):
    """ api call to trigger internal callback update """
    return client.post(
        BASE_URL + "/callback/transaction",
        data=json.dumps(payload),
        content_type="application/json",
    )


def process_invest(client, investment_id):
    """ api call to trigger processinng investment """
    return client.post(
        BASE_URL + "/investment/{}/invest/".format(investment_id),
    )


def approve_investor(client, investor_id):
    """ api call to trigger approve investor """
    return client.post(
        BASE_URL + "/investor/{}/approve/".format(investor_id),
    )


def withdraw_rdl(client, investor_id, payload):
    """ api call to trigger approve investor """
    return client.post(
        BASE_URL + "/investor/{}/withdraw/".format(investor_id),
        data=json.dumps(payload),
        content_type="application/json",
    )
