import requests
import random
from bson import ObjectId

from flask import current_app
from celery.exceptions import (
    MaxRetriesExceededError
)

from app.api import (
    celery,
    sentry
)
from app.api.models.transaction import Transaction
from app.api.models.base import StatusEmbed
from app.config.worker import WORKER, HTTP


def backoff(attempts):
    """ prevent hammering service with thousand retry"""
    return random.uniform(2, 4) ** attempts


class UtilityTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        sentry.captureException(exc)
        super(UtilityTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        sentry.captureException(exc)
        # end with
        super(UtilityTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def notify(self, transaction_id):
        """ send notification transaction services """
        transaction = Transaction.find_one({"id": ObjectId(transaction_id)})

        base_url = HTTP["LENDING_ENGINE"]["BASE_URL"]
        endpoint = HTTP["LENDING_ENGINE"]["API"]["CALLBACK"]
        url = base_url + endpoint

        payload = {
            "transaction_id": transaction_id,
            "transaction_type": transaction.transaction_type,
            "status": transaction.payment.status
        }

        try:
            current_app.logger.info("Notify Lending Engine...")
            current_app.logger.info(payload)
            r = requests.post(url, json=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                current_app.logger.info(exc)
        else:
            return r.json()["status"]
