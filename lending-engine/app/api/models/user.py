"""
    Document Models
"""
from datetime import datetime
from umongo import Document, EmbeddedDocument
from umongo.fields import (
    EmbeddedField,
    StrField,
    DateTimeField,
    ObjectIdField,
    ListField
)
from app.api import instance
from app.api.models.base import BaseDocument


@instance.register
class UserVaEmbed(EmbeddedDocument):
    """ embedded models for object inside """

    account_no = StrField(attribute="va")
    trx_id = StrField(attribute="trxId")
    wallet_id = StrField(attribute="walletId")


@instance.register
class User(BaseDocument):
    password = StrField(required=True, attribute="pa")
    email = StrField(required=True, attribute="em")
    account_type = StrField(required=True, attribute="at")
    msidn = StrField(required=True, attribute="mp")
    token = StrField(attribute="tn")
    otp_status = StrField(attribute="os")
    role = StrField(attribute="ro")
    employee_id = StrField(attribute="ei")
    device_id = StrField(attribute="di")
    otp_uuid = StrField(attribute="ou")
    email_code = StrField(attribute="emc")
    is_email_verified = StrField(attribute="iev")
    user_virtual_account = EmbeddedField(UserVaEmbed, attribute="uVA")
    next_payment_date = StrField(attribute="npd")
    investor_id = ObjectIdField()
    permissions = ListField(StrField())
    created_by = ObjectIdField(attribute="createdBy")
    name = StrField()

    class Meta:
        collection_name = "lender_users"
