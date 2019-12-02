"""
    BNI OPG Response Object
    __________________
    module to handle HTTP Response from BNI OPG
"""
from rpc.lib.core.response import AsyncHTTPResponse
from rpc.lib.core.response import FailedResponseError, ResponseError

ACCEPTED_RESP_CODES = ["0001", "3656"]


class BNIRdlAuthResponse(AsyncHTTPResponse):
    """ HTTP Response represent BNI RDL Auth Response """

    def validate_status_code(self):
        """ override base http response so it raise Response Error
        instead of StatusCodeError """
        status_code = self.http_status
        if status_code != 200:
            # later should check whether status code valid or not !
            raise ResponseError("RESPONSE_FAILED", self.data)
        return True


class BNIRdlResponse(AsyncHTTPResponse):
    """ BNI Rdl Response """

    wrapper_key = (
        "response"
    )  # used so every response automatically unpacked with this key

    @staticmethod
    def _check_response_code(response):
        """
            special function to check response code according to BNI response
            and handle any weird error
        """
        for key, value in response.items():
            for key, value in value.items():
                if key == "responseCode":
                    # check response code here
                    if value not in ACCEPTED_RESP_CODES:
                        # mark request as failed
                        raise FailedResponseError(original_exception=response)
                elif key == "parameters":
                    # check response code here
                    if value["responseCode"] not in ACCEPTED_RESP_CODES: 
                        # mark request as failed
                        raise FailedResponseError(original_exception=response)
        return True

    def validate_data(self):
        """ for bni response we need to decrypt it first before consume it """
        try:
            # first validate status any response
            self._check_response_code(self.data)
        except FailedResponseError as error:
            raise ResponseError("RESPONSE_FAILED", error.original_exception)
        # end try

    def validate(self):
        # only validate data ignore HTTP status code
        self.validate_data()
