"""
    Package Initialization
"""

from flask_restplus import Api

from flask import Blueprint

from app.api import sentry
from app.api.transactions import api as trx_ns


class CustomApi(Api):
    """ Custom API Classs """

    def handle_error(self, e):
        """ Overrides the handle_error() method of the Api and adds custom error handling
        :param e: error object
        """
        code = getattr(e, "code", 500)  # Gets code or defaults to 500
        message = getattr(e, "message", "INTERNAL_SERVER_ERROR")
        to_dict = getattr(e, "to_dict", None)

        if code == 500:
            # capture error and send to sentry
            sentry.captureException(e)
            data = {"error": message}

        # handle request schema error from reqparse
        if code == 400:
            response = getattr(e, "response", True)
            if response is None:
                # build error response
                data = {
                    "error": "MISSING_PARAMETER",
                    "message": e.data["message"],
                    "details": e.data["errors"],
                }

        if to_dict:
            data = to_dict()
        return self.make_response(data, code)


blueprint = Blueprint("api", __name__)
# intialize API
api = CustomApi(blueprint, contact="kelvindsmn@gmail.com")  # register blueprint
api.add_namespace(trx_ns, path="/transaction")
