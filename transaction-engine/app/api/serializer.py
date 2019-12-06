"""
    Serializer & Deserialize
"""
from marshmallow import fields, ValidationError, validates, post_load

from app.api import ma


class TrxSchema(ma.Schema):
    """ this is class schema for transaction """

    wallet_id = fields.Str(required=True)
    source_id = fields.Str(required=True)
    source_type = fields.Str(required=True)
    destination_id = fields.Str(required=True)
    destination_type = fields.Str(required=True)
    amount = fields.Float(required=True)
    transaction_type = fields.Str(required=True)
    reference_no = fields.Str()


class BulkTrxSchema(ma.Schema):
    """ this is class for bulk create transaction """
    transactions = fields.Nested(TrxSchema, many=True)
