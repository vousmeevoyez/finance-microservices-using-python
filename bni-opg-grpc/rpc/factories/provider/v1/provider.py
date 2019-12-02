"""
    BNI OPG Provider
    _________________
    handle request response communication with BNI OPG and provide various interface based on BNI Documentation
"""
import random
from datetime import datetime
import functools

from expiringdict import ExpiringDict

from rpc.config import BNI_OPG

from rpc.serializer import TransferInquirySchema
from rpc.lib.core.provider import (
    BaseProvider
)

def ref_number(actual_func):
    """ decorator func to help generate ref_number if its missing """
    @functools.lru_cache(maxsize=128)
    async def generate_ref_number(*args, **kwargs):
        # if ref number is not supplied, we auto generate it!
        now = datetime.utcnow()
        if kwargs["ref_number"] is None:
            # first 8 digit is date
            value_date = now.strftime("%Y%m%d%H%M")
            randomize = random.randint(1, 99)

            destination = kwargs["destination"]
            amount = kwargs.get("amount")
            end_fix = str(destination)[:8]
            if amount is not None:
                end_fix = str(destination)[:4] + str(amount)[:4]
            # end if
            ref_number = str(value_date) + str(end_fix) + str(randomize)
            kwargs["ref_number"] = ref_number
        # end if
        return await actual_func(*args, **kwargs)
    return generate_ref_number


class BNIOpgProvider(BaseProvider):
    """ Class that provide various BNI OPG Interface """

    service_url = BNI_OPG["BASE_URL"]
    service_port = BNI_OPG["PORT"]
    contract = "BNI_OPG"

    def __init__(self, access_token):
        super().__init__()
        self.access_token = access_token

    def api_name_to_full_url(self, api_name):
        """ convert API name into right full url """
        full_url = self.url + BNI_OPG["ROUTES"][api_name]
        full_url = full_url + "?access_token={}".format(self.access_token)
        return full_url

    def prepare_request(self, **kwargs):
        """
            extend base prepare_request from BaseProvider so instead passing a url
            we just need to pass api_name
        """
        self.request_contract.url = self.api_name_to_full_url(
            kwargs["api_name"]
        )
        self.request_contract.method = kwargs["method"]
        self.request_contract.payload = kwargs["payload"]
        return self.request_contract

    async def get_balance(self, account_no):
        """
            Function to check bank account balance using BNI provider
            args :
                params -- account_no
        """
        # payload
        payload = {
            "api_name": "GET_BALANCE",
            "method": "POST",
            "payload": {
                "accountNo": account_no
            }
        }

        post_resp = await self.execute(**payload)

        # access the data here
        response_data = post_resp["getBalanceResponse"]["parameters"]

        response = {
            "customer_name": response_data["customerName"],
            "balance": response_data["accountBalance"],
        }
        return response

    async def get_inhouse_inquiry(self, account_no):
        """
            function to call check Account inquiry that stored in BNI
            args :
                params -- account_no // BNI account number
        """
        # payload
        payload = {
            "api_name": "GET_INHOUSE_INQUIRY",
            "method": "POST",
            "payload": {
                "accountNo": account_no
            }
        }

        post_resp = await self.execute(**payload)

        # access the data here
        response_data = post_resp["getInHouseInquiryResponse"]["parameters"]

        # put conditional here, if account currency is missing it means a VA
        try:
            currency = response_data["accountCurrency"]
            acc_type = "BANK_ACCOUNT"
        except KeyError:
            acc_type = "VIRTUAL_ACCOUNT"
        # end try

        response = {
            "account_no": response_data["accountNumber"],
            "customer_name": response_data["customerName"],
            "status": response_data["accountStatus"],
            "account_type": response_data["accountType"],
            "type": acc_type,  # BANK // VA
        }
        return response

    # end def

    @ref_number
    async def do_payment(self, source, destination, amount,
                         ref_number=None, method="0", email="",
                         clearing_code="", account_name="", address="",
                         charge_mode="", notes="?"):
        """
            function to do interbank payment
            using LLG / Clearing Method
            args :
                params -- parameter
        """
        api_name = "DO_PAYMENT"

        # build payload here
        now = datetime.utcnow()
        value_date = now.strftime("%Y%m%d%H%M%S")
        currency = "IDR"

        payload = {
            "api_name": "DO_PAYMENT",
            "method": "POST",
            "payload": {
                "customerReferenceNumber": ref_number,
                "paymentMethod": method,  # 0 IN_HOUSE // 1 RTGS // 3 CLEARING
                "debitAccountNo": source,  # registered BNI account
                "creditAccountNo": destination,  # destination BNI / EXTERNAL BANK
                "valueDate": value_date,  # yyyyMMddHHmmss
                "valueCurrency": currency,  # IDR
                "valueAmount": int(amount),
                "remark": notes,
                "beneficiaryEmailAddress": email,  # must be filled if not IN_HOUSE
                "destinationBankCode": clearing_code,  # must be filled if not IN_HOUSE
                "beneficiaryName": account_name,  # must be filled if not IN_HOUSE
                "beneficiaryAddress1": address,
                "beneficiaryAddress2": "",
                "chargingModelId": charge_mode,  # whos pay for it (OUR/BEN/SHA)
            }
        }

        post_resp = await self.execute(**payload)

        # access the data here
        response_data = post_resp["doPaymentResponse"]["parameters"]

        response = {
            "source": response_data["debitAccountNo"],
            "destination": response_data["creditAccountNo"],
            "amount": response_data["valueAmount"],
            "uuid": response_data["customerReference"]
        }
        return response

    # end def

    async def get_payment_status(self, request_ref):
        """
            function to check payment status from DO_PAYMENT
            args:
                params -- parameter
        """
        # build payload here
        payload = {
            "api_name": "GET_PAYMENT_STATUS",
            "method": "POST",
            "payload": {
                "customerReferenceNumber": request_ref
            }
        }

        post_resp = await self.execute(**payload)

        # accessing the inner data
        response_data = post_resp["getPaymentStatusResponse"]["parameters"][
            "previousResponse"
        ]
        response = TransferInquirySchema().dump(response_data)
        return response
    # end def

    async def transfer(self, source, destination, bank_code,
                       amount, notes=None, inquiry_uuid=None,
                       transfer_uuid=None):
        """
            function that wrap interbank inquiry do_payment and interbank payment
            args :
                params -- parameter
        """
        response = {}
        # if bank code is BNI then use do_payment
        if bank_code == "009":
            inhouse_response = await self.do_payment(
                source=source, destination=destination, amount=amount,
                ref_number=transfer_uuid
            )
            response["response_uuid"] = inhouse_response["uuid"]
        else:
            interbank_response = await self.get_interbank_inquiry(
                source=source, destination=destination,
                bank_code=bank_code, ref_number=inquiry_uuid
            )
            interbank_response.pop("uuid")
            interbank_response["amount"] = amount
            interbank_response["bank_code"] = bank_code

            interbank_payment_response = await self.interbank_payment(**interbank_response)
            response["response_uuid"] = interbank_payment_response["uuid"]
        return response

    @ref_number
    async def get_interbank_inquiry(self, source, bank_code, destination,
                                    ref_number=None):
        """
            function to check inquiry OUTSIDE BNI like BCA, etc...
            args :
                params -- parameter
        """
        # build payload here
        payload = {
            "api_name": "GET_INTERBANK_INQUIRY",
            "method": "POST",
            "payload": {
                "customerReferenceNumber": ref_number,
                "accountNum": source,
                "destinationBankCode": bank_code,
                "destinationAccountNum": destination
            }
        }

        # post here
        post_resp = await self.execute(**payload)

        # access the data here
        response_data = post_resp["getInterbankInquiryResponse"]["parameters"]
        response = {
            "destination": response_data["destinationAccountNum"],
            "destination_name": response_data["destinationAccountName"],
            "bank_name": response_data["destinationBankName"],
            "transfer_ref": response_data["retrievalReffNum"], # IMPORTANT!
            "uuid": ref_number
        }
        return response

    # end def

    @ref_number
    async def interbank_payment(self, source, destination, destination_name,
                                bank_code, bank_name, amount, transfer_ref,
                                ref_number=None):
        """
            function to transfer to external bank like bca, mandiri, etc..
            args :
                params -- parameter
        """
        # build payload here
        payload = {
            "api_name": "GET_INTERBANK_PAYMENT",
            "method": "POST",
            "payload": {
                "customerReferenceNumber": ref_number,
                "amount": amount,
                "destinationAccountNum": destination,
                "destinationAccountName": destination_name,
                "destinationBankCode": bank_code,
                "destinationBankName": bank_name,
                "accountNum": source,
                "retrievalReffNum": transfer_ref,
            }
        }

        # should log request and response
        post_resp = await self.execute(**payload)

        # access the data here
        response_data = post_resp["getInterbankPaymentResponse"]["parameters"]

        response = {
            "destination": response_data["destinationAccountNum"],
            "destination_name": response_data["destinationAccountName"],
            "uuid": response_data["customerReffNum"]
        }
        return response


class BNIOpgProviderBuilder(BaseProvider):
    """ responsible for initializing BNI OPG Provider """

    service_url = BNI_OPG["BASE_URL"]
    service_port = BNI_OPG["PORT"]
    contract = "BNI_AUTH_OPG"
    cache = ExpiringDict(max_len=1, max_age_seconds=3600)

    def __init__(self):
        super().__init__()
        self._instance = None

    async def __call__(self):
        if not self._instance:
            access_token = await self.authorize()
            self._instance = BNIOpgProvider(access_token)
        return self._instance

    def api_name_to_full_url(self, api_name):
        full_url = self.url + BNI_OPG["ROUTES"][api_name]
        return full_url

    def prepare_request(self, **kwargs):
        self.request_contract.url = self.api_name_to_full_url(
            kwargs["api_name"]
        )
        self.request_contract.method = kwargs["method"]
        self.request_contract.payload = kwargs["payload"]
        return self.request_contract

    async def authorize(self):
        payload = {
            "api_name": "GET_TOKEN",
            "method": "POST",
            "payload": {"grant_type": "client_credentials"}
        }

        try:
            access_token = self.cache["access_token"]
        except KeyError:
            response = await self.execute(**payload)
            access_token = response["access_token"]
            self.cache["access_token"] = access_token
        # end try
        return access_token
