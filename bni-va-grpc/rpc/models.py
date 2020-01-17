"""
    Models
    _______________
"""
import random
from datetime import datetime, timedelta
import pytz

from mongoengine import Document, StringField, IntField, DateTimeField, fields
from rpc.config.external import BNI_ECOLLECTION, CUSTOM_PREFIX

TIMEZONE = pytz.timezone("Asia/Jakarta")


def generate_expired_at():
    """ generate date time for va so it always active """
    local_now = datetime.now(TIMEZONE)
    expire = timedelta(hours=int(BNI_ECOLLECTION["CREDIT_VA_EXPIRE"]))
    return local_now + expire


def generate_past_expired_at():
    """ generate date time for va so it always active """
    local_now = datetime.now(TIMEZONE)
    expire = timedelta(hours=int(BNI_ECOLLECTION["CREDIT_VA_EXPIRE"]) * 10)
    return local_now - expire


def update_document(document, data_dict):
    """ special method for updating document """

    def field_value(field, value):

        if field.__class__ in (fields.ListField, fields.SortedListField):
            return [field_value(field.field, item) for item in value]
        if field.__class__ in (
            fields.EmbeddedDocumentField,
            fields.GenericEmbeddedDocumentField,
            fields.ReferenceField,
            fields.GenericReferenceField,
        ):
            return field.document_type(**value)
        else:
            return value

    [
        setattr(document, key, field_value(document._fields[key], value))
        for key, value in data_dict.items()
    ]
    return document


class VirtualAccount(Document):
    """ Virtual Account ODM """

    account_no = StringField(required=True, unique=True)
    va_type = StringField(default="CREDIT")
    trx_id = StringField(required=True, unique=True)
    amount = IntField(default=0)
    name = StringField(required=True)
    phone_number = StringField(default="")
    expired_at = DateTimeField(required=True, default=generate_expired_at)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    updated_at = DateTimeField(required=True, default=datetime.utcnow)
    status = StringField(default="PENDING")

    def generate_trx_id(self):
        """ generate random trx id """
        while True:
            trx_id = random.randint(100000000, 999999999)
            # check trx id make sure it doesnt exist
            result = VirtualAccount.objects(trx_id=trx_id).first()
            if result is None:
                break
        self.trx_id = str(trx_id)
        return trx_id

    def generate_suffix(self, random_length):
        """ generate random number based on length """
        # generate 00000000 + 1
        zeroes = "0" * (int(random_length) - 1)
        start_point = int("1" + zeroes)
        # generate 999999999999
        end_point = int("9" * random_length)
        # generate random number between
        suffix = random.randint(start_point, end_point)
        return suffix

    def generate_va_number(self):
        """ generate va number """
        account_no = None
        # BNI VA Number
        while True:
            fixed = BNI_ECOLLECTION["VA_PREFIX"]
            length = BNI_ECOLLECTION["VA_LENGTH"]

            custom_prefix = ""
            if self.va_type == "CREDIT":
                client_id = BNI_ECOLLECTION["CREDIT_CLIENT_ID"]
            elif self.va_type == "INVESTMENT":
                client_id = BNI_ECOLLECTION["CREDIT_CLIENT_ID"]
                custom_prefix = CUSTOM_PREFIX[self.va_type]
            elif self.va_type == "REPAYMENT":
                client_id = BNI_ECOLLECTION["CREDIT_CLIENT_ID"]
                custom_prefix = CUSTOM_PREFIX[self.va_type]
            else:
                client_id = BNI_ECOLLECTION["DEBIT_CLIENT_ID"]
            # end if

            # calculate fixed length first
            prefix = len(fixed) + len(client_id)
            # calulcate free number
            # if its not custom prefix we just normal pattern
            random_length = length - prefix
            suffix = self.generate_suffix(random_length)
            account_no = str(fixed) + str(client_id) + str(suffix)

            if custom_prefix != "":
                random_length = length - prefix - len(custom_prefix)
                suffix = self.generate_suffix(random_length)
                account_no = (
                    str(fixed) + str(client_id) + str(custom_prefix) + str(suffix)
                )

            result = VirtualAccount.objects(account_no=account_no).first()
            if result is None:
                break
            # end if
        # end while
        self.account_no = account_no
        return account_no
