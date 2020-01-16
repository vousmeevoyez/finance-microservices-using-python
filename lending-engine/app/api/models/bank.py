from datetime import datetime

from bson import ObjectId
from umongo import Document, EmbeddedDocument
from umongo.fields import (
    EmbeddedField,
    ListField,
    DateTimeField,
    ObjectIdField,
    IntField,
    StrField,
)

from app.api import instance
from app.api.models.base import BaseDocument


@instance.register
class Bank(BaseDocument):
    """ shared bank account embedded models """

    bank_name = StrField(attribute="bna")
    interbank_code = StrField(attribute="ic")
    clearing_code = StrField(attribute="cc")
    rtgs_code = StrField(attribute="rc")

    class Meta:
        collection_name = "lender_banks"
