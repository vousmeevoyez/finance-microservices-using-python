"""
    Test BNI RDL Provider
    ___________________
"""

import pytest
from asynctest import CoroutineMock, patch

from rpc.lib.core.provider import ProviderError
from rpc.factories.provider.v1.provider import BNIRdlProvider, BNIRdlProviderBuilder

from rpc.config import BNI_RDL


class TestBNIRDLProviderBuilder:
    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_authorize(self, mock_request):
        expected_value = {
            "access_token": "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2",
            "token_type": "Bearer",
            "expires_in": 3599,
            "scope": "resource.WRITE resource.READ",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        builder = BNIRdlProviderBuilder()
        result = await builder.authorize()
        assert result == "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"


class TestBNIRdlProvider:
    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_create_investor(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-06 23:11:44.226",
                "responseUuid": "29FCB72E71D34C48",
                "journalNum": "000000",
                "cifNumber": "9100749959",
                "mobilePhone": "0812323232",
                "branchOpening": "00259",
                "idNumber": "331234766887878518",
                "customerName": "JUAN DANIEL",
            }
        }

        data = {
            "title": "01",
            "first_name": "Juan",
            "middle_name": "",
            "last_name": "Daniel",
            "npwp_option": "1",
            "npwp_no": "999999999999999",
            "nationality": "ID",
            "country": "ID",
            "religion": "2",
            "birth_place": "Semarang",
            "birth_date": "26111980",
            "gender": "M",
            "is_married": "L",
            "mother_maiden_name": "Dina Maryati",
            "job_code": "01",
            "education": "07",
            "id_number": "331234766887878518",
            "id_issuing_city": "Jakarta Barat",
            "id_expire_date": "26102099",
            "address_street": "Jalan Mawar Melati",
            "address_rt_rw_perum": "003009Sentosa",
            "address_kelurahan": "Cengkareng Barat",
            "address_kecamatan": "Cengkareng/Jakarta Barat",
            "zip_code": "11730",
            "home_phone_ext": "021",
            "home_phone": "745454545",
            "office_phone_ext": "",
            "office_phone": "",
            "mobile_phone_ext": "0812",
            "mobile_phone": "323232",
            "fax_ext": "",
            "fax": "",
            "email": "juan.daniel@gmail.com",
            "monthly_income": "8000000",
            "branch_opening": "259",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).create_investor(**data)
        assert result["customer_name"]
        assert result["journal_no"]
        assert result["cif_number"]
        assert result["mobile_phone"]
        assert result["branch_opening"]
        assert result["id_number"]
        assert result["customer_name"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_create_investor_cif_already_exist(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "3656",
                "responseMessage": "Requested ID number already has a CIF number",
                "responseTimestamp": "2019-10-03 15:55:08.508",
                "responseUuid": "20FDDE4B7B824610",
                "journalNum": "000000",
                "cifNumber": "9100749959",
                "mobilePhone": "0812323232",
                "branchOpening": "0259",
                "idNumber": "331234766887878518",
                "customerName": "JUAN DANIEL",
            }
        }

        data = {
            "title": "01",
            "first_name": "Juan",
            "middle_name": "",
            "last_name": "Daniel",
            "npwp_option": "1",
            "npwp_no": "999999999999999",
            "nationality": "ID",
            "country": "ID",
            "religion": "2",
            "birth_place": "Semarang",
            "birth_date": "26111980",
            "gender": "M",
            "is_married": "L",
            "mother_maiden_name": "Dina Maryati",
            "job_code": "01",
            "education": "07",
            "id_number": "331234766887878518",
            "id_issuing_city": "Jakarta Barat",
            "id_expire_date": "26102099",
            "address_street": "Jalan Mawar Melati",
            "address_rt_rw_perum": "003009Sentosa",
            "address_kelurahan": "Cengkareng Barat",
            "address_kecamatan": "Cengkareng/Jakarta Barat",
            "zip_code": "11730",
            "home_phone_ext": "021",
            "home_phone": "745454545",
            "office_phone_ext": "",
            "office_phone": "",
            "mobile_phone_ext": "0812",
            "mobile_phone": "323232",
            "fax_ext": "",
            "fax": "",
            "email": "juan.daniel@gmail.com",
            "monthly_income": "8000000",
            "branch_opening": "259",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).create_investor(**data)
        assert result["customer_name"]
        assert result["journal_no"]
        assert result["cif_number"]
        assert result["mobile_phone"]
        assert result["branch_opening"]
        assert result["id_number"]
        assert result["customer_name"]
        assert result["uuid"]
    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_register_investor(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-06 23:11:44.226",
                "responseUuid": "29FCB72E71D34C48",
                "journalNum": "230223",
                "accountNumber": "114476287",
            }
        }

        data = {
            "cif_number": "9100749959",
            "account_type": "RDL",
            "reason": "2",
            "source_of_fund": "1",
            "branch_opening": "259",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).register_investor(**data)

        assert result["journal_no"]
        assert result["account_no"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_inquiry_account_info(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-07 19:44:18.145",
                "responseUuid": "E26DB4C8F6484E72",
                "accountNumber": "0115476117",
                "accountType": "DEP",
                "customerName": "Bpk ROBERT NARO ROBERT NARO",
                "currency": "IDR",
                "accountStatus": "BUKA",
            }
        }

        data = {"account_no": "0115476117"}

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).inquiry_account_info(**data)

        assert result["account_no"]
        assert result["account_type"]
        assert result["customer_name"]
        assert result["status"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_inquiry_account_balance(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-07 19:51:37.448",
                "responseUuid": "DD454674BF074D9E",
                "accountNumber": "0115476117",
                "customerName": "Bpk ROBERT NARO ROBERT NARO",
                "currency": "IDR",
                "accountBalance": "20478259594945",
            }
        }

        data = {"account_no": "0115476117"}

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).inquiry_account_balance(**data)

        assert result["account_no"]
        assert result["customer_name"]
        assert result["balance"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_inquiry_account_history(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-07 20:16:57.096",
                "responseUuid": "413DDF336A174F81",
                "accountNumber": "0115476117",
                "accountName": "Bpk ROBERT NARO ROBERT NARO",
                "productName": "GIRO TDK HIT BBB PERUSAHAAN",
                "address1": "JALAN NARO TERKINI",
                "address2": "PERUM NARO TERKINI",
                "address4": "Abiansemal",
                "address3": "DESA NARO TERKINI",
                "postCode": "80352",
                "currency": "IDR",
                "fromDate": "2010-05-31",
                "toDate": "2010-05-31",
                "beginingBalance": "20577099077934.00",
                "debitsTotal": "2026000.00",
                "creditsTotal": "162909195.00",
                "endingBalance": "20577259961029.00",
                "totalRecords": "000101",
                "longHistoricals": [
                    {
                        "sequenceNum": "000001",
                        "date": "2010-05-31",
                        "description": "TRANSFER DARI",
                        "narative": "merchantName",
                        "branchNum": "986",
                        "tracer": "955139",
                        "txcode": "00",
                        "debit_credit": "K",
                        "amount": "1000.002",
                        "balance": "0577259961029.00",
                        "tofrAccount": "00000000115476151",
                        "transactionTime": "18:57:31",
                        "narative36": "Bpk ROBERT NARO ROBERT NARO",
                        "narative02": "",
                        "narative03": "",
                        "narative38": "",
                        "narative39": "",
                    }
                ],
            }
        }

        data = {"account_no": "0115476117"}

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).inquiry_account_history(**data)
        assert result

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_payment_transfer(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-10 12:36:47.881",
                "responseUuid": "E8C6E0027F6E429F",
                "journalNum": "940301",
                "accountNumber": "0115476117",
                "beneficiaryAccountNumber": "0115471119",
                "amount": "11500",
            }
        }

        data = {
            "source": "0115476117",
            "destination": "0115471119",
            "amount": "11500",
            "remark": "Test P2PL",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).payment_transfer(**data)

        assert result["journal_no"]
        assert result["source"]
        assert result["destination"]
        assert result["amount"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_payment_transfer_uuid(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-10 12:36:47.881",
                "responseUuid": "E8C6E0027F6E429F",
                "journalNum": "940301",
                "accountNumber": "0115476117",
                "beneficiaryAccountNumber": "0115471119",
                "amount": "11500",
            }
        }

        data = {
            "source": "0115476117",
            "destination": "0115471119",
            "amount": "11500",
            "remark": "Test P2PL",
            "request_uuid": "ABCDEFG12345678",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).payment_transfer(**data)

        assert result["journal_no"]
        assert result["source"]
        assert result["destination"]
        assert result["amount"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_inquiry_payment_status(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-10 12:36:47.881",
                "responseUuid": "106323AEB63D4FF0",
                "requestedUuid": "E8C6E0027F6E429F",
                "transactionStatus": "PAID",
                "transactionDateTime": "2018-12-10 12:36:47.883",
                "transactionType": "paymentUsingTransfer",
                "journalNum": "940301",
                "accountNumber": "0115476117",
                "beneficiaryAccountNumber": "0115471119",
                "currency": "IDR",
            }
        }

        data = {"requested_uuid": "E8C6E0027F6E429F"}

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).inquiry_payment_status(**data)

        assert result["status"]
        assert result["created_at"]
        assert result["transaction_type"]
        assert result["source"]
        assert result["destination"]
        assert result["request_uuid"]
        assert result["response_uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_inquiry_payment_status_interbank(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2019-10-07 15:37:51.906",
                "responseUuid": "DADAD7FD46C54162",
                "requestedUuid": "585E28DC4FF54767",
                "transactionStatus": "PAID",
                "transactionDateTime": "2019-10-07 15:33:31.603",
                "transactionType": "paymentUsingInterbank",
                "accountNumber": "0116724773",
                "beneficiaryAccountNumber": "0011223344",
                "beneficiaryBankCode": "014",
            }
        }

        data = {"requested_uuid": "E8C6E0027F6E429F"}

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).inquiry_payment_status(**data)

        assert result["status"]
        assert result["created_at"]
        assert result["transaction_type"]
        assert result["source"]
        assert result["destination"]
        assert result["request_uuid"]
        assert result["response_uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_clearing_transfer(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-11 15:34:48.692",
                "responseUuid": "F980D79CB0EB41D7",
                "journalNum": "231281",
                "accountNumber": "0115476117",
                "beneficiaryAccountNumber": "3333333333",
                "beneficiaryBankCode": "140397",
                "amount": "15000",
                "remittanceNumber": "9860000001098802",
            }
        }

        data = {
            "source": "0115476117",
            "destination": "3333333333",
            "address": "Jakarta",
            "clearing_code": "140397",
            "account_name": "Panji Samudra",
            "amount": "15000",
            "remark": "Test kliring",
            "charge_mode": "OUR",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).clearing_transfer(**data)

        assert result["journal_no"]
        assert result["source"]
        assert result["destination"]
        assert result["bank_code"]
        assert result["amount"]
        assert result["remittance_no"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_clearing_transfer_error(self, mock_request):
        expected_value = {
            "Response": {
                "parameters": {
                    "responseCode": "0000",
                    "responseMessage": "Unknown output",
                    "errorMessage": "Unknown output",
                }
            }
        }

        data = {
            "source": "0115476117",
            "destination": "3333333333",
            "address": "Jakarta",
            "clearing_code": "140397",
            "account_name": "Panji Samudra",
            "amount": "15000",
            "remark": "Test kliring",
            "charge_mode": "OUR",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        with pytest.raises(ProviderError):
            result = await BNIRdlProvider(access_token).clearing_transfer(**data)

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_rtgs_transfer(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-11 17:09:33.555",
                "responseUuid": "871BFD631BBB4798",
                "journalNum": "231360",
                "accountNumber": "0115476117",
                "beneficiaryAccountNumber": "3333333333",
                "beneficiaryBankCode": "CENAIDJA",
                "amount": "150000000",
                "remittanceNumber": "R77760677952BE56",
            }
        }

        data = {
            "source": "0115476117",
            "destination": "3333333333",
            "address": "Jakarta",
            "rtgs_code": "CENAIDJA",
            "account_name": "Panji Samudra",
            "amount": "150000000",
            "remark": "Test rtgs",
            "charge_mode": "OUR",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).rtgs_transfer(**data)

        assert result["journal_no"]
        assert result["source"]
        assert result["destination"]
        assert result["bank_code"]
        assert result["amount"]
        assert result["remittance_no"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_interbank_inquiry(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-10 18:07:07.788",
                "responseUuid": "C202946D99844E59",
                "retrievalReffNum": "100000000097",
                "beneficiaryAccountNumber": "3333333333",
                "beneficiaryAccountName": "Bpk KEN AROK",
                "beneficiaryBankName": "BCA",
            }
        }

        data = {"source": "0115476117", "bank_code": "014", "destination": "3333333333"}

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).interbank_inquiry(**data)

        assert result["destination"]
        assert result["name"]
        assert result["bank"]
        assert result["uuid"]
        assert result["ref_number"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_interbank_transfer(self, mock_request):
        expected_value = {
            "response": {
                "responseCode": "0001",
                "responseMessage": "Request has been processed successfully",
                "responseTimestamp": "2018-12-10 18:07:07.788",
                "responseUuid": "C202946D99844E59",
                "retrievalReffNum": "100000000102",
                "accountNumber": "0115476117",
                "accountName": "BNI API SERVICES",
                "beneficiaryAccountNumber": "3333333333",
                "beneficiaryAccountName": "KEN AROK",
                "beneficiaryBankName": "BANK BCA",
                "amount": "15000",
            }
        }

        data = {
            "source": "0115476117",
            "destination": "3333333333",
            "account_name": "KEN AROK",
            "bank_code": "014",
            "bank_name": "BANK BCA",
            "amount": "15000",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = CoroutineMock(
            return_value=expected_value
        )

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"
        result = await BNIRdlProvider(access_token).interbank_transfer(**data)

        assert result["source"]
        assert result["source_account_name"]
        assert result["destination"]
        assert result["destination_name"]
        assert result["destination_bank"]
        assert result["amount"]
        assert result["uuid"]
        assert result["ref_number"]
