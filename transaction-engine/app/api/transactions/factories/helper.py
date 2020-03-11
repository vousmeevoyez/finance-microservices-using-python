from bson import ObjectId
from pymongo.errors import ConnectionFailure, OperationFailure

from app.api.models.transaction import (
    Transaction,
    PaymentEmbed,
    ChildTransactionEmbed
)
from app.api.transactions.factories.transactions.factory import generate_transaction
from app.api.lib.core.exceptions import BaseError


class TransactionError(BaseError):
    """ raised when failed to create transaction !"""


def process_child_transactions(child_transactions):
    # we need to create child transactions embed here
    transactions = []
    for child in child_transactions:
        child_transaction = ChildTransactionEmbed(
            wallet_id=ObjectId(child["wallet_id"]),
            source_id=ObjectId(child["source_id"]),
            source_type=child["source_type"],
            destination_id=ObjectId(child["destination_id"]),
            destination_type=child["destination_type"],
            amount=child["amount"],
            transaction_type=child["transaction_type"]
        )
        transactions.append(child_transaction)
    return transactions


def process_transaction(
        wallet_id,
        source_id,
        source_type,
        destination_id,
        destination_type,
        amount,
        transaction_type,
        child_transactions=None,
        reference_no=None,
        notes=None
):

    # first we need to convert every incoming string with object id
    source_id = ObjectId(source_id)
    destination_id = ObjectId(destination_id)
    wallet_id = ObjectId(wallet_id)

    # if there's child we add it
    transactions = []
    if child_transactions is not None:
        transactions = process_child_transactions(child_transactions)


    # second we create the actual transaction object that going to be inserted
    transaction = Transaction(
        wallet_id=wallet_id,
        source_id=source_id,
        source_type=source_type,
        destination_id=destination_id,
        destination_type=destination_type,
        amount=amount,
        transaction_type=transaction_type,
        notes=notes,
        transactions=transactions
    )

    # third we generate payment
    # using transaction we can generate the right payment for transaction
    payment = PaymentEmbed()
    payment.generate_payment_info(transaction)
    payment.reference_no = reference_no

    transaction.payment = payment
    transaction.commit()

    transaction = generate_transaction(transaction, transaction_type)
    return transaction
