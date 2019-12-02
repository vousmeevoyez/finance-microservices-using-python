"""
    Handle Serialization from BNI Ecollection
"""
from datetime import datetime
from marshmallow import Schema, fields, EXCLUDE


class TransferInquirySchema(Schema):
    """ schema used for get payment status """

    debitAccountNo = fields.Str(data_key="source")
    creditAccountNo = fields.Str(data_key="destination")
    transactionStatus = fields.Str(data_key="status")
    valueAmount = fields.Float(data_key="amount")

    class Meta:
        unknown = EXCLUDE
