"""
    Health Services
    ______________
    module to check health for db, external service, etc...
"""
import re
import sys

from celery import group

from flask import current_app
from umongo.exceptions import UMongoError

from app.api import sentry
from app.api.models.user import User

# task
from task.investment.tasks import InvestmentTask
from task.investor.tasks import InvestorTask
from task.scheduler.tasks import SchedulerTask
from task.transaction.tasks import TransactionTask
from task.utility.tasks import UtilityTask
from task.virtual_account.tasks import VirtualAccountTask


def str_to_class(class_name):
    return getattr(sys.modules[__name__], class_name)


class HealthServices:
    @staticmethod
    def _check_db():
        """ method to check db that we connect """
        try:
            User.collection.find_one({})
        except UMongoError as e:
            if not current_app.testing and not current_app.debug:
                sentry.captureException(e)
            # end if
            return False
        # end try
        return True

    # end def

    @staticmethod
    def _convert_state_to_bool(task):
        """ convert known celery task state into boolean """
        worker_status = True
        if task.completed_count() != 4:  # no of known worker
            worker_status = False
        return worker_status

    # end def

    @staticmethod
    def _convert_http_to_bool(status_code):
        """ convert known http status code from external service into boolean """
        result = True
        if status_code != 200:
            result = False
        return result

    # end def

    @staticmethod
    def _calculate_length(_dict):
        length = 0
        for key, value in _dict.items():
            if isinstance(value, dict):
                for key, value in value.items():
                    length += 1
                # end for
            else:
                length += 1
            # end if
        # end for
        return length

    def _convert_to_percentage(self, _dict):
        # first check how many item inside dict
        length = self._calculate_length(_dict)
        score = 0
        for key, value in _dict.items():
            if isinstance(value, dict):
                for key, value in value.items():
                    if value:
                        score += 1
                    # end if
                # end for
            elif value:
                score += 1
            # end if
        # end for
        return round(score / length * 100, 1)

    def _snake_to_camel(self, word):
        return ''.join(x.capitalize() or '_' for x in word.split('_'))

    def _check_worker(self):
        """ method to check all worker that we connect """
        # iterate to all known worker
        QUEUES = current_app.config["CELERY_QUEUES"]

        workers = []
        for key, value in QUEUES.items():
            if value["exchange"] != "default":
                workers.append(value)

        job_group = group(
            [
                str_to_class(self._snake_to_camel(wrk["exchange"]) + "Task")()
                .health_check.s("CHECK")
                .set(queue=wrk["exchange"])
                for wrk in workers
            ]
        )

        result = job_group.apply_async()
        return self._convert_state_to_bool(result)

    def check(self):
        """ inteface method to check various health modules """
        health_status = {}
        # check db connection
        health_status["db"] = self._check_db()
        # check worker connection
        health_status["worker"] = self._check_worker()
        # calcaulate overall percentage of current health
        health_status["hp"] = self._convert_to_percentage(health_status)
        return health_status
