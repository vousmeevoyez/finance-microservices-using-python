"""
    Services Class
    _______________
    Handle logic to models or external party API
"""
from collections import Counter
from bson import ObjectId

from app.api.models.transaction import Transaction
from app.api.transactions.factories.helper import process_transaction

from app.api.lib.core.exceptions import BaseError


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


def aggregate_by_destination_id(transactions):
    """ aggregate transactions by its destination so we know how much amount we
    should bulk transfer to destination """
    counter = Counter()
    for trx in transactions:
        counter[
            trx["source_id"],
            trx["source_type"],
            trx["destination_id"],
            trx["destination_type"],
            trx["transaction_type"],
            trx["wallet_id"]
        ] += int(trx['amount'])

    # after we got the aggregated result we revert back the result into the
    # original state
    dict_count = dict(counter)
    result = [{
        "source_id": k[0],
        "source_type": k[1],
        "destination_id": k[2],
        "destination_type": k[3],
        "transaction_type": k[4],
        "wallet_id": k[5],
        "amount": v
    } for k, v in dict_count.items()]
    return result


def bulk_transaction(
        transactions
):
    # we group transaction based on its destination so let say if there 10
    # transaction have source a and destination b we aggregate it into 1
    # transaction a to b with total amount of 10 transaction

    # first we aggregate transaction so we know total amount that we have to
    # transfer for certain destination id
    aggregated_transactions = aggregate_by_destination_id(transactions)
    result = []
    for transaction in aggregated_transactions:
        trx_id = single_transaction(**transaction)
        result.append(str(trx_id))
    return result


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

        # if its debit then we should revert - to +
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
