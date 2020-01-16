"""
    Callback Routes
    ______________________
    this module that receive http request from callback url
"""
from flask import current_app

# api
from app.api.lib.core.routes import Routes
from app.api.callback import api

# serializer
from app.api.serializer import (
    BniVaCallbackSchema,
    BniRdlCallbackSchema,
    TransactionCallbackSchema,
)

# services
from app.api.callback.modules.services import top_up_rdl, top_up_va, update_transaction

from app.api.lib.helper import decrypt, DecryptError

# error
from app.api.lib.core.http_error import BadRequest

# configuration
from app.config.external.bank import BNI_ECOLLECTION
from app.config.external.bank import BNI_RDL
from app.api.lib.core.message import RESPONSE as error_response


class Callback(Routes):
    """
        Base Callback
    """

    client_id = None
    secret_key = None
    traffic_type = None

    __serializer__ = None

    def preprocess(self, payload):
        try:
            payload = decrypt(self.client_id, self.secret_key, payload["data"])
        except DecryptError:
            # raise error
            raise BadRequest(
                error_response["INVALID_CALLBACK"]["TITLE"],
                error_response["INVALID_CALLBACK"]["MESSAGE"],
            )
        return payload


@api.route("/bni/rdl/deposit")
class BNIRdlDepositCallback(Callback):
    """
        BNI RDL Deposit Callback
        /bni/rdl/deposit
    """

    client_id = BNI_RDL["COMPANY"]
    secret_key = BNI_RDL["CALLBACK_SECRET_KEY"]

    __serializer__ = BniRdlCallbackSchema(strict=True)

    def post(self):
        """ execute BNI Rdl Top up via services """
        request_data = self.serialize(self.payload(raw=True), load=True)

        current_app.logger.info("Request: {}".format(request_data))
        response = top_up_rdl(
            rdl_account=request_data["account_number"],
            amount=request_data["payment_amount"],
            journal_no=request_data["journal_number"],
        )
        return response


@api.route("/bni/va/deposit")
class BNIVaDepositCallback(Callback):
    """
        Callback
        /bni/va/deposit
    """

    client_id = BNI_ECOLLECTION["CREDIT_CLIENT_ID"]
    secret_key = BNI_ECOLLECTION["CREDIT_SECRET_KEY"]

    __serializer__ = BniVaCallbackSchema(strict=True)

    def post(self):
        """ execute BNI Rdl Top up via services """
        request_data = self.serialize(self.payload(raw=True), load=True)

        current_app.logger.info("Request: {}".format(request_data))
        response = top_up_va(
            account_no=request_data["virtual_account"],
            amount=request_data["trx_amount"],
            payment_ntb=request_data["payment_ntb"],
            va_type=request_data["va_type"],
        )
        return response


@api.route("/transaction")
class TransactionCallback(Routes):
    """
        Transaction Callback
        /transaction/
    """

    __serializer__ = TransactionCallbackSchema(strict=True)

    def post(self):
        """ execute BNI Rdl Top up via services """
        request_data = self.serialize(self.payload(raw=True))
        response = update_transaction(**request_data)
        return response
