"""
    BNI E-Collection Helper
    ________________________
"""
import sys
from datetime import datetime
import functools
import json
import random

from string import Template
import requests

from app.api.lib.BniEnc3 import BniEnc, BNIVADecryptError
from app.api.models.base import BankAccEmbed, StatusEmbed
from app.api.models.batch import Schedule, TransactionQueue
from app.api.models.bank import Bank
from app.api.models.user import User
from app.api.models.borrower import Borrower
from app.api.models.investment import Investment
from app.api.models.investor import Investor
from app.api.models.wallet import Wallet
from app.api.models.loan_request import LoanRequest
from app.api.models.product import Product
from app.api.models.notif import Notification

from app.api.const import NOTIFICATIONS
from app.config.external.investor import INVESTOR_BE

from task.utility.tasks import UtilityTask


class DecryptError(Exception):
    """ error raised to encapsulate decrypt error from BNI """


class RefreshTokenError(Exception):
    """ error raised when push refresh token error """


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


def opg_extract_error(obj):
    """ extract error from BNI OPG Response format """
    error_message = ""
    if isinstance(obj.original_exception, dict):
        for key, value in obj.original_exception.items():
            for key, value in value.items():
                if key == "parameters":
                    for key, value in value.items():
                        if key == "errorMessage":
                            error_message = value
    return error_message


def extract_error(obj):
    try:
        key = obj.original_exception["response"]
    except KeyError:
        error = opg_extract_error(obj)
    except:
        error = obj.message
    return error


@functools.lru_cache(maxsize=128)
def generate_ref_number(destination, amount=None):
    """ generate reference number matched to BNI format"""
    now = datetime.utcnow()
    # first 8 digit is date
    value_date = now.strftime("%Y%m%d%H%M")
    randomize = random.randint(1, 99)

    end_fix = str(destination)[:8]
    if amount is not None:
        end_fix = str(destination)[:4] + str(amount)[:4]

    return str(value_date) + str(end_fix) + str(randomize)


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def send_notif(
    recipient, user_id, notif_type, platform, device_token=None, custom_content=None
):
    email_info = {
        "recipient": recipient,
        "product_type": "MOPINJAM",
        "email_type": notif_type,
    }

    in_app_info = {
        "user_id": user_id,
        "template": {
            "subject": NOTIFICATIONS["SUBJECT"][notif_type],
            "message": NOTIFICATIONS["CONTENT"][platform][notif_type],
        },
        "type_": NOTIFICATIONS["TYPE"][notif_type],
        "platform": platform,
    }

    push_info = {
        "device_token": device_token,
        "product_type": "MOPINJAM",
        "notif_type": notif_type,
    }

    if custom_content is not None:
        template = Template(in_app_info["template"]["message"])
        parsed_template = template.substitute(**custom_content)
        in_app_info["template"]["message"] = parsed_template

        email_info["content"] = custom_content
        push_info["content"] = custom_content

    UtilityTask().send_email.apply_async(kwargs=email_info, queue="utility")

    if platform == "mobile":
        # need to prevent empty device token for being sent here
        if device_token is not None:
            UtilityTask().send_push_notif.apply_async(kwargs=push_info, queue="utility")

    notif = Notification(**in_app_info)
    notif.commit()
    return email_info, in_app_info


def push_refresh_token(user_id):
    url = INVESTOR_BE["BASE_URL"] + INVESTOR_BE["ENDPOINTS"]["REFRESH_TOKEN"]
    try:
        payload = {"uid": str(user_id), "socketioKey": INVESTOR_BE["SOCKETIO_KEY"]}
        r = requests.post(url, payload)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RefreshTokenError()
