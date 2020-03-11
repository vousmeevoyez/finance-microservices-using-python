"""
    Transaction Task Modules
"""
import requests
from bson import ObjectId
from itertools import groupby


import pymongo
from pymongo import UpdateOne

from flask import current_app
from celery.exceptions import (
    MaxRetriesExceededError
)

from task.tasks import BaseTask

from app.api import (
    celery
)
from app.api.lib.helper import str_to_class
from app.api.lib.utils import backoff

from app.api.models.base import StatusEmbed
from app.config.worker import WORKER, HTTP


class TransactionTask(BaseTask):
    """Abstract base class for all tasks in my app."""

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def send_transaction(self, wallet_id, source_id, source_type,
                         destination_id, destination_type, amount,
                         transaction_type, reference_no=None, notes=None,
                         model=None, model_id=None, status=None):
        """ execute HTTP Api call to transaction engine where the actual
        transaction created """

        # prepare HTTP Request to Transaction Engine
        base_url = HTTP["TRANSACTION_ENGINE"]["BASE_URL"]
        endpoint = HTTP["TRANSACTION_ENGINE"]["API"]["CREATE"]
        url = base_url + endpoint
        payload = {
            "wallet_id": wallet_id,
            "source_id": source_id,
            "source_type": source_type,
            "destination_id": destination_id,
            "destination_type": destination_type,
            "amount": amount,
            "transaction_type": transaction_type,
            "reference_no": reference_no,
            "notes": notes
        }

        try:
            current_app.logger.info("Send to Transaction engine ..")
            current_app.logger.info(payload)
            r = requests.post(url, data=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                current_app.logger.info(exc)
        else:
            transaction_id = r.json()["id"]
            return {
                "transaction_id": transaction_id,
                "model": model,
                "model_id": model_id,
                "status": status
            }

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def send_bulk_transaction(self, transactions, update_records):
        """ execute HTTP Api call to transaction engine where the bulk
        transaction created """

        # prepare HTTP Request to Transaction Engine
        base_url = HTTP["TRANSACTION_ENGINE"]["BASE_URL"]
        endpoint = HTTP["TRANSACTION_ENGINE"]["API"]["BULK_CREATE"]
        url = base_url + endpoint

        payload = {
            "transactions": transactions
        }

        try:
            current_app.logger.info("Send to Transaction engine ..")
            current_app.logger.info(payload)
            r = requests.post(url, json=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                current_app.logger.info(exc)
        else:
            transaction_ids = r.json()
            return {
                "transaction_ids": transaction_ids,
                "update_records": update_records # all record we need t update
            }

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def map_transaction(self, transaction_result):
        """ function to map transaction id that generated into model """
        model = transaction_result["model"]
        model_id = transaction_result["model_id"]
        transaction_id = transaction_result["transaction_id"]
        status = transaction_result["status"]

        # convert string into actual model object
        object_ = str_to_class(model)

        with current_app.connection.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                try:
                    object_.collection.update_one(
                        {"_id": ObjectId(model_id)},
                        {"$push": {
                            "lst": {
                                "transaction_id": ObjectId(transaction_id),
                                "st": status
                            }
                        }},
                        session=session
                    )
                    session.commit_transaction()
                except (
                        pymongo.errors.ConnectionFailure,
                        pymongo.errors.OperationFailure,
                ) as exc:
                    current_app.logger.info("retry map transaction {} ... ".format(
                        transaction_id
                    ))
                    self.retry(exc=exc)

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def map_bulk_transaction(self, transaction_result):
        """ function to map transaction id that generated into model """
        transaction_ids = transaction_result["transaction_ids"]
        update_records = transaction_result["update_records"]

        for transaction_id in transaction_ids:
            # first group update records by its own model / collection
            groupped_models = groupby(update_records, lambda x: x.pop("model"))
            for model in groupped_models:
                model_name = model[0]
                # populate operation here
                operations = []
                for data in model[1]:
                    operation = UpdateOne(
                        {"_id": ObjectId(data["model_id"])},
                        {"$push": {
                            "lst": {
                                "transaction_id":
                                ObjectId(transaction_id),
                                "st": data["status"]
                            }
                        }}
                    )
                    operations.append(operation)
                # end for
                # apply all bulk here
                is_updated = False
                actual_model = str_to_class(model_name)
                while is_updated is False:
                    actual_model = str_to_class(model_name)
                    result = actual_model.collection.bulk_write(operations)

                    if result.modified_count != 0:
                        is_updated = True
            # end for
        # end for
