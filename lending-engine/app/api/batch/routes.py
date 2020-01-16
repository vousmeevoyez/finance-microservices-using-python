"""
    Routes
    ___________
    this is where our flask app define all url
"""
from flask_restplus import Resource
from celery import chain

from app.api.investment import api
from app.api.investment.modules.services import InvestmentServices
from app.api.investment.modules.fake_services import (
    create_random_loan_request,
    create_random_investment,
)


@api.route("/<string:investment_id>/invest/")
class InvestorRoutes(Resource):
    """
        Investment
        /investment-id/invest/
    """

    def post(self, investment_id):
        """ start prepare to invest !"""
        response = InvestmentServices(investment_id).prepare_investment()
        return response


@api.route("/<string:investor_id>/<string:loan_request_id>/random")
class InvestmentRandomRoutes(Resource):
    """
        /
    """

    def post(self, investor_id, loan_request_id):
        # get all investment
        response = create_random_investment(investor_id, loan_request_id)
        return response


@api.route("/loan_request/random")
class BorrowerRandomRoutes(Resource):
    """
        /
    """

    def post(self):
        # get all investment
        response = create_random_loan_request()
        return response
