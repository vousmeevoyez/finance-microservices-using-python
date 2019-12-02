"""
    Document Models
"""
from datetime import datetime
from umongo.fields import ObjectIdField, StrField, DecimalField, DateTimeField
from app.api import instance
from app.api.models.base import BaseBankDocument


@instance.register
class Wallet(BaseBankDocument):
    """ Represent Object for maintaning balance """
    user_id = ObjectIdField()
    balance = DecimalField(default=0)
    label = StrField()
    wallet_type = StrField()  # INVESTOR | MASTER ACC | ETC
    pin = StrField()  # hashed wallet pin

    class Meta:
        collection_name = "lender_wallets"
