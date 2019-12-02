"""
    This is Celery Task that actually apply transaction
"""
import random
from bson import ObjectId
from bson.decimal128 import Decimal128

from datetime import datetime

import pymongo

from flask import current_app
from app.api import sentry, celery

from app.api.models.transaction import Transaction, PaymentEmbed
from app.api.models.wallet import Wallet

# const
from app.api.const import WORKER


def backoff(attempts):
    """ prevent hammering service with thousand retry"""
    return random.uniform(2, 4) ** attempts


class TransactionTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        sentry.captureException(exc)
        super(TransactionTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        sentry.captureException(exc)
        super(TransactionTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def apply(self, transaction_id):
        """ background to really apply the transaction to completed and deduct
        balance """

        # begin mongo session here
        with current_app.connection.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                try:
                    # fetch transaction first to get transaction info
                    transaction = Transaction.find_one({
                        "_id": ObjectId(transaction_id)
                    })
                    current_trx_amount = int(transaction.amount)

                    # fetch wallet to get latest wallet info
                    wallet = Wallet.find_one({"_id": transaction.wallet_id})
                    current_balance = wallet.balance

                    # deduct wallet balance based on how much the transactioin
                    wallet = Wallet.collection.update_one(
                        {"_id": transaction.wallet_id},
                        {"$inc": {"balance": current_trx_amount}},
                        session=session,
                    )

                    # finally apply balance based on current balance -
                    # transaction amount
                    after_balance = current_balance + current_trx_amount
                    Transaction.collection.update_one(
                        {"_id": ObjectId(transaction_id)},
                        {"$set": {
                            "status": "APPLIED",
                            "balance": Decimal128(after_balance)
                        }}
                    )

                    session.commit_transaction()

                except (
                    pymongo.errors.ConnectionFailure,
                    pymongo.errors.OperationFailure,
                ) as exc:
                    current_app.logger.info("retry.. ".format(transaction_id))
                    self.retry(countdown=backoff(self.request.retries), exc=exc)
