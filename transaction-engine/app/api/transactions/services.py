"""
    Services Class
    _______________
    Handle logic to models or external party API
"""
from itertools import groupby
from bson import ObjectId

from app.api.models.transaction import Transaction
from app.api.models.wallet import Wallet
from app.api.transactions.factories.helper import process_transaction

from app.api.const import RESPONSE as error_response
from app.api.const import TRANSFER_TYPES
from app.api.lib.core.exceptions import BaseError
from app.api.lib.core.http_error import UnprocessableEntity


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
        reference_no=None,
        notes=None,
        child_transactions=None
):

    # first need to make sure the wallet balance is enough for this transaction
    # if its active
    if transaction_type in TRANSFER_TYPES["ACTIVE"]:
        wallet = Wallet.find_one({"id": ObjectId(wallet_id)})
        if wallet.balance < amount:
            raise UnprocessableEntity(
                error_response["INSUFFICIENT_BALANCE"]["TITLE"],
                error_response["INSUFFICIENT_BALANCE"]["MESSAGE"]
            )

    # trigger single ledger (DEBIT/CREDIT) transaction creation
    trx = process_transaction(
        wallet_id=wallet_id,
        source_id=source_id,
        source_type=source_type,
        destination_id=destination_id,
        destination_type=destination_type,
        amount=amount,
        transaction_type=transaction_type,
        reference_no=reference_no,
        notes=notes,
        child_transactions=child_transactions
    )
    return trx


def aggregate_by_destination_id(transactions, group_key="destination_id"):
    """ aggregate transactions by its destination so we know how much amount we should bulk transfer to destination """
    # first group transaction by its destination id
    groupped = groupby(transactions, lambda x: x.pop(group_key))
    result = []
    for item in groupped:
        # second initialize counter to count items
        groupped_sum = 0
        child_transactions = []
        destination_id = item[0]
        parent = {}

        for transaction in item[1]:
            # set all infromation to transaction info
            parent["reference_no"] = transaction.get("reference_no", None)
            parent["transaction_type"] = transaction["transaction_type"]
            parent["source_id"] = transaction["source_id"]
            parent["source_type"] = transaction["source_type"]
            parent["destination_id"] = destination_id
            parent["destination_type"] = \
                transaction["destination_type"]
            parent["wallet_id"] = \
                transaction["wallet_id"]
            # set missing destination id
            transaction["destination_id"] = destination_id
            groupped_sum += int(transaction["amount"])
            child_transactions.append(transaction)
        # end for
        parent["child_transactions"] = child_transactions
        parent["amount"] = groupped_sum
        result.append(parent)
    # end for
    return result


def bulk_transaction(transactions):
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
    if transaction.transactions != []:
        refunds += transaction.transactions

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
