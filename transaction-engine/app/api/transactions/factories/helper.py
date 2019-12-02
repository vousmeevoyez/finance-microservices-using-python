from bson import ObjectId
from pymongo.errors import ConnectionFailure, OperationFailure

from app.api.models.transaction import Transaction, PaymentEmbed
from app.api.transactions.factories.transactions.factory import generate_transaction
from app.api.lib.core.exceptions import BaseError


class TransactionError(BaseError):
    """ raised when failed to create transaction !"""


def process_transaction(
    wallet_id,
    source_id,
    source_type,
    destination_id,
    destination_type,
    amount,
    transaction_type,
    reference_no=None
):

    # first we need to convert every incoming string with object id
    source_id = ObjectId(source_id)
    destination_id = ObjectId(destination_id)
    wallet_id = ObjectId(wallet_id)

    # second we create the actual transaction object that going to be inserted
    transaction = Transaction(
        wallet_id=wallet_id,
        source_id=source_id,
        source_type=source_type,
        destination_id=destination_id,
        destination_type=destination_type,
        amount=amount,
        transaction_type=transaction_type,
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
