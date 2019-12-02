"""
    BNI Bank Helper
    _________________
    this is module to interact with BNI RDL
"""

from datetime import datetime
from expiringdict import ExpiringDict

from rpc.config import BNI_RDL

from rpc.lib.core.provider import BaseProvider

from rpc.serializer import RdlAccountHistorySchema, TransferInquirySchema


class BNIRdlProvider(BaseProvider):
    """ This is class that handle interaction to BNI RDL API"""

    service_url = BNI_RDL["BASE_URL"]
    service_port = BNI_RDL["PORT"]
    contract = "BNI_RDL"

    def __init__(self, access_token):
        super().__init__()
        self.access_token = access_token

    def api_name_to_full_url(self, api_name):
        full_url = self.url + BNI_RDL["ROUTES"][api_name]
        full_url = full_url + "?access_token={}".format(self.access_token)
        return full_url

    def prepare_request(self, **kwargs):
        self.request_contract.url = self.api_name_to_full_url(kwargs["api_name"])
        self.request_contract.method = kwargs["method"]
        self.request_contract.payload = kwargs["payload"]
        return self.request_contract

    def generate_ref_number(self):
        """ generate reference number matched to BNI format"""
        now = datetime.utcnow()
        value_date = now.strftime("%Y%m%d%H%M%S")
        code = random.randint(1, 99999)
        return str(value_date) + str(code)

    async def create_investor(
        self,
        title,
        first_name,
        middle_name,
        last_name,
        npwp_option,
        npwp_no,
        nationality,
        country,
        religion,
        birth_place,
        birth_date,
        gender,
        is_married,
        mother_maiden_name,
        job_code,
        education,
        id_number,
        id_issuing_city,
        id_expire_date,
        address_street,
        address_rt_rw_perum,
        address_kelurahan,
        address_kecamatan,
        zip_code,
        home_phone_ext,
        home_phone,
        office_phone_ext,
        office_phone,
        mobile_phone_ext,
        mobile_phone,
        fax_ext,
        fax,
        email,
        monthly_income,
        branch_opening,
    ):
        """
            Function to register investor using BNI provider
            args :
        """
        # payload
        payload = {
            "api_name": "REGIST_INVESTOR",
            "method": "POST",
            "payload": {
                "title": title,
                "firstName": first_name,
                "middleName": middle_name,
                "lastName": last_name,
                "optNPWP": npwp_option,
                "NPWPNum": npwp_no,
                "nationality": nationality,
                "domicileCountry": country,
                "religion": religion,
                "birthPlace": birth_place,
                "birthDate": birth_date,
                "gender": gender,
                "isMarried": is_married,
                "motherMaidenName": mother_maiden_name,
                "jobCode": job_code,
                "education": education,
                "idNumber": id_number,
                "idIssuingCity": id_issuing_city,
                "idExpiryDate": id_expire_date,
                "addressStreet": address_street,
                "addressRtRwPerum": address_rt_rw_perum,
                "addressKel": address_kelurahan,
                "addressKec": address_kecamatan,
                "zipCode": zip_code,
                "homePhone1": home_phone_ext,
                "homePhone2": home_phone,
                "officePhone1": office_phone_ext,
                "officePhone2": office_phone,
                "mobilePhone1": mobile_phone_ext,
                "mobilePhone2": mobile_phone,
                "faxNum1": fax_ext,
                "faxNum2": fax,
                "email": email,
                "monthlyIncome": monthly_income,
                "branchOpening": branch_opening,
            },
        }

        provider_response = await self.execute(**payload)

        response = {
            "customer_name": provider_response["customerName"],
            "journal_no": provider_response["journalNum"],
            "cif_number": provider_response["cifNumber"],
            "mobile_phone": provider_response["mobilePhone"],
            "branch_opening": provider_response["branchOpening"],
            "id_number": provider_response["idNumber"],
            "uuid": provider_response["responseUuid"],
        }
        return response

    async def register_investor(
        self,
        cif_number,
        reason,
        source_of_fund,
        branch_opening,
        account_type="RDL",
        currency="IDR",
    ):
        """
            function to register investor
            args :
        """
        # payload
        payload = {
            "api_name": "REGIST_INVESTOR_ACC",
            "method": "POST",
            "payload": {
                "cifNumber": cif_number,
                "accountType": account_type,
                "currency": currency,
                "openAccountReason": reason,
                "sourceOfFund": source_of_fund,
                "branchId": branch_opening,
            },
        }

        provider_response = await self.execute(**payload)

        response = {
            "journal_no": provider_response["journalNum"],
            "account_no": provider_response["accountNumber"],
            "uuid": provider_response["responseUuid"],
        }
        return response

    async def create_rdl(
        self,
        title,
        first_name,
        middle_name,
        last_name,
        npwp_option,
        npwp_no,
        nationality,
        country,
        religion,
        birth_place,
        birth_date,
        gender,
        is_married,
        mother_maiden_name,
        job_code,
        education,
        id_number,
        id_issuing_city,
        id_expire_date,
        address_street,
        address_rt_rw_perum,
        address_kelurahan,
        address_kecamatan,
        zip_code,
        home_phone_ext,
        home_phone,
        office_phone_ext,
        office_phone,
        mobile_phone_ext,
        mobile_phone,
        fax_ext,
        fax,
        email,
        monthly_income,
        branch_opening,
        reason,
        source_of_fund
    ):
        """ wrapper function to help create rdl """
        investor_resp = await self.create_investor(
            title,
            first_name,
            middle_name,
            last_name,
            npwp_option,
            npwp_no,
            nationality,
            country,
            religion,
            birth_place,
            birth_date,
            gender,
            is_married,
            mother_maiden_name,
            job_code,
            education,
            id_number,
            id_issuing_city,
            id_expire_date,
            address_street,
            address_rt_rw_perum,
            address_kelurahan,
            address_kecamatan,
            zip_code,
            home_phone_ext,
            home_phone,
            office_phone_ext,
            office_phone,
            mobile_phone_ext,
            mobile_phone,
            fax_ext,
            fax,
            email,
            monthly_income,
            branch_opening,
        )

        cif_number = investor_resp["cif_number"]
        branch_opening = investor_resp["branch_opening"]

        response = await self.register_investor(
            cif_number=cif_number,
            reason=reason,
            source_of_fund=source_of_fund,
            branch_opening=branch_opening
        )
        return response

    async def inquiry_account_info(self, account_no):
        """
            function to get inquiry account info using RDL
            args :
                params -- parameter
        """

        payload = {
            "api_name": "INQUIRY_ACC",
            "method": "POST",
            "payload": {"accountNumber": account_no},
        }

        provider_response = await self.execute(**payload)

        response = {
            "account_no": provider_response["accountNumber"],
            "account_type": provider_response["accountType"],
            "customer_name": provider_response["customerName"],
            "status": provider_response["accountStatus"],
            "uuid": provider_response["responseUuid"],
        }
        return response

    # end def

    async def inquiry_account_balance(self, account_no):
        """
            function to get inquiry account balance using RDL
            args :
                params -- parameter
        """

        payload = {
            "api_name": "INQUIRY_BALANCE",
            "method": "POST",
            "payload": {"accountNumber": account_no},
        }

        provider_response = await self.execute(**payload)

        response = {
            "account_no": provider_response["accountNumber"],
            "customer_name": provider_response["customerName"],
            "balance": provider_response["accountBalance"],
            "uuid": provider_response["responseUuid"],
        }
        return response

    # end def

    async def inquiry_account_history(self, account_no):
        """
            function to get inquiry account history using RDL
            args :
        """

        payload = {
            "api_name": "INQUIRY_HISTORY",
            "method": "POST",
            "payload": {"accountNumber": account_no},
        }

        provider_response = await self.execute(**payload)
        response = RdlAccountHistorySchema().dump(provider_response)
        return response

    async def transfer(
        self, source, bank_code, destination, amount, transfer_uuid, inquiry_uuid=None
    ):
        """ wrapper function that automatically transfer based on bank code """
        # IF ITS BNI Transfer using payment transfer !
        response = {}

        if bank_code == "009":
            inhouse_trf_resp = await self.payment_transfer(
                source=source,
                destination=destination,
                amount=amount,
                remark="",
                request_uuid=transfer_uuid,
            )
            response["response_uuid"] = inhouse_trf_resp["uuid"]
        else:
            inquiry_resp = await self.interbank_inquiry(
                source=source,
                bank_code=bank_code,
                destination=destination,
                request_uuid=inquiry_uuid,
            )

            destination = inquiry_resp["destination"]
            account_name = inquiry_resp["name"]
            bank_name = inquiry_resp["bank"]

            interbank_trf_resp = await self.interbank_transfer(
                source=source,
                destination=destination,
                bank_code=bank_code,
                account_name=account_name,
                bank_name=bank_name,
                amount=amount,
                request_uuid=transfer_uuid,
            )
            response["response_uuid"] = interbank_trf_resp["uuid"]

        return response

    async def payment_transfer(
        self, source, destination, amount, remark, currency="IDR", request_uuid=None
    ):
        """
            function to transfer from p2p company or investor to another BNI
            account through RDL
            args :
        """

        payload = {
            "api_name": "PAYMENT_TRANSFER",
            "method": "POST",
            "payload": {
                "accountNumber": source,
                "beneficiaryAccountNumber": destination,
                "currency": currency,
                "amount": str(amount),
                "remark": remark,
                "request_uuid": request_uuid,
            },
        }

        provider_response = await self.execute(**payload)

        response = {
            "journal_no": provider_response["journalNum"],
            "source": provider_response["accountNumber"],
            "destination": provider_response["beneficiaryAccountNumber"],
            "amount": provider_response["amount"],
            "uuid": provider_response["responseUuid"],
        }
        return response

    async def inquiry_payment_status(self, requested_uuid):
        """
            function to check payment status from PAYMENT TRANSFER
            args:
                params -- parameter
        """
        # build payload here
        payload = {
            "api_name": "PAYMENT_STATUS",
            "method": "POST",
            "payload": {"requestedUuid": requested_uuid},
        }

        provider_response = await self.execute(**payload)
        response = TransferInquirySchema().dump(provider_response)
        return response

    # end def

    async def clearing_transfer(
        self,
        source,
        destination,
        address,
        clearing_code,
        account_name,
        amount,
        remark,
        charge_mode,
        currency="IDR",
        request_uuid=None,
    ):
        """
            function to transfer from p2p company or investor to another BNI
            account through RDL
            args :
        """

        payload = {
            "api_name": "CLEARING_TRANSFER",
            "method": "POST",
            "payload": {
                "accountNumber": source,
                "beneficiaryAccountNumber": destination,
                "beneficiaryAddress1": address,
                "beneficiaryAddress2": "",
                "beneficiaryBankCode": clearing_code,
                "beneficiaryName": account_name,
                "currency": currency,
                "amount": amount,
                "remark": remark,
                "chargingType": charge_mode,
                "request_uuid": request_uuid,
            },
        }

        provider_response = await self.execute(**payload)

        response = {
            "journal_no": provider_response["journalNum"],
            "source": provider_response["accountNumber"],
            "destination": provider_response["beneficiaryAccountNumber"],
            "bank_code": provider_response["beneficiaryBankCode"],
            "amount": provider_response["amount"],
            "remittance_no": provider_response["remittanceNumber"],
            "uuid": provider_response["responseUuid"],
        }
        return response

    async def rtgs_transfer(
        self,
        source,
        destination,
        address,
        rtgs_code,
        account_name,
        amount,
        remark,
        charge_mode,
        currency="IDR",
        request_uuid=None,
    ):
        """
            function to transfer from p2p company or investor to another BNI
            account through rtgs method from RDL
            args :
        """

        payload = {
            "api_name": "RTGS_TRANSFER",
            "method": "POST",
            "payload": {
                "accountNumber": source,
                "beneficiaryAccountNumber": destination,
                "beneficiaryAddress1": address,
                "beneficiaryAddress2": "",
                "beneficiaryBankCode": rtgs_code,
                "beneficiaryName": account_name,
                "currency": currency,
                "amount": amount,
                "remark": remark,
                "chargingType": charge_mode,
                "request_uuid": request_uuid,
            },
        }

        provider_response = await self.execute(**payload)

        response = {
            "journal_no": provider_response["journalNum"],
            "source": provider_response["accountNumber"],
            "destination": provider_response["beneficiaryAccountNumber"],
            "bank_code": provider_response["beneficiaryBankCode"],
            "amount": provider_response["amount"],
            "remittance_no": provider_response["remittanceNumber"],
            "uuid": provider_response["responseUuid"],
        }
        return response

    async def interbank_inquiry(
        self, source, bank_code, destination, request_uuid=None
    ):
        """
            function to transfer from p2p company or investor to another BNI
            account through rtgs method from RDL
            args :
        """

        payload = {
            "api_name": "INTERBANK_INQUIRY",
            "method": "POST",
            "payload": {
                "accountNumber": source,
                "beneficiaryAccountNumber": destination,
                "beneficiaryBankCode": bank_code,
                "request_uuid": request_uuid,
            },
        }

        provider_response = await self.execute(**payload)

        response = {
            "destination": provider_response["beneficiaryAccountNumber"],
            "name": provider_response["beneficiaryAccountName"],
            "bank": provider_response["beneficiaryBankName"],
            "uuid": provider_response["responseUuid"],
            "ref_number": provider_response["retrievalReffNum"],
        }
        return response

    async def interbank_transfer(
        self,
        source,
        destination,
        account_name,
        bank_code,
        bank_name,
        amount,
        request_uuid=None,
    ):
        """
            function to transfer from p2p company or investor to another BNI
            account through rtgs method from RDL
            args :
        """

        payload = {
            "api_name": "INTERBANK_TRANSFER",
            "method": "POST",
            "payload": {
                "accountNumber": source,
                "beneficiaryAccountNumber": destination,
                "beneficiaryAccountName": account_name,
                "beneficiaryBankCode": bank_code,
                "beneficiaryBankName": bank_name,
                "amount": amount,
                "request_uuid": request_uuid,
            },
        }

        provider_response = await self.execute(**payload)

        response = {
            "source": provider_response["accountNumber"],
            "source_account_name": provider_response["accountName"],
            "destination": provider_response["beneficiaryAccountNumber"],
            "destination_name": provider_response["beneficiaryAccountName"],
            "destination_bank": provider_response["beneficiaryBankName"],
            "amount": provider_response["amount"],
            "uuid": provider_response["responseUuid"],
            "ref_number": provider_response["retrievalReffNum"],
        }
        return response


# end class


class BNIRdlProviderBuilder(BaseProvider):
    """ responsible for initializing bni rdl  """

    service_url = BNI_RDL["BASE_URL"]
    service_port = BNI_RDL["PORT"]
    contract = "BNI_AUTH_RDL"
    cache = ExpiringDict(max_len=1, max_age_seconds=3600)


    def __init__(self):
        super().__init__()
        self._instance = None

    async def __call__(self):
        if not self._instance:
            access_token = await self.authorize()
            self._instance = BNIRdlProvider(access_token)
        return self._instance

    def api_name_to_full_url(self, api_name):
        full_url = self.url + BNI_RDL["ROUTES"][api_name]
        return full_url

    def prepare_request(self, **kwargs):
        self.request_contract.url = self.api_name_to_full_url(kwargs["api_name"])
        self.request_contract.method = kwargs["method"]
        self.request_contract.payload = kwargs["payload"]
        return self.request_contract

    async def authorize(self):
        payload = {
            "api_name": "GET_TOKEN",
            "method": "POST",
            "payload": {"grant_type": "client_credentials"},
        }

        try:
            access_token = self.cache["access_token"]
        except KeyError:
            response = await self.execute(**payload)
            access_token = response["access_token"]
            self.cache["access_token"] = access_token
        # end try
        return access_token
