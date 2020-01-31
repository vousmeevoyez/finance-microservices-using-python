"""
    Routes
    ___________
    this is where our flask app define all url
"""
from flask_restplus import Resource
from celery import chain

from app.api.investor import api
from app.api.lib.core.routes import Routes
from app.api.models.investor import Investor
from app.api.serializer import WithdrawSchema
from app.api.investor.modules.services import (
    approve_investor,
    withdraw,
    sync_balance
)
from app.api.investor.modules.fake_services import (
    create_random_investor
)


@api.route("/random")
class InvestorRoutes(Routes):
    """
        special endpoint for generation random user + investor
    """

    def post(self):
        investor, user = create_random_investor()
        return {"investor": investor.dump(), "user": user.dump()}


@api.route("/<string:investor_id>/approve/")
class InvestorApproveRoutes(Routes):
    """
        Approve Investor
        /investor-id/approve/
    """

    def post(self, investor_id):
        """ sending background task to approve investor """
        response = approve_investor(investor_id)
        return response


@api.route("/<string:investor_id>/withdraw/")
class InvestorWithdrawRoutes(Routes):
    """
        Withdraw RDL Investor
        /investor-id/withdraw/
    """

    __serializer__ = WithdrawSchema(strict=True)

    def post(self, investor_id):
        """ sending background task to approve investor """
        request_data = self.serialize(self.payload(raw=True))
        request_data["investor_id"] = investor_id

        response = withdraw(**request_data)
        return response


@api.route("/<string:investor_id>/sync/")
class InvestorSyncBalanceRoutes(Routes):
    """
         Sync Investor Balance
        /investor-id/sync/
    """

    def post(self, investor_id):
        response = sync_balance(investor_id)
        return response
