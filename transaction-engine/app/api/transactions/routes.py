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
from app.api.request_schema import (
    TransactionRequestSchema,
    BulkTransactionRequestSchema,
)
from app.api.serializer import (
    TrxSchema as TransactionSchema,
    BulkTrxSchema as BulkTransactionSchema,
)
from app.api.transactions.services import single_transaction, bulk_transaction, get_all


@api.route("/")
class TransactionRoutes(Routes):
    """
        Create Transaction
        /transaction/
    """

    __schema__ = TransactionRequestSchema
    __serializer__ = TransactionSchema()

    def post(self):
        request_data = self.serialize(self.payload())
        current_app.logger.info("Request Data......")
        current_app.logger.info(request_data)

        trx_id = single_transaction(**request_data)
        return {"id": str(trx_id)}, 202


@api.route("/bulk")
class TransactionBulkRoutes(Routes):
    """
        Create Bulk Transaction
        /transaction/bulk
    """

    __schema__ = BulkTransactionRequestSchema
    __serializer__ = BulkTransactionSchema()

    def post(self):
        # request_data = self.serialize(self.payload(), load=True)
        request_data = self.serialize(self.payload())
        current_app.logger.info("Request Data......")
        current_app.logger.info(request_data)

        trx_ids = bulk_transaction(**request_data)
        return trx_ids, 202
