"""
    BNI E-Collection Provider
    _________________________
    Handle API Execution to BNI E-collection
"""
import pytz
from datetime import datetime

from rpc.const import VA_TYPES
from rpc.config.external import BNI_ECOLLECTION
from rpc.factories import generate_request
from rpc.factories import generate_response
from rpc.serializer import InquiryVaSchema, GeneralVaSchema
from rpc.lib.core.provider import BaseProvider


VA_CONFIG = {
    "CREDIT": {"TYPE": "createbilling", "BILLING_TYPE": "o"},
    "DEBIT": {"TYPE": "createdebitcardless", "BILLING_TYPE": "j"},
}


class BNIVaProvider(BaseProvider):
    """ This is class to interact with BNI E-Collection API"""

    service_url = BNI_ECOLLECTION["BASE_URL"]

    TIMEZONE = pytz.timezone("Asia/Jakarta")

    def __init__(self, *args, **kwargs):
        pass

    def set(self, va_type):
        # convert va_type into known format
        converted_va_type = VA_TYPES[va_type]
        self.va_type = converted_va_type
        request = generate_request(
            f"BNI_{converted_va_type}_VA"
        )  # create request contract according to VA TYPE
        response = generate_response(
            f"BNI_{converted_va_type}_VA"
        )  # create request contract according to VA TYPE
        self._request_contract = request
        self._response_contract = response

    def prepare_request(self, **kwargs):
        """
            extend base prepare_request from BaseProvider so instead passing a url
            we just need to pass api_name
        """
        self.request_contract.url = self.service_url  # it static
        self.request_contract.method = kwargs["method"]
        self.request_contract.payload = kwargs["payload"]

    async def create_va(
        self, trx_id, amount, name, phone_number, account_no, expired_at,
        **ignored
    ):
        """
            Function to Create Virtual Account on BNI
            args:
                params -- payload
        """
        # modify msisdn so match BNI format
        payload = {
            "method": "POST",
            "payload": {
                "type": VA_CONFIG[self.va_type]["TYPE"],
                "trx_id": trx_id,
                "trx_amount": amount,
                "billing_type": VA_CONFIG[self.va_type]["BILLING_TYPE"],
                "customer_name": name,
                "customer_email": "",
                "customer_phone": phone_number,
                "virtual_account": account_no,
                "datetime_expired": expired_at.astimezone(self.TIMEZONE).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            },
        }

        result = await self.execute(**payload)
        response = GeneralVaSchema().dump(result) 
        return response

    async def get_inquiry(self, trx_id, **ignored):
        """
            Function to get Virtual Account Inquiry on BNI
            args:
                resource_type -- CARDLESS/ CREDIT
                params -- payload
        """
        payload = {
            "method": "POST",
            "payload": {"type": BNI_ECOLLECTION["INQUIRY"], "trx_id": trx_id},
        }

        result = await self.execute(**payload)
        response = InquiryVaSchema().dump(result) 
        return response

    async def update_va(self, trx_id, amount, name, expired_at, **ignored):
        """
            Function to update BNI Virtual Account
            args:
                resource_type -- CREDIT/CARDLESS
                params -- payload
        """
        payload = {
            "method": "POST",
            "payload": {
                "type": BNI_ECOLLECTION["UPDATE"],
                "trx_id": trx_id,
                "trx_amount": amount,
                "customer_name": name,
                "datetime_expired": expired_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        }

        result = await self.execute(**payload)
        # convert to known field
        response = GeneralVaSchema().dump(result) 
        return response
