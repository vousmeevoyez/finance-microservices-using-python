"""
    Handle Serialization from BNI Ecollection
"""
from datetime import datetime
from marshmallow import (
    Schema,
    fields,
    EXCLUDE,
    post_load,
    ValidationError
)
from rpc.models import VirtualAccount, generate_expired_at


class CreateVaSchema(Schema):
    """ schema used for created VA """
    va_type = fields.Str(missing="CREDIT")
    amount = fields.Int(missing=0)
    name = fields.Str(required=True)
    phone_number = fields.Str()
    expired_at = fields.Str(missing=generate_expired_at)

    def string_to_date(self, date):
        """ convert string into known date if supplied """
        return datetime.strptime(date, "%Y-%m-%d")

    @post_load
    def make_va(self, data, **kwargs):
        # we need to use sended va_type for generating va number
        va = VirtualAccount(**data)
        va.generate_trx_id()
        va.generate_va_number()
        va.save()
        return va.to_mongo()

    class Meta:
        unknown = EXCLUDE


class UpdateVaSchema(Schema):
    """ schema used for updating VA """
    account_no = fields.Str(required=True)
    trx_id = fields.Str()
    amount = fields.Int(missing=0)
    name = fields.Str(required=True)
    expired_at = fields.Method(deserialize="string_to_date")

    def string_to_date(self, date):
        return datetime.strptime(date, "%Y-%m-%d")

    class Meta:
        unknown = EXCLUDE


class InquiryVaSchema(Schema):
    """ schema for serialize / deserialize va inquiry from BNI """
    trx_id = fields.Str(dump_only=True)
    virtual_account = fields.Str(data_key="account_no")
    trx_amount = fields.Int(dump_only=True)
    customer_name = fields.Str(dump_only=True, data_key="name")
    customer_phone = fields.Str(dump_only=True, data_key="phone_number")
    customer_email = fields.Str(dump_only=True, data_key="email")
    datetime_created_iso8601 = fields.Str(dump_only=True, data_key="created_at")
    datetime_expired_iso8601 = fields.Str(dump_only=True, data_key="expired_at")
    datetime_payment_iso8601 = fields.Str(dump_only=True, data_key="paid_at")
    datetime_last_updated_iso8601 = fields.Str(dump_only=True, data_key="updated_at")
    payment_ntb = fields.Str(dump_only=True, data_key="ref_number")
    payment_amount = fields.Int(dump_only=True, data_key="paid_amount")
    va_status = fields.Method("va_status_to_status", data_key="status")
    description = fields.Str(dump_only=True)
    billing_type = fields.Str(dump_only=True)

    def va_status_to_status(self, obj):
        status = "ACTIVE"
        if obj["va_status"] == "2":
            status = "INACTIVE"
        return status


class GeneralVaSchema(Schema):
    """ schema for serialize / deserialize va from BNI """
    trx_id = fields.Str()
    virtual_account = fields.Str(data_key="account_no")
