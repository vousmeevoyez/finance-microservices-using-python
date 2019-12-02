from datetime import datetime

from bson import ObjectId
from umongo import Document, EmbeddedDocument
from umongo.fields import (
    EmbeddedField,
    ListField,
    DateTimeField,
    ObjectIdField,
    IntField,
    StrField
)

from app.api import instance
from app.api.const import TYPE_TO_BANK_TYPES
from app.api.lib.core.exceptions import BaseError


class TransactionStatusNotFound(BaseError):
    """ raised when transaction inside status not found """


@instance.register
class BaseEmbeddedDocument(EmbeddedDocument):
    id = ObjectIdField(attribute="_id", default=ObjectId)
    ca = DateTimeField(default=datetime.utcnow)
    ua = DateTimeField(default=datetime.utcnow)


@instance.register
class BaseDocument(Document):
    version = IntField(attribute="__v")
    ca = DateTimeField(default=datetime.utcnow)
    ua = DateTimeField(default=datetime.utcnow)

    class Meta:
        abstract = True
        allow_inheritance = True


@instance.register
class BankAccEmbed(BaseEmbeddedDocument):
    """ shared bank account embedded models """
    bank_id = ObjectIdField(attribute="bid")
    bank_name = StrField(attribute="bn")
    account_no = StrField(attribute="ano")
    account_name = StrField(attribute="an")
    account_type = StrField(attribute="at")
    label = StrField(allow_none=True)


@instance.register
class StatusEmbed(BaseEmbeddedDocument):
    """ shared status embedded models """
    transaction_id = ObjectIdField()
    status = StrField(attribute="st")
    message = StrField(attribute="msg")


@instance.register
class BaseBankDocument(BaseDocument):
    status = StrField(
        attribute="st"
    )
    bank_accounts = ListField(
        EmbeddedField(BankAccEmbed),
        attribute="ba",
        default=list
    )
    list_of_status = ListField(
        EmbeddedField(StatusEmbed),
        attribute="lst",
        default=list
    )

    class Meta:
        abstract = True
        allow_inheritance = True

    def get_bank_account_using_id_label(self, _id, type_):
        """ common inteface for all base document that store bank accounts """
        # generate matcher and projection here
        matchers = []
        projections = []
        if isinstance(TYPE_TO_BANK_TYPES[type_], dict):
            account_type = TYPE_TO_BANK_TYPES[type_]["ACCOUNT_TYPE"]
            label = TYPE_TO_BANK_TYPES[type_]["LABEL"]
            matchers.append({"at": account_type})
            matchers.append({"label": label})
            projections.append({"$eq": ["$$ba.at", account_type]})
            projections.append({"$eq": ["$$ba.label", label]})
        else:
            account_type = TYPE_TO_BANK_TYPES[type_]
            matchers.append({"at": account_type})
            projections.append({"$eq": ["$$ba.at", account_type]})

        result = self.collection.aggregate(
            [
                {
                    "$match": {
                        "_id": _id,
                        "ba": {
                            "$elemMatch": {"$and": matchers}
                        },
                    }
                },
                {
                    "$project": {
                        "ba": {
                            "$filter": {
                                "input": "$ba",
                                "as": "ba",
                                "cond": {
                                    "$and": projections
                                },
                            }
                        }
                    }
                },
            ]
        )
        # get the very first array
        bank_accounts = list(result)[0]
        return bank_accounts["ba"][0]

    def get_bank_account_using_id(self, _id):
        """ common inteface for all base document that store bank accounts """
        # generate matcher and projection here
        result = self.collection.aggregate(
            [
                {
                    "$match": {
                        "ba": {
                            "$elemMatch": {"$and": [{
                                "_id": ObjectId(_id)
                            }]}
                        },
                    }
                },
                {
                    "$project": {
                        "ba": {
                            "$filter": {
                                "input": "$ba",
                                "as": "ba",
                                "cond": {
                                    "$and": [{
                                        "$eq": ["$$ba._id", ObjectId(_id)]
                                    }]
                                },
                            }
                        }
                    }
                },
            ]
        )
        # get the very first array
        bank_accounts = list(result)[0]
        return bank_accounts["ba"][0]

    def get_by_transaction(self, transaction_id):
        """ common inteface for all base document that store status """
        # generate matcher and projection here
        result = self.collection.aggregate([
                {
                    "$match": {
                        "lst": {
                            "$elemMatch": {
                                "$and": [{"transaction_id": ObjectId(transaction_id)}]
                            }
                        },
                    }
                },
                {
                    "$project": {
                        "_id": 1
                    }
                }
        ])
        lists = list(result)
        try:
            transaction = lists[0]["_id"]
        except IndexError:
            raise TransactionStatusNotFound
        return transaction
