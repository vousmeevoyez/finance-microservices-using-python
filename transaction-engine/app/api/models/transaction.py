"""
    Models
    _______________
"""
import random
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
from app.api.const import TYPE_TO_MODELS, PROVIDER_ROUTES, TRANSFER_TYPES
from app.api.models.bank import Bank
from app.api.lib.helper import str_to_class


def generate_trx_id():
    """ generate human friendly trx id based from time stamp"""
    value_date = datetime.utcnow().strftime("%Y%m%d%H%M")
    randomize = random.randint(10000, 99999)
    return str(value_date) + str(randomize)


@instance.register
class TransactionType(Document):
    """
        Represnt List of known Transaction Type:

        Top Up -> Virtual Account to RDL
        Investment -> RDL to Escrow
        Disbursement -> Escrow to Wallet
        Profit -> Escrow to Profit
        Bank Transfer -> RDL to Escrow
    """

    label = StrField()
    description = StrField()


@instance.register
class PaymentEmbed(EmbeddedDocument):
    """
        Represent actual payment that been made
    """

    source = StrField()  # VA /BANK ACC / RDL
    destination = StrField()  # VA / BANK ACC / RDL
    amount = DecimalField()
    payment_type = StrField(default="DEBIT")  # DEBIT | CREDIT
    bank_code = StrField()  # bank code / RTGS / etc...
    provider = StrField()  # BNI | BCA
    method = StrField()  # INHOUSE | INTERBANK
    status = StrField(default="PENDING")  # PENDING | COMPLETED | FAILED
    request_reference_no = StrField(allow_none=True)  # Request Payment references
    reference_no = StrField(allow_none=True)  # Payment references
    notes = StrField()  # Payment References
    created_at = DateTimeField(required=True, attribute="ca", default=datetime.utcnow)
    updated_at = DateTimeField(attribute="ua", default=datetime.utcnow)

    @staticmethod
    def _set_collection(type_):
        """ based on source & destination type
        we can decide what table to look up """
        return str_to_class(TYPE_TO_MODELS[type_])

    @staticmethod
    def _get_record(collection, collection_id, type_):
        """
            after having the collection to look up, collection id and type
            we can retrieve the bank account information that needed for
            payment purpose
            return bank account information or lending wallet info
        """
        if type_ == "INVESTOR_BANK_ACC":
            bank_account = collection().get_bank_account_using_id(collection_id)
        else:
            bank_account = collection().get_bank_account_using_id_label(
                collection_id, type_
            )

        bank = Bank.find_one({"id": bank_account["bid"]})
        # add bank code here
        bank_account["bank_code"] = bank.interbank_code
        return bank_account

    @staticmethod
    def _set_payment_type(amount):
        payment_type = "CREDIT"
        if amount < 0:
            payment_type = "DEBIT"
        return payment_type

    # @staticmethod
    # def _get_bank_code(destination):
    #    bank = Bank.find_one({"id": destination["bid"]})
    #    return bank.interbank_code

    @staticmethod
    def _match_method(source, destination, transaction_type):
        """ based on source and destination we return the matching method for
        this transaction """
        status = "PENDING"

        # first were going to check if current transaction ACTIVE or PASSIVE
        if transaction_type in TRANSFER_TYPES["ACTIVE"]:

            method = "INHOUSE_TRANSFER"

            if source["bank_code"] == "009" and destination["bank_code"] != "009":
                method = "INTERBANK_TRANSFER"

            # based on source account type we can decide what provider were
            # goint to use
            provider = PROVIDER_ROUTES[source["at"]]
        # if its INTERNAL
        elif transaction_type in TRANSFER_TYPES["INTERNAL"]:
            provider = "INTERNAL"
            method = "INTERNAL_TRANSFER"
        # if its PASSIVE
        elif transaction_type in TRANSFER_TYPES["PASSIVE"]:
            method = "DEPOSIT_CALLBACK"
            status = "COMPLETED"
            if transaction_type == "TOP_UP_RDL":
                provider = "BNI_RDL"
            else:
                provider = "BNI_VA"

        return provider, method, status

    def generate_payment_info(self, transaction):
        # first based on incoming source we decide which collection to look up
        source_collection = self._set_collection(transaction.source_type)
        destination_collection = self._set_collection(transaction.destination_type)

        # second after we get the right collection we look up the incoming
        # source id
        source_record = self._get_record(
            source_collection, transaction.source_id, transaction.source_type
        )
        destination_record = self._get_record(
            destination_collection,
            transaction.destination_id,
            transaction.destination_type,
        )
        # we generate right payment method and provider
        provider, method, status = self._match_method(
            source_record, destination_record, transaction.transaction_type
        )
        # we generate right payment type
        payment_type = self._set_payment_type(transaction.amount)

        self.source = source_record["ano"]
        self.destination = destination_record["ano"]
        self.bank_code = destination_record["bank_code"]
        self.provider = provider
        self.method = method
        self.payment_type = payment_type
        self.status = status


@instance.register
class Transaction(Document):
    """ Virtual Account ODM """

    trx_id = StrField(unique=True, default=generate_trx_id)
    wallet_id = ObjectIdField()
    source_id = ObjectIdField()  # OPTIONAL -> internal identifier can be RDL
    source_type = StrField()
    destination_id = ObjectIdField()
    destination_type = StrField()
    transaction_type = StrField()
    amount = DecimalField(default=0)
    balance = DecimalField(default=0)
    notes = StrField(allow_none=True)  # Payment references
    status = StrField(default="PENDING")
    payment = EmbeddedField(PaymentEmbed)
    transaction_link_id = ObjectIdField(default=None)  # OPTIONAL -> to link another trx
    created_at = DateTimeField(required=True, attribute="ca", default=datetime.utcnow)
    updated_at = DateTimeField(attribute="ua", default=datetime.utcnow)

    def load(self, generator):
        generator.load(self)

    class Meta:
        collection_name = "lender_transactions"
