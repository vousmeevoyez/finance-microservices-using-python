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
    StrField
)

from app.api import instance
from app.api.models.base import BaseDocument


@instance.register
class File(BaseDocument):
    """ shared bank account embedded models """
    borrower_id = ObjectIdField()
    user_id = ObjectIdField()
    file_type = StrField(attribute="ft")
    file_id = StrField()
    is_valid = BooleanField(attribute="iv")
    is_deleted = BooleanField(attribute="id")
    same_as_hr = BooleanField(attribute="sh")
    mime_type = StrField(attribute="mt")

    class Meta:
        collection_name = "lender_files"


@instance.register
class Article(BaseDocument):
    """ shared bank account embedded models """
    file_type = StrField(attribute="ft")
    id_ = BooleanField(attribute="id")
    type_ = StrField(attribute="t")
    content = StrField(attribute="c")
    is_active = BooleanField(attribute="ia")
    create_by = ObjectIdField(attribute="cb")
    language = StrField(attribute="l")

    class Meta:
        collection_name = "lender_files"
