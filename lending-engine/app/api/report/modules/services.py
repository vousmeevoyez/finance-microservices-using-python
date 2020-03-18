"""
    Loan Request Services
    _________________
    This is module to process business logic from routes and return API
    response
"""
import shutil
import subprocess
import io
import csv
import pysftp
from pymongo import ReplaceOne

from datetime import datetime, timedelta

from bson import ObjectId
from app.api.serializer import generate_afpi_filename, LoanBorrowerReportSchema

# models
from app.api.models.report import RegulationReport, AfpiReport
from app.api.models.borrower import Borrower
from app.api.models.loan_request import LoanRequest, LoanRequestNotFound

# config
from app.config.external.afpi import SERVER
from app.config.external.storage import FILE_URL

# core
from app.api.lib.core.exceptions import BaseError


class ReportServicesError(BaseError):
    """ raised when reporrt services error """


class DateTimeReportServices:

    def __init__(self, is_today):
        # first fetch start end time range
        start_time, end_time = self.generate_time_range(is_today)
        self.start_time = start_time
        self.end_time = end_time
        # second look up regulation report using time range
        regulation_report = self.fetch_report_based_on_time(
            start_time,
            end_time
        )
        self.regulation_report = regulation_report
        # third generate file name for designated report
        if regulation_report is not None:
            zip_name, csv_name = self.generate_zip_csv_name(regulation_report)
            self.zip_name = zip_name
            self.csv_name = csv_name

    def generate_time_range(self, is_today):
        today = datetime.utcnow()
        if not is_today:
            today = today - timedelta(days=1)
        start_time = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = today.replace(hour=23, minute=59)
        return start_time, end_time

    def fetch_report_based_on_time(self, start_time, end_time):
        regulation_report = RegulationReport.find_one(
            {"ca": {"$gte": start_time, "$lte": end_time}}
        )
        return regulation_report

    def generate_zip_csv_name(self, regulation_report):
        # generate filename according to AFPI format
        filename = generate_afpi_filename(
            regulation_report.ca,
            regulation_report.version
        )
        zip_name = "{}.zip".format(filename)
        csv_name = "{}.csv".format(filename)
        return zip_name, csv_name

    @staticmethod
    def fetch_all_loans(regulation_report_id, start_time, end_time):
        # we populate LOAN + Borrower data using time range as parameter and
        # return all required file for AFPI
        loans_borrowers = list(
            LoanRequest.collection.aggregate(
                [
                    {
                        "$match": {
                            "$or": [
                                {"st": "DISBURSED"},
                                {
                                    "st": "PAID",
                                    "pda": {
                                        "$gte": start_time,
                                        "$lte": end_time
                                    },
                                },
                                {
                                    "st": "WRITEOFF",
                                    "wda": {
                                        "$gte": start_time,
                                        "$lte": end_time
                                    },
                                },
                            ]
                        }
                    },
                    {
                        "$lookup": {
                            "from": "lender_borrowers",
                            "localField": "borrower_id",
                            "foreignField": "_id",
                            "as": "borrower",
                        }
                    },
                    {"$unwind": "$borrower"},
                    {
                        "$project": {
                            "_id": 0,
                            "lrc": 1,
                            "tnc.aa": 1,
                            "borrower.bc": 1,
                            "borrower.fn": 1,
                            "borrower.mn": 1,
                            "borrower.ln": 1,
                            "borrower.ktp.kn": 1,
                            "borrower.npwp.nn": 1,
                            "pda": 1,
                            "lar": 1,
                            "dd": 1,
                            "psts": 1,
                            "ov": 1,
                            "st": 1,
                            "lst": 1,
                        }
                    },
                ]
            )
        )

        converted_data = []
        for loan_borrower in loans_borrowers:
            serialized = LoanBorrowerReportSchema().dump(loan_borrower)
            # access serialized data
            report = serialized.data
            # append report id
            report["regulation_report_id"] = regulation_report_id
            converted_data.append(report)
        return converted_data

    def create_or_increment_regulation_report(self):
        """ we check whether the regulation report for particular time already
        exist or not, if already exist we simply increment the version we newer
        record
        """
        # we need to make every 24 hour we only have 1 report and update if we
        # found

        regulation_report = self.regulation_report
        if regulation_report is None:
            regulation_report = RegulationReport(
                report_type="AFPI",
                list_of_status=[{"status": "PROCESSING"}]
            )
            regulation_report.commit()
        else:
            # increment the version
            regulation_report.version += 1
            regulation_report.commit()
        return regulation_report

    def create_or_update_loans(self):
        """ query all required loan & borrower convert it
            into accepted values to afpi report collection
            if record is not exist we insert if already existed we replace the
            whole previous record with the new one
        """
        regulation_report = self.create_or_increment_regulation_report()
        # assign regulation report to class
        self.regulation_report = regulation_report

        # fetch all loans
        loans = self.fetch_all_loans(
            regulation_report.id,
            self.start_time,
            self.end_time
        )
        if loans == []:
            # if no matched loan we need to remove regulation report so it
            # became consistent
            regulation_report.delete()
            raise ReportServicesError
        # first we need to check whether this regulation report id has been
        # inserted or not if already inserted we just update the information so no
        # duplicate entry created
        afpi_reports = list(
            AfpiReport.find({
                "regulation_report_id": regulation_report.id
            })
        )
        if afpi_reports == []:
            AfpiReport.collection.insert_many(loans)
        else:
            # replace all the previous records
            operations = []
            for loan in loans:
                # replace query
                query = ReplaceOne(
                    {
                        "regulation_report_id": regulation_report.id,
                        "loan_id": loan["loan_id"]
                    },
                    loan,
                    upsert=True
                )
                operations.append(query)
            AfpiReport.collection.bulk_write(operations)
        return loans, str(regulation_report.id)

    def write_to_csv(self, loan_borrowers):
        """ write loan borrowers data into
        correct csv return the csv buffer """
        # initialize temporary output using stringio
        csv_buffer = io.StringIO()
        # init header name
        field_names = [
            "p2p_id",
            "borrower_id",
            "borrower_type",
            "borrower_name",
            "identity_no",
            "npwp_no",
            "loan_id",
            "agreement_date",
            "disburse_date",
            "loan_amount",
            "reported_date",
            "remaining_loan_amount",
            "due_date",
            "quality",
            "current_dpd",
            "max_dpd",
            "status",
        ]
        # init csv writer using dictwriter instead of normal writer
        writer = csv.DictWriter(
            csv_buffer, field_names, delimiter="|", extrasaction="ignore"
        )
        csv_buffer = io.StringIO()
        # init header name
        field_names = [
            "p2p_id",
            "borrower_id",
            "borrower_type",
            "borrower_name",
            "identity_no",
            "npwp_no",
            "loan_id",
            "agreement_date",
            "disburse_date",
            "loan_amount",
            "reported_date",
            "remaining_loan_amount",
            "due_date",
            "quality",
            "current_dpd",
            "max_dpd",
            "status",
        ]
        # init csv writer using dictwriter instead of normal writer
        writer = csv.DictWriter(
            csv_buffer, field_names, delimiter="|", extrasaction="ignore"
        )

        for loan_borrower in loan_borrowers:
            writer.writerow(loan_borrower)
        return csv_buffer

    def generate_afpi_report(self):
        """ convert from record to actual zip + csv file """
        loan_borrowers = list(
            AfpiReport.collection.find({
                "regulation_report_id": self.regulation_report.id
            })
        )

        csv_buffer = self.write_to_csv(loan_borrowers)

        # write buffer into actual file
        with open(self.csv_name, mode="w") as cf:
            csv_buffer.seek(0)
            shutil.copyfileobj(csv_buffer, cf)

        password = "-p" + SERVER["ZIP_PASSWORD"]
        command = ["7z", "a", password, "-y", self.zip_name] + [self.csv_name]
        subprocess.call(command)

        # also add link to access the file
        regulation_report_id = str(self.regulation_report.id)
        self.regulation_report.file_url = \
            FILE_URL.format(regulation_report_id)
        self.regulation_report.commit()
        return self.zip_name

    def upload_file_via_ftp(self, file_, filename):
        """ send file to AFPI server through SFTP protocol """
        # disable ssh key checking
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        try:
            with pysftp.Connection(
                    SERVER["HOST"],
                    username=SERVER["USERNAME"],
                    password=SERVER["PASSWORD"],
                    cnopts=cnopts,
            ) as sftp:
                sftp.putfo(file_, "/in/{}".format(filename))
        except:
            raise ReportServicesError
        else:
            if any(
                    "SENT" in rr.status for rr in
                    self.regulation_report.list_of_status
            ):
                self.regulation_report.collection.update_one(
                    {
                        "_id": self.regulation_report.id
                    },
                    {
                        "$pull": {"st": "SENT"}
                    }
                )
            self.regulation_report.list_of_status.append({"status": "SENT"})
            self.regulation_report.commit()


class IdReportServices(DateTimeReportServices):

    def __init__(self, regulation_report_id):
        # first fetch start end time range
        start_time, end_time = self.generate_time_range(is_today=True)
        self.start_time = start_time
        self.end_time = end_time

        # second look up regulation report using time range
        regulation_report = RegulationReport.find_one({
            "id": ObjectId(regulation_report_id)
        })
        self.regulation_report = regulation_report

        # third generate file name for designated report
        if regulation_report is not None:
            zip_name, csv_name = self.generate_zip_csv_name(regulation_report)
            self.zip_name = zip_name
            self.csv_name = csv_name
