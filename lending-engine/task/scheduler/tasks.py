import random
from datetime import datetime, date, timedelta

from bson.decimal128 import Decimal128
from bson import ObjectId

from flask import current_app
from celery.exceptions import (
    MaxRetriesExceededError
)

from app.api import (
    celery,
    sentry
)

from app.api.models.investment import Investment
from app.api.models.product import Product
from app.api.models.loan_request import LoanRequest

from app.config.worker import WORKER, RPC


def backoff(attempts):
    """ prevent hammering service with thousand retry"""
    return random.uniform(2, 4) ** attempts


def check_grace_period(due_date, grace_period, today):
    """ function to check whether today its still grace period or not """
    return due_date <= today <= due_date + timedelta(days=grace_period)


def check_write_off(overdue):
    """ function to check whether today write off or not """
    if overdue >= 89:
        return True
    return False


def calculate_rate(type_, amount):
    rate = amount
    if type_ == "PERCENT":
        rate = amount / 100
    return rate


def calculate_late_fee(type_, rate, loan_amount, overdue):
    # convert type and rate into fraction
    rate = calculate_rate(type_, rate)
    return loan_amount * overdue * rate


def calculate_splitted_profit(type_, rate, late_fee):
    investor_rate = calculate_rate(type_, rate)
    platform_rate = 1 - investor_rate
    return investor_rate * late_fee, platform_rate * late_fee


class SchedulerTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        sentry.captureException(exc)
        super(SchedulerTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        sentry.captureException(exc)
        # end with
        super(SchedulerTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def calculate_overdues(self):
        """ calculate all overdues for every loan request that has been
        disbursed """

        today = date.today()
        today_datetime = datetime.utcnow()

        overdue_loan_ids = []

        # we check is there any loan request that has been disbursed and have
        loan_requests = LoanRequest.get_with_product_info(
            {
                "st": "DISBURSED",
                "dd": {
                    "$lt": today_datetime
                }
            }
        )

        current_app.logger.info(
            "Today is: {}".format(today)
        )
        current_app.logger.info(
            "No of Disbursed Loan : {}".format(len(loan_requests))
        )

        for loan_request in loan_requests:
            # first we need to make sure today is past due date
            loan_request_id = str(loan_request["_id"])
            due_date = loan_request["dd"].date()  # convert datetime to date

            current_app.logger.info(
                "Loan {} is on due date: {}".format(
                    loan_request_id,
                    due_date
                )
            )
            grace_period = loan_request["product"]["interests"]["gp"]  # grace period
            current_overdue = loan_request["ov"]

            is_grace_period = check_grace_period(
                due_date,
                grace_period,
                today
            )

            current_app.logger.info(
                "Is grace period?: {}".format(is_grace_period)
            )

            # we increment the overdue
            LoanRequest.collection.update_one(
                {"_id": loan_request["_id"]},
                {
                    "$inc": {
                        "ov": 1
                    }
                }
            )

            # second we need to check grace period
            # only if its not grace period we mark it as tidak lancar
            current_app.logger.info(
                "current overdue: {}".format(current_overdue)
            )

            current_app.logger.info(
                "latest overdue: {}".format(current_overdue + 1)
            )
            if not is_grace_period:
                # if its already 89 days:
                if check_write_off(current_overdue):
                    current_app.logger.info(
                        "should mark as write off..."
                    )
                    LoanRequest.collection.update_one(
                        {"_id": loan_request["_id"]},
                        {"$set": {
                            "st": "WRITEOFF",
                            "psts": "MACET"
                        }}
                    )
                else:
                    current_app.logger.info(
                        "should mark as overdue..."
                    )

                    LoanRequest.collection.update_one(
                        {"_id": loan_request["_id"]},
                        {
                            "$set": {
                                "psts": "TIDAK_LANCAR"
                            }
                        }
                    )
                    overdue_loan_ids.append(loan_request_id)

        return overdue_loan_ids

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def calculate_late_fees(self, loan_request_ids):
        """ calculate late fees for every late loan """
        for loan_request_id in loan_request_ids:
            loan_request = LoanRequest.get_with_product_investor(
                {"_id": ObjectId(loan_request_id)}
            )[0]

            # fetch late fee and late fee type
            late_rate = loan_request["product"]["interests"]["lf"].to_decimal()
            late_rate_type = loan_request["product"]["interests"]["lft"]
            loan_amount = loan_request["lar"].to_decimal()
            overdue = loan_request["ov"]
            late_fee_date = loan_request["dd"] + timedelta(days=overdue)
            # calculate late fee
            late_fee = calculate_late_fee(
                late_rate_type,
                late_rate,
                loan_amount,
                overdue
            )
            # calculate how much platform and investor should earn here
            investor_late_rate = loan_request["investor"]["fees"][0]["lf"].to_decimal()
            investor_late_rate_type = loan_request["investor"]["fees"][0]["lft"]

            investor_profit, platform_profit = calculate_splitted_profit(
                investor_late_rate_type,
                investor_late_rate,
                late_fee
            )

            # new total fees based on new late fees
            investment = Investment.extract_investment_loan(loan_request_id)
            current_fee = investment["tafees"].to_decimal()
            new_fee = current_fee + late_fee

            current_app.logger.info(
                "Late Rate: {} {}".format(late_rate, late_rate_type)
            )
            current_app.logger.info("Late Date: {}".format(late_fee_date))
            current_app.logger.info("Loan amount: {}".format(loan_amount))
            current_app.logger.info("Overdue: {}".format(overdue))
            current_app.logger.info("Late Fee: {}".format(late_fee))
            current_app.logger.info(
                "Investor Rate: {} {}".format(
                    investor_late_rate,
                    investor_late_rate_type
                )
            )
            current_app.logger.info("Investor get : {}".format(investor_profit))
            current_app.logger.info("Platform get : {}".format(platform_profit))
            current_app.logger.info("Current Fee: {}".format(current_fee))
            current_app.logger.info("New Fee: {}".format(new_fee))

            # make sure we only calculate if the current loan amount less equal
            # max late fee
            max_late_rate = loan_request["product"]["interests"]["mlf"].to_decimal()
            max_late_fee = loan_amount * (max_late_rate/100)

            if new_fee <= max_late_fee:
                Investment.collection.update_one(
                    {
                        "_id": loan_request["investment_id"],
                        "lr.loanRequest_id": loan_request["_id"]
                    },
                    {
                        "$push": {
                            "lr.$.fees": {
                                "na": "lateFee",
                                "if": Decimal128(investor_profit),
                                "af": Decimal128(platform_profit),
                                "lf": Decimal128(late_fee),
                                "lfd": late_fee_date
                            }
                        }
                    }
                )

                LoanRequest.collection.update_one(
                    {"_id": loan_request["_id"]},
                    {
                        "$push": {
                            "lateFeeLog": {
                                "lfd": late_fee_date,
                                "lfa": Decimal128(late_fee),
                                "tpa": Decimal128(new_fee)
                            }
                        }
                    }
                )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def remind_before_due_dates(self):
        """ check all due dates and send notification """
        # we check is there any loan request have due date today
        morning = datetime.utcnow().replace(hour=0, minute=0)
        night = datetime.utcnow().replace(hour=23, minute=59)

        loan_requests = LoanRequest.get_with_product_info(
            {
                "st": "DISBURSED",
                "dd": {
                    "$gte": morning,
                    "$lt": night
                }
            }
        )

        current_app.logger.info(
            "No of due dates Loan : {}".format(len(loan_requests))
        )

        loan_request_ids = [{str(lr["_id"]), "BEFORE_DUE_DATE"} for lr in loan_requests]
        return loan_request_ids

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def remind_after_due_dates(self):
        """ check all due dates and send notification """
        # we check is there any loan request have due date today
        morning = datetime.utcnow().replace(hour=0, minute=0)
        night = datetime.utcnow().replace(hour=23, minute=59)

        loan_requests = LoanRequest.get_with_product_info(
            {
                "st": "DISBURSED",
                "dd": {
                    "$gte": morning,
                    "$lt": night
                }
            }
        )

        current_app.logger.info(
            "No of due dates Loan : {}".format(len(loan_requests))
        )

        loan_request_ids = [{str(lr["_id"]), "AFTER_DUE_DATE"} for lr in loan_requests]
        return loan_request_ids
