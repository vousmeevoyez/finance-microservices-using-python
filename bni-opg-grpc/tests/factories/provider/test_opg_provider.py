import pytest
from asynctest import CoroutineMock, patch

from rpc.lib.core.provider import ProviderError
from rpc.factories.provider.v1.provider import (
    BNIOpgProvider,
    BNIOpgProviderBuilder
)

from rpc.config import BNI_OPG


class TestBNIOpgProviderBuilder:

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_authorize(self, mock_request):
        expected_value = {
            "access_token": "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2",
            "token_type": "Bearer",
            "expires_in": 3599,
            "scope": "resource.WRITE resource.READ"
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        builder = BNIOpgProviderBuilder()
        result = await builder.authorize()
        assert result == "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"


class TestMockBNIOpgProvider:
    """ Test class for BNI OPG Provider """

    def test_api_name_to_full_url(self):
        result = BNIOpgProvider("some-access-token").api_name_to_full_url("GET_BALANCE")
        assert result == "https://apidev.bni.co.id:8066/H2H/v2/getbalance?access_token=some-access-token"

    def test_prepare_request(self):
        """ make sure by passing api_name we get the designated request object
        !"""
        payload = {
            "api_name": "GET_BALANCE",
            "method": "POST",
            "payload": {"somepayload": "test"}
        }
        result = BNIOpgProvider("some-access-token").prepare_request(**payload)
        request = result.to_representation()
        assert request["url"]
        assert request["method"]
        assert request["data"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_balance_success(self, mock_request):
        """ test success get balance from BNI OPG"""
        expected_value = {
            "getBalanceResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0001",
                    "responseMessage": "Request has been processed successfully",
                    "responseTimestamp": "2017-02-24T14:12:25.871Z",
                    "customerName": "Bpk JONOMADE MADEMADEMADEMADE IMAMADE",
                    "accountCurrency": "IDR",
                    "accountBalance": 16732765949981,
                },
            }
        }
        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)
        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        result = await BNIOpgProvider(access_token).get_balance("123456")
        assert result
        assert result["customer_name"]
        assert result["balance"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_balance_failed(self, mock_request):
        """ test fail to get balance from BNI OPG"""
        expected_value = {
            "getBalanceResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0000",
                    "errorMessage": "Unknown Output",
                    "responseMessage": "Request failed",
                    "responseTimestamp": "2017-02-24T14:12:25.871Z",
                }
            }
        }
        mock_request.return_value.__aenter__.return_value.status = 400
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        with pytest.raises(ProviderError):
            result = await BNIOpgProvider(access_token).get_balance("123456")

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_inhouse_inquiry(self, mock_request):
        """ test get account information from BNI OPG"""
        # mock the response here
        expected_value = {
            "getInHouseInquiryResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0001",
                    "responseMessage": "Request has been processed successfully",
                    "responseTimestamp": "2017-09-07T14:10:23.431Z",
                    "customerName": "Bpk JONOMADE MADEMADEMADEMADE IMAMADE",
                    "accountCurrency": "IDR",
                    "accountNumber": "0115475045",
                    "accountStatus": "BUKA",
                    "accountType": "DEP",
                },
            }
        }
        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)
        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        result = await BNIOpgProvider(access_token).get_inhouse_inquiry("123456")

        assert result
        assert result["account_no"]
        assert result["customer_name"]
        assert result["status"]
        assert result["account_type"]
        assert result["type"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_inhouse_inquiry_failed(self, mock_request):
        """ test failed to get account inquiry from BNI OPG"""
        # mock the response here
        expected_value = {
            "getInHouseInquiryResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0000",
                    "responseMessage": "Request Failed",
                    "errorMessage": "Some error message",
                    "responseTimestamp": "2017-09-07T14:10:23.431Z",
                },
            }
        }
        mock_request.return_value.__aenter__.return_value.status = 400
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)
        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        with pytest.raises(ProviderError):
            result = await BNIOpgProvider(access_token).get_inhouse_inquiry("123456")

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_do_payment_success(self, mock_request):
        """ test success do payment from BNI OPG"""
        # mock the response here
        expected_value = {
            "doPaymentResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0001",
                    "responseMessage": "Request has been processed successfully",
                    "responseTimestamp": "2017-02-27T14:46:55.084Z",
                    "debitAccountNo": 113183203,
                    "creditAccountNo": 115471119,
                    "valueAmount": 100500,
                    "valueCurrency": "IDR",
                    "bankReference": 953403,
                    "customerReference": 20170227000000000020,
                },
            }
        }

        data = {
            "method": "IN_HOUSE",
            "source": "113183203",
            "destination": "115471119",
            "amount": "100500",
            "ref_number": "20170227000000000020",
            "email": "jennie@blackpink.com",
            "clearing_code": "CENAIDJAXXX",
            "account_name": "Jennie",
            "address": "Jl. Buntu",
            "charge_mode": "SOURCE",
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        result = await BNIOpgProvider(access_token).do_payment(**data)
        assert result
        assert result["source"]
        assert result["destination"]
        assert result["amount"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_do_payment_failed(self, mock_request):
        """ test fail to do payment from BNI OPG"""
        # mock the response here
        expected_value = {
            "doPaymentResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0000",
                    "responseTimestamp": "2017-02-27T14:46:55.084Z",
                    "responseMessage": "Request Failed",
                    "errorMessage": "Some error message",
                },
            }
        }

        data = {
            "method": "IN_HOUSE",
            "source": "113183203",
            "destination": "115471119",
            "amount": "100500",
            "ref_number": "20170227000000000020",
            "email": "jennie@blackpink.com",
            "clearing_code": "CENAIDJAXXX",
            "account_name": "Jennie",
            "address": "Jl. Buntu",
            "charge_mode": "SOURCE",
        }

        mock_request.return_value.__aenter__.return_value.status = 400
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        with pytest.raises(ProviderError):
            result = await BNIOpgProvider(access_token).do_payment(**data)

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_payment_status_success(self, mock_request):
        """ test success to get payment status from BNI OPG"""
        # mock the response here
        expected_value = {
            "getPaymentStatusResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0001",
                    "responseMessage": "Request has been processed successfully",
                    "responseTimestamp": "2017-02-27T15:04:00.927Z",
                    "previousResponse": {
                        "transactionStatus": "Y",
                        "previousResponseCode": "null",
                        "previousResponseMessage": "null",
                        "previousResponseTimestamp": "2017-02-27T07:47:14.640Z",
                        "debitAccountNo": 113183203,
                        "creditAccountNo": 115471119,
                        "valueAmount": 100500,
                        "valueCurrency": "IDR",
                    },
                    "bankReference": 953403,
                    "customerReference": 20170227000000000020,
                },
            }
        }

        data = {"request_ref": "20170227000000000020"}


        mock_request.return_value.__aenter__.return_value.status = 400
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        result = await BNIOpgProvider(access_token).get_payment_status(**data)

        assert result
        assert result["status"]
        assert result["source"]
        assert result["destination"]
        assert result["amount"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_payment_status_failed(self, mock_request):
        """ test failed to get payment status from BNI OPG"""
        # mock the response here
        expected_value = {
            "getPaymentStatusResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0000",
                    "responseMessage": "Request Failed",
                    "responseTimestamp": "2017-02-27T15:04:00.927Z",
                    "errorMessage": "Some Error Message",
                },
            }
        }

        data = {"request_ref": "20170227000000000020"}


        mock_request.return_value.__aenter__.return_value.status = 400
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        with pytest.raises(ProviderError):
            result = await BNIOpgProvider(access_token).get_payment_status(**data)

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_interbank_inquiry_success(self, mock_request):
        """ test succesfully get interbank inquiry from BNI OPG"""
        # mock the response here
        expected_value = {
            "getInterbankInquiryResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0001",
                    "responseMessage": "Request has been processed successfully",
                    "responseTimestamp": "2017-05-08T14:57:51.963Z",
                    "destinationAccountNum": "113183203",
                    "destinationAccountName": "DUMMY NAME",
                    "destinationBankName": "BCA",
                    "retrievalReffNum": 100000000097,
                },
            }
        }

        data = {
            "ref_number": "20170227000000000020",
            "source": "113183203",
            "bank_code": "014",
            "destination": "3333333333",
        }


        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        result = await BNIOpgProvider(access_token).get_interbank_inquiry(**data)
        assert result
        assert result["destination"]
        assert result["destination_name"]
        assert result["bank_name"]
        assert result["transfer_ref"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_get_interbank_inquiry_failed(self, mock_request):
        """ test failed get interbank inquiry from BNI OPG"""
        # mock the response here
        expected_value = {
            "getInterbankInquiryResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0000",
                    "responseMessage": "Error",
                    "errorMessage": "Some error message",
                    "responseTimestamp": "2017-05-08T14:57:51.963Z",
                },
            }
        }

        data = {
            "ref_number": "20170227000000000020",
            "source": "113183203",
            "bank_code": "014",
            "destination": "3333333333",
        }


        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        with pytest.raises(ProviderError):
            result = await BNIOpgProvider(access_token).get_interbank_inquiry(**data)

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_interbank_payment_success(self, mock_request):
        """ test failed get interbank payment success from BNI OPG"""
        # mock the response here
        expected_value = {
            "getInterbankPaymentResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0001",
                    "responseMessage": "Request has been processed successfully",
                    "responseTimestamp": "2017-03-01T11:45:02.062Z",
                    "destinationAccountNum": 3333333333,
                    "destinationAccountName": "BENEFICIARY NAME",
                    "customerReffNum": 100000000011,
                    "accountName": "BPK JONOMADE MADEMADEMADEMADE",
                },
            }
        }

        data = {
            "ref_number": "20170227000000000020",
            "amount": "10000",
            "source": "115471119",
            "destination": "3333333333",
            "destination_name": "Jennie",
            "bank_code": "014",
            "bank_name": "BCA",
            "transfer_ref": "100000000024",
        }


        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        result = await BNIOpgProvider(access_token).interbank_payment(**data)
        assert result["destination"]
        assert result["destination_name"]
        assert result["uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_interbank_payment_failed(self, mock_request):
        """ test failed get interbank payment success from BNI OPG"""
        # mock the response here
        expected_value = {
            "getInterbankPaymentResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0000",
                    "responseMessage": "Request Failed",
                    "responseTimestamp": "2017-02-27T15:04:00.927Z",
                    "errorMessage": "Some Error Message",
                },
            }
        }

        data = {
            "ref_number": "20170227000000000020",
            "amount": "10000",
            "source": "115471119",
            "destination": "3333333333",
            "destination_name": "Jennie",
            "bank_code": "014",
            "bank_name": "BCA",
            "transfer_ref": "100000000024",
        }

        mock_request.return_value.__aenter__.return_value.status = 400
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        with pytest.raises(ProviderError):
            result = await BNIOpgProvider(access_token).interbank_payment(**data)

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_bni_transfer_success(self, mock_request):
        """ test successfully transfer from bni to bni"""
        # mock the response here
        expected_value = {
            "doPaymentResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0001",
                    "responseMessage": "Request has been processed successfully",
                    "responseTimestamp": "2017-02-27T14:46:55.084Z",
                    "debitAccountNo": 113183203,
                    "creditAccountNo": 115471119,
                    "valueAmount": 100500,
                    "valueCurrency": "IDR",
                    "bankReference": 953403,
                    "customerReference": 20170227000000000020,
                },
            }
        }

        data = {
            "source": "113183203",
            "destination": "115471119",
            "amount": "100500",
            "bank_code": "009"
        }

        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        result = await BNIOpgProvider(access_token).transfer(**data)
        assert result["response_uuid"]

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.request")
    async def test_bni_transfer_failed(self, mock_request):
        """ test failed to transfer from bni to bni"""
        # mock the response here
        expected_value = {
            "doPaymentResponse": {
                "clientId": "BNISERVICE",
                "parameters": {
                    "responseCode": "0000",
                    "responseMessage": "Request Failed",
                    "responseTimestamp": "2017-02-27T15:04:00.927Z",
                    "errorMessage": "Some Error Message",
                },
            }
        }

        data = {
            "source": "113183203",
            "destination": "115471119",
            "amount": "100500",
            "bank_code": "009",
        }

        mock_request.return_value.__aenter__.return_value.status = 400
        mock_request.return_value.__aenter__.return_value.json = \
        CoroutineMock(return_value=expected_value)

        access_token = "x3LyfeWKbeaARhd2PfU4F4OeNi43CrDFdi6XnzScKIuk5VmvFiq0B2"

        with pytest.raises(ProviderError):
            result = await BNIOpgProvider(access_token).transfer(**data)
