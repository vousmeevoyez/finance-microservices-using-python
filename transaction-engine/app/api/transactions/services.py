"""
    Services Class
    _______________
    Handle logic to models or external party API
"""
from bson import ObjectId

from app.api.lib.core.exceptions import BaseError
from app.api.models.transaction import Transaction
from app.api.transactions.factories.helper import process_transaction


class ServicesError(BaseError):
    """ error raised when something wrong at services """


def single_transaction(
        wallet_id,
        source_id,
        source_type,
        destination_id,
        destination_type,
        amount,
        transaction_type,
        reference_no=None
):
    # trigger single ledger (DEBIT/CREDIT) transaction creation
    trx = process_transaction(
        wallet_id=wallet_id,
        source_id=source_id,
        source_type=source_type,
        destination_id=destination_id,
        destination_type=destination_type,
        amount=amount,
        transaction_type=transaction_type,
        reference_no=reference_no
    )
    return trx


def refund(transaction_id):
    """ transaction refund """
    # first need to check status of each transaction
    transaction = Transaction.find_one({"_id": ObjectId(transaction_id)})
    if transaction is None:
        raise ServicesError(message="transaction not found")

    # second make sure transaction is not CANCELLED
    if transaction.status == "CANCELLED":
        raise ServicesError(message="transaction already refunded")

    # need to check if this transaction linked together or not
    refunds = []
    refunds.append(transaction.id)
    if transaction.transaction_link_id is not None:
        refunds.append(transaction.transaction_link_id)

    refund_result = []
    for item in refunds:
        transaction = Transaction.find_one({"_id": ObjectId(item)})

        refunded_amount = int(-transaction.amount)
        refund_transaction_type = "CREDIT_REFUND"

        if transaction.payment.payment_type == "DEBIT":
            refunded_amount = abs(transaction.amount)
            refund_transaction_type = "DEBIT_REFUND"

        refund_trx_id = process_transaction(
            wallet_id=transaction.wallet_id,
            source_id=transaction.source_id,
            source_type=transaction.source_type,
            destination_id=transaction.destination_id,
            destination_type=transaction.destination_type,
            amount=refunded_amount,
            transaction_type=refund_transaction_type,
        )

        transaction = Transaction.collection.update_one(
            {"_id": ObjectId(item)}, {"$set": {"status": "CANCELLED"}}
        )
        refund_result.append(str(refund_trx_id))
    return refund_result


def get_all():
    """ get all transactions """
    # first need to check status of each transaction
    transactions = Transaction.find()
    transactions = [trx.dump() for trx in transactions]
    return transactions
