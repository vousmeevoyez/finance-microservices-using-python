from datetime import datetime

from bson import ObjectId
from umongo import Document, EmbeddedDocument
from umongo.fields import (
    EmbeddedField,
    ListField,
    DateTimeField,
    ObjectIdField,
    IntField,
    BooleanField,
    StrField,
)

from app.api import instance
from app.api.models.base import BaseDocument, BaseEmbeddedDocument


@instance.register
class TemplateEmbed(BaseEmbeddedDocument):
    subject = StrField(attribute="su")
    message = StrField(attribute="msg")


@instance.register
class Notification(BaseDocument):
    """ shared bank account embedded models """

    user_id = ObjectIdField()
    template = EmbeddedField(TemplateEmbed, attribute="tmp")
    type_ = StrField(attribute="tp")
    platform = StrField(attribute="pf")
    seen = BooleanField(attribute="se", default=True)

    class Meta:
        collection_name = "lender_notifications"
