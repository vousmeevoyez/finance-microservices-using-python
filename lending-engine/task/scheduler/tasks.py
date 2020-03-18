import io
import pytz
import requests
from datetime import datetime, date, timedelta

from bson.decimal128 import Decimal128
from bson import ObjectId

from flask import current_app
from celery.exceptions import (
    MaxRetriesExceededError
)

from task.tasks import BaseTask

from app.api import (
    celery
)

from app.api.models.user import User
from app.api.models.borrower import Borrower
from app.api.models.investment import Investment
from app.api.models.product import Product
from app.api.models.loan_request import LoanRequest
from app.api.models.batch import Schedule, TransactionQueue
from app.api.models.report import RegulationReport

from app.api.batch.modules.services import (
    check_executed_schedule,
    convert_start_end_to_datetime
)
from app.api.report.modules.services import (
    DateTimeReportServices,
    IdReportServices,
    ReportServicesError
)

from task.transaction.tasks import TransactionTask

from app.api.lib.helper import send_notif
from app.api.lib.utils import backoff

from app.api.const import LOAN_QUALITIES
from app.config.worker import WORKER, RPC
from app.config.external.analyst import ANALYST_BE


TIMEZONE = pytz.timezone("Asia/Jakarta")


def check_grace_period(due_date, grace_period, today):
    """ function to check whether today its still grace period or not """
    return due_date <= today <= due_date + timedelta(days=grace_period)


def determine_loan_quality(overdue):
    """ function to check whether today write off or not """
    loan_status = "DISBURSED"
    # start + operator + overdue + operator + end
    # x <= overdue <= y
    if eval(
            LOAN_QUALITIES["LANCAR"]["start"]
            + LOAN_QUALITIES["LANCAR"]["operator"]
            + str(overdue)
            + LOAN_QUALITIES["LANCAR"]["operator"]
            + LOAN_QUALITIES["LANCAR"]["end"]
    ):
        payment_status = "LANCAR"
    elif eval(
            LOAN_QUALITIES["TIDAK_LANCAR"]["start"]
            + LOAN_QUALITIES["TIDAK_LANCAR"]["operator"]
            + str(overdue)
            + LOAN_QUALITIES["TIDAK_LANCAR"]["operator"]
            + LOAN_QUALITIES["TIDAK_LANCAR"]["end"]
    ):
        payment_status = "TIDAK_LANCAR"
    elif eval(
            LOAN_QUALITIES["MACET"]["start"]
            + LOAN_QUALITIES["MACET"]["operator"]
            + str(overdue)
    ):
        loan_status = "WRITEOFF"
        payment_status = "MACET"
    return loan_status, payment_status


def calculate_rate(type_, amount):
    rate = amount
    if type_ == "PERCENT":
        rate = amount / 100
    return rate


def send_borrower_notif(borrower_id, notif_type, loan_request_id):
    """ wrapper function to help borrower notif """
    borrower = Borrower.find_one({"id": borrower_id})
    user = User.find_one({"id": borrower.user_id})
    loan = LoanRequest.find_one({"id": loan_request_id})

    email_notif, in_app_notif = send_notif(
        recipient=borrower.email,
        user_id=borrower.user_id,
        notif_type=notif_type,
        platform="mobile",
        device_token=user.device_id,
        custom_content={
            "loan_request_code": loan.loan_request_code
        }
    )


def calculate_late_fee(type_, rate, loan_amount, overdue):
    # convert type and rate into fraction
    rate = calculate_rate(type_, rate)
    return loan_amount * overdue * rate


def calculate_splitted_profit(type_, rate, late_fee):
    investor_rate = calculate_rate(type_, rate)
    platform_rate = 1 - investor_rate
    return investor_rate * late_fee, platform_rate * late_fee


class SchedulerTask(BaseTask):
    """Abstract base class for all tasks in my app."""

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
                loan_status, payment_status = \
                    determine_loan_quality(current_overdue + 1)

                if payment_status == "MACET":
                    current_app.logger.info(
                        "should mark as write off..."
                    )
                    LoanRequest.collection.update_one(
                        {"_id": loan_request["_id"]},
                        {"$set": {
                            "st": loan_status,
                            "psts": payment_status,
                            "wda": today_datetime
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
                                "psts": payment_status
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
        # we check is there any loan request that has been disbursed and have
        # due date today
        morning = datetime.now().replace(
            tzinfo=TIMEZONE,
            hour=0,
            minute=0
        )

        night = datetime.now().replace(
            tzinfo=TIMEZONE,
            hour=23,
            minute=59,
            second=59
        )

        loan_requests = list(LoanRequest.collection.find(
            {
                "st": "DISBURSED",
                "dd": {
                    "$gte": morning,
                    "$lte": night
                }
            }
        ))

        current_app.logger.info(
            "No of loan have due dates: {}".format(
                len(loan_requests)
            )
        )

        for loan_request in loan_requests:
            send_borrower_notif(
                loan_request["borrower_id"],
                "REMINDER_BEFORE_DUEDATE",
                loan_request["_id"]
            )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def remind_after_due_dates(self):
        """ check all loan that not been paid until certain time """
        # we check is there any loan request have due date today
        morning = datetime.now().replace(
            tzinfo=TIMEZONE,
            hour=0,
            minute=0
        )

        night = datetime.now().replace(
            tzinfo=TIMEZONE,
            hour=23,
            minute=59,
            second=59
        )

        loan_requests = list(LoanRequest.collection.find(
            {
                "st": "DISBURSED",
                "dd": {
                    "$gte": morning,
                    "$lte": night
                }
            }
        ))

        current_app.logger.info(
            "No of loan that not been paid in due dates: {}".format(
                len(loan_requests)
            )
        )

        for loan_request in loan_requests:
            send_borrower_notif(
                loan_request["borrower_id"],
                "REMINDER_AFTER_DUEDATE",
                loan_request["_id"]
            )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def auto_cancel_pending_loan(self):
        """ auto cancel loan that not been approved after 24 hour """
        # we check is there any loan request have due date today
        now = datetime.utcnow()
        local_now = TIMEZONE.localize(now)
        # update to cut off
        cut_off = local_now.replace(hour=12, minute=0)
        cut_off_utc = cut_off.astimezone(pytz.utc)

        loan_requests = list(LoanRequest.collection.find(
            {
                "st": "PENDING",
                "ca": {
                    #"$gte": last_cut_off,
                    "$lte": cut_off_utc
                }
            }
        ))

        current_app.logger.info(
            "No of cancelled requested Loan: {}".format(
                len(loan_requests)
            )
        )

        for loan_request in loan_requests:
            LoanRequest.collection.update_one(
                {"_id": loan_request["_id"]},
                {"$set": {
                    "st": "CANCELLED"
                }},
            )

            send_borrower_notif(
                loan_request["borrower_id"],
                "LOAN_REQUEST_CANCEL",
                loan_request["_id"]
            )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def auto_cancel_approved_loan(self):
        """ auto cancel loan that not been disbursed after 24 hour """
        # we check is there any loan request have due date today
        now = datetime.utcnow()
        local_now = TIMEZONE.localize(now)
        # update to cut off
        cut_off = local_now.replace(hour=12, minute=0)
        cut_off_utc = cut_off.astimezone(pytz.utc)

        loan_requests = list(LoanRequest.collection.aggregate([
            {
                "$match": {
                    "st": "APPROVED",
                    "app": {
                        "$elemMatch": {
                            "$and": [
                                {"ca": {
                                    #"$gte": last_cut_off,
                                    "$lte": cut_off_utc
                                }}
                            ]
                        }
                    }
                }
            }
        ]))

        current_app.logger.info(
            "No of approved requested Loan: {}".format(
                len(loan_requests)
            )
        )

        for loan_request in loan_requests:
            LoanRequest.collection.update_one(
                {"_id": loan_request["_id"]},
                {"$set": {
                    "st": "CANCELLED"
                }},
            )

            send_borrower_notif(
                loan_request["borrower_id"],
                "LOAN_REQUEST_CANCEL",
                loan_request["_id"]
            )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def execute_transaction_batch(self):
        """ execute schedules every hour if there any """
        schedule_ids = check_executed_schedule()

        current_app.logger.info(
            "No of Schedules: {}".format(
                len(schedule_ids)
            )
        )

        for schedule_id in schedule_ids:
            # we need to fetch schedule
            schedule_info = Schedule.find_one({"id": schedule_id})
            start_range, end_range = convert_start_end_to_datetime(
                schedule_info["start"],
                schedule_info["end"]
            )
            # convert back to utc
            transactions = list(TransactionQueue.collection.aggregate([
                {
                    "$match": {
                        "schedule_id": schedule_id,
                        "status": "WAITING",
                        "transaction_info": {
                            "$ne": None
                        },
                    }
                }
            ]))
            if transactions != []:
                # clean up transactions and format the list
                current_app.logger.info(
                    "No of Transaction that going to be processed: {}".format(
                        len(transactions)
                    )
                )
                formatted_transactions = [
                    {
                        "wallet_id": str(trx["wallet_id"]),
                        "source_id": str(trx["source_id"]),
                        "source_type": trx["source_type"],
                        "destination_id": str(trx["destination_id"]),
                        "destination_type": trx["destination_type"],
                        "amount": trx["amount"].to_decimal(),
                        "transaction_type": trx["transaction_type"],
                    }
                    for trx in transactions
                ]

                update_records = [
                    {
                        "model": trx["transaction_info"]["model"],
                        "model_id": trx["transaction_info"]["model_id"],
                        "status": trx["transaction_info"]["status"],
                    }
                    for trx in transactions
                ]

                task_payload = {
                    "transactions": formatted_transactions,
                    "update_records": update_records
                }
                current_app.logger.info(
                    "Transaction that going to be processed: {}".format(
                        task_payload
                    )
                )

                TransactionTask().send_bulk_transaction.apply_async(
                    kwargs=task_payload,
                    queue="transaction",
                    link=TransactionTask().map_bulk_transaction.s().set(queue="transaction")
                )

                for transaction in transactions:
                    transactions = TransactionQueue.collection.update_one(
                        {"_id": transaction["_id"]},
                        {
                            "$set": {
                                "status": "SENT"
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
    def generate_afpi_report(self):
        """ generate afpi report every 18.00 WIB """
        try:
            # populate all loans here
            services = DateTimeReportServices(is_today=True)
            loans, regulation_report_id = services.create_or_update_loans()
        except ReportServicesError:
            self.retry()
        else:
            current_app.logger.info(
                "No of loans reported: {}".format(len(loans))
            )
            zip_name = services.generate_afpi_report()
            current_app.logger.info(
                "Generating AFPI Report: {} with file {}".format(
                    str(regulation_report_id), zip_name
                )
            )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def send_afpi_report(self):
        """ read a file and send afpi report every 00.00 WIB through SFTP """
        # we use is_today apparently because 00.00 WIB is equal to 17.00 UTC so
        # it's not different day
        services = DateTimeReportServices(is_today=True)
        zip_name = services.generate_afpi_report()

        current_app.logger.info(
            "begin upload AFPI Report: {} ".format(
                zip_name
            )
        )
        # upload it through sftp
        with open(zip_name, "rb") as zf:
            # open the actual file and convert into file like object
            try:
                services.upload_file_via_ftp(io.BytesIO(zf.read()), zip_name)
            except ReportServicesError:
                self.retry()

        current_app.logger.info(
            "upload AFPI Report: {} completed".format(
                zip_name
            )
        )

    @celery.task(
        bind=True,
        max_retries=int(WORKER["MAX_RETRIES"]),
        task_soft_time_limit=WORKER["SOFT_LIMIT"],
        task_time_limit=WORKER["SOFT_LIMIT"],
        acks_late=WORKER["ACKS_LATE"],
    )
    def generate_ojk_report(self):
        """ trigger ojk report on anaylst backend"""
        # fetch token from backend
        base_url = ANALYST_BE["BASE_URL"]
        endpoint = ANALYST_BE["ENDPOINTS"]["LOGIN"]
        url = base_url + endpoint

        payload = {
            "username": ANALYST_BE["USERNAME"],
            "password": ANALYST_BE["PASSWORD"],
            "accountType": "ANALYST"
        }

        try:
            r = requests.post(url, payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            try:
                self.retry(countdown=backoff(self.request.retries))
            except MaxRetriesExceededError:
                current_app.logger.info(exc)

        access_token = r.json()["payload"]["token"]

        # geenrate report
        local_now = TIMEZONE.localize(datetime.utcnow())
        report_types = ["CA", "LENDER"]

        endpoint = ANALYST_BE["ENDPOINTS"]["CREATE_REPORT"]

        for report in report_types:
            url = base_url + endpoint.format(local_now.date(), report)

            try:
                print(url)
                r = requests.get(url, headers={"authorization": access_token})
                print(r.json())
                r.raise_for_status()
            except requests.exceptions.HTTPError as exc:
                try:
                    self.retry(countdown=backoff(self.request.retries))
                except MaxRetriesExceededError:
                    current_app.logger.info(exc)
