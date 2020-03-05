"""
    This is Celery Task that actually apply transaction
"""
import random
from bson import ObjectId
from bson.decimal128 import Decimal128

from datetime import datetime

import pymongo
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

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
        with current_app.connection.start_session(
            causal_consistency=True
        ) as session:
            with session.start_transaction(
                    read_concern=ReadConcern("majority"),
                    write_concern=WriteConcern("majority")
            ):
                try:
                    # start locking the transaction
                    transaction_lock = ObjectId()
                    transaction = Transaction.collection.find_one_and_update(
                        {"_id": ObjectId(transaction_id)},
                        {
                            "$set": {
                                "lock": transaction_lock
                            }
                        }
                    )

                    # deduct wallet balance based on how much the transactioin
                    wallet = Wallet.collection.find_one_and_update(
                        {"_id": transaction["wallet_id"]},
                        {
                            "$set": {
                                "lock": ObjectId(),
                            },
                            "$inc": {
                                "balance": transaction["amount"]
                            }
                        },
                        session=session
                    )

                    # finally apply balance based on current balance -
                    # transaction amount
                    after_balance = wallet["balance"].to_decimal() + \
                        transaction["amount"].to_decimal()
                    if after_balance < 0:
                        session.abort_transaction()
                        self.retry()

                    Transaction.collection.find_one_and_update(
                        {"_id": ObjectId(transaction_id)},
                        {
                            "$set": {
                                "status": "APPLIED",
                                "balance": Decimal128(after_balance)
                            },
                            "$unset": {"lock": transaction_lock}
                        },
                        session=session
                    )

                    session.commit_transaction()

                except (
                        pymongo.errors.ConnectionFailure,
                        pymongo.errors.OperationFailure,
                        pymongo.errors.InvalidOperation,
                ) as exc:
                    current_app.logger.info("retry.{}".format(transaction_id))
                    session.abort_transaction()
                    self.retry(
                        countdown=1,
                        exc=exc
                    )
