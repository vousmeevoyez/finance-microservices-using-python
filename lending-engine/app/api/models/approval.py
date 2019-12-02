from datetime import datetime
from bson.objectid import ObjectId

from umongo.fields import (
    EmbeddedField,
    ObjectIdField,
    StrField,
    DecimalField,
    DateTimeField,
    IntField,
    ListField
)
from app.api import instance
from app.api.models.base import BaseEmbeddedDocument


@instance.register
class ApprovalEmbed(BaseEmbeddedDocument):
    user_id = ObjectIdField(attribute="user_id")
    status = StrField(default="PENDING", attribute="st")
    approval_by = ObjectIdField(attribute="ab")
    approval_at = DateTimeField(default=datetime.utcnow, attribute="aa")
    message = StrField(attribute="msg")
    reason_id = ObjectIdField(allow_none=True)
    reviewer = StrField()
