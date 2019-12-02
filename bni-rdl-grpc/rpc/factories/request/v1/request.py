"""
    BNI Opg Request
    __________________
    module to handle HTTP Request BNI Opg
"""
import json
import uuid
import base64
import jwt

from rpc.config import BNI_RDL
from rpc.lib.core.request import HTTPRequest


def generate_bni_uuid():
    """ generate uuid for BNI """
    return str(uuid.uuid4()).replace("-", "").upper()[:16]


class BNIRdlAuthRequest(HTTPRequest):
    """ Request Class for handling BNI RDL Auth """

    username = BNI_RDL["USERNAME"]
    password = BNI_RDL["PASSWORD"]
    secret_key = BNI_RDL["SECRET_API_KEY"]
    client_id = BNI_RDL["CLIENT_NAME"]

    def create_signature(self, payload):
        """ generate jwt signature """
        signature = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return signature.decode("utf-8")

    # end def

    def setup_header(self, *args, **kwargs):
        auth_key = base64.b64encode(
            (self.username + ":" + self.password).encode("utf-8")
        ).decode("utf-8")
        self._header["Authorization"] = "Basic {}".format(str(auth_key))
        self._header["Content-Type"] = "application/x-www-form-urlencoded"

    @property
    def payload(self):
        """ fetch request payload """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """ set payload """
        self._payload = payload


class BNIRdlRequest(BNIRdlAuthRequest):
    """ Request Class for handling BNI OPG """

    api_key = BNI_RDL["API_KEY"]
    company = BNI_RDL["COMPANY"]
    parent_company = BNI_RDL["PARENT_COMPANY"]
    secret_key = BNI_RDL["SECRET_API_KEY"]

    def __init__(self):
        super().__init__()

    def setup_header(self, *args, **kwargs):
        self._header["x-api-key"] = self.api_key
        self._header["Content-Type"] = "application/json"

    @property
    def payload(self):
        """ fetch request payload """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """ set payload """
        # need to wrap it inside request
        request_uuid = generate_bni_uuid()
        if "request_uuid" in payload and payload["request_uuid"] is not None:
            request_uuid = payload["request_uuid"]
        # end def
        payload.pop("request_uuid", None)

        payload = {"request": payload}
        # added header!
        payload["request"]["header"] = {
            "requestUuid": request_uuid,
            "companyId": self.company,
            "parentCompanyId": self.parent_company,
        }
        payload["request"]["header"]["signature"] = self.create_signature(payload)
        self._payload = payload

    def to_representation(self):
        """ represent the request as JSON """
        result = super().to_representation()
        result["data"] = json.dumps(result["data"])
        return result
