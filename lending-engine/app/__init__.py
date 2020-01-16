"""
    Package Initialization
"""

from flask_restplus import Api

from flask import Blueprint

from app.api.investor import api as investor_ns
from app.api.investment import api as investment_ns
from app.api.callback import api as callback_ns
from app.api.report import api as report_ns
from app.api.health import api as health_ns


class CustomApi(Api):
    """ Custom API Classs """

    def handle_error(self, e):
        """ Overrides the handle_error() method of the Api and adds custom error handling
        :param e: error object
        """
        code = getattr(e, "code", 500)  # Gets code or defaults to 500
        message = getattr(e, "message", "INTERNAL_SERVER_ERROR")
        to_dict = getattr(e, "to_dict", None)

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
api = CustomApi(
    blueprint, catch_all_404s=True, version="1.0", ui=False, contact="kelvin@modana.id"
)
api.add_namespace(investor_ns, path="/investor")
api.add_namespace(callback_ns, path="/callback")
api.add_namespace(investment_ns, path="/investment")
api.add_namespace(report_ns, path="/report")
api.add_namespace(health_ns, path="/health")
