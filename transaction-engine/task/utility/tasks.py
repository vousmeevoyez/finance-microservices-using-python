"""
    Utility Task modules
"""
import requests
from bson import ObjectId

from flask import current_app
from celery.exceptions import MaxRetriesExceededError

from app.api.models.transaction import Transaction
from app.api.models.base import StatusEmbed

from app.api.const import WORKER
from app.config.worker import HTTP

from task.base import celery, fast_backoff, BaseTask


class UtilityTask(BaseTask):
    """ all task related to utility like sending notif to lending engine """

    @celery.task(
        bind=True,
        max_retries=WORKER["TRANSACTION_MAX_RETRIES"],
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
            "status": transaction.payment.status,
        }

        try:
            current_app.logger.info("Notify Lending Engine...")
            current_app.logger.info(payload)
            r = requests.post(url, json=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            try:
                self.retry(countdown=fast_backoff())
            except MaxRetriesExceededError:
                current_app.logger.info(exc)
        else:
            return r.json()["status"]
