"""
    REQUEST SCHEMA
"""
# pylint: disable=too-few-public-methods
# pylint: disable=bad-whitespace
# pylint: disable=import-error

from decimal import Decimal
from flask_restplus import reqparse


class TransactionRequestSchema:
    """Define all mandatory argument for creating transaction"""

    parser = reqparse.RequestParser()
    parser.add_argument("wallet_id", type=str, required=True)
    parser.add_argument("source_id", type=str, required=True)
    parser.add_argument("source_type", type=str, required=True)
    parser.add_argument("destination_id", type=str, required=True)
    parser.add_argument("destination_type", type=str, required=True)
    parser.add_argument("transaction_type", type=str, required=True)
    parser.add_argument("amount", type=Decimal, required=True)
    parser.add_argument("reference_no", type=str)


class BulkTransactionRequestSchema:
    """Define all mandatory argument for bulk transaction"""
    parser = reqparse.RequestParser()
    parser.add_argument("transactions", type=dict, action="append")
