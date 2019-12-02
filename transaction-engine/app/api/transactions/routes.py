"""
    Routes
    ___________
    this is where our flask app define all url
"""
from flask import current_app
from flask_restplus import Resource
from celery import chain

from app.api.transactions import api
from app.api.lib.core.routes import Routes
from app.api.request_schema import TransactionRequestSchema
from app.api.serializer import TrxSchema as TransactionSchema
from app.api.transactions.services import (
    single_transaction,
    get_all
)


@api.route("/")
class TransactionRoutes(Routes):
    """
        Create Transaction
        /investor-id/approve/
    """

    __schema__ = TransactionRequestSchema
    __serializer__ = TransactionSchema()

    def post(self):
        request_data = self.serialize(self.payload())
        current_app.logger.info("Request Data......")
        current_app.logger.info(request_data)

        trx_id = single_transaction(**request_data)
        return {"id": str(trx_id)}, 202

    def get(self):
        result = get_all()
        return result
