"""
    Models
    _______________
"""
from datetime import datetime

from umongo.fields import (
    EmbeddedField,
    StrField,
    ListField,
    ObjectIdField,
    DateTimeField,
    DecimalField,
)

from app.api import instance
from app.api.models.base import BaseDocument, BaseEmbeddedDocument, BaseBankDocument


@instance.register
class Schedule(BaseDocument):
    """ Schedule Model """

    name = StrField()
    start = StrField()
    end = StrField()
    executed_at = StrField()

    class Meta:
        collection_name = "lender_schedules"


@instance.register
class TransactionInfoEmbed(BaseEmbeddedDocument):
    """ transaction info embedded Model """

    model = StrField()
    model_id = StrField()
    status = StrField()


@instance.register
class TransactionQueue(BaseDocument):
    """ transaction queue """

    status = StrField(default="WAITING")
    schedule_id = ObjectIdField()
    wallet_id = ObjectIdField()
    source_id = ObjectIdField()
    source_type = StrField()
    destination_id = ObjectIdField()
    destination_type = StrField()
    transaction_type = StrField()
    amount = DecimalField(default=0)
    request_transaction_id = ObjectIdField()
    transaction_info = EmbeddedField(TransactionInfoEmbed)

    class Meta:
        collection_name = "lender_queue"
