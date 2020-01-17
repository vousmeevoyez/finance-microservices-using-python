"""
    Models
    _______________
"""
from datetime import datetime

from umongo import Document, EmbeddedDocument
from umongo import fields
from umongo.fields import (
    DecimalField,
    ObjectIdField,
    StrField,
    DateTimeField,
    EmbeddedField,
    ListField,
)

from app.api import instance


@instance.register
class InvestmentEmbed(EmbeddedDocument):
    investment_id = ObjectIdField()
    amount = DecimalField(default=0)


@instance.register
class Batch(Document):
    """ Virtual Account ODM """

    scheduled_at = DateTimeField(required=True)
    accumulated_amount = DecimalField(default=0)
    status = StrField(default="WAITING")  # COMPLETED | FAILED
    investments = ListField(EmbeddedField(InvestmentEmbed))
    created_at = DateTimeField(required=True, attribute="ca", default=datetime.utcnow)
    updated_at = DateTimeField(attribute="ua", default=datetime.utcnow)

    class Meta:
        collection_name = "lender_batch"
