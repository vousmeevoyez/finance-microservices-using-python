"""
    Test BNI Rdl Request
    ______________
"""
from rpc.factories.request.v1.request import BNIRdlAuthRequest, BNIRdlRequest


class TestBNIRdlAuthRequest:
    """ Testing class for BNI RDL Auth Request """

    def test_create_signature(self):
        """ test create signature method """
        http_request = BNIRdlAuthRequest()
        http_request.url = "https://apidev.bni.co.id:8066/api/oauth/token"
        http_request.method = "POST"
        result = http_request.create_signature(
            {
                "header": {
                    "companyId": "SANDBOX",
                    "parentCompanyId": "STI_CHS",
                    "requestUuid": "E26DB4C8F6484E72",
                }
            }
        )
        assert len(result) > 15

    def test_to_representation(self):
        """ test method to represent the request object """
        http_request = BNIRdlAuthRequest()
        http_request.method = "POST"
        http_request.url = "https://apidev.bni.co.id:8066/api/oauth/token"
        http_request.payload = {"grant_type": "client_credentials"}

        request = http_request.to_representation()

        assert request["url"]
        # check headers
        assert request["headers"]
        assert request["headers"]["Authorization"]
        assert request["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        # check data
        assert request["data"]
        assert request["method"]
        assert request["timeout"]


class TestBNIRdlRequest:
    """ Testing class for BNI RDL Request """

    def test_to_representation(self):
        """ test method to represent the request object """
        http_request = BNIRdlRequest()
        http_request.url = "https://apidev.bni.co.id:8066/p2pl/register/investor"
        http_request.method = "POST"
        http_request.payload = {
            "title": "01",
            "firstName": "Juan",
            "middleName": "",
            "lastName": "Daniel",
            "optNPWP": "1",
            "NPWPNum": "999999999999999",
            "nationality": "ID",
            "domicileCountry": "ID",
            "religion": "2",
            "birthPlace": "Semarang",
            "birthDate": "26111980",
            "gender": "M",
            "isMarried": "L",
            "motherMaidenName": "Dina Maryati",
            "jobCode": "01",
            "education": "07",
            "idNumber": "331234766887878518",
            "idIssuingCity": "Jakarta Barat",
            "idExpiryDate": "26102099",
            "addressStreet": "Jalan Mawar Melati",
            "addressRtRwPerum": "003009Sentosa",
            "addressKel": "Cengkareng Barat",
            "addressKec": "Cengkareng/Jakarta Barat",
            "zipCode": "11730",
            "homePhone1": "021",
            "homePhone2": "745454545",
            "officePhone1": "",
            "officePhone2": "",
            "mobilePhone1": "0812",
            "mobilePhone2": "323232",
            "faxNum1": "",
            "faxNum2": "",
            "email": "juan.daniel@gmail.com",
            "monthlyIncome": "8000000",
            "branchOpening": "259",
        }
        request = http_request.to_representation()

        assert request["url"]
        # check headers
        assert request["headers"]
        assert request["headers"]["x-api-key"]
        assert request["headers"]["Content-Type"] == "application/json"
        # check data
        assert request["data"]
        assert request["method"]
        assert request["timeout"]
