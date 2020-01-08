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

import pytz
from datetime import datetime, timedelta

from bson import ObjectId
from flask import current_app
from app.api.serializer import LoanBorrowerReportSchema
# models
from app.api.models.report import RegulationReport, AfpiReport
from app.api.models.borrower import Borrower
from app.api.models.loan_request import LoanRequest, LoanRequestNotFound
# config
from app.api.const import P2P_ID
from app.config.external.afpi import SERVER
from app.config.external.storage import FILE_URL
# core
from app.api.lib.core.exceptions import BaseError


TIMEZONE = pytz.timezone("Asia/Jakarta")


class ReportServicesError(BaseError):
    """ raised when reporrt services error """


def fetch_all_loans(regulation_report_id, start_time, end_time):
    # first we need to join loan and borrower and query everything
    loans_borrowers = list(LoanRequest.collection.aggregate([
        {
            "$match": {
                "$or": [
                    {
                        "st": "DISBURSED"
                    },
                    {
                        "st": "PAID",
                        "pda": {
                            "$gte": start_time,
                            "$lte": end_time
                        }
                    },
                    {
                        "st": "WRITEOFF",
                        "wda": {
                            "$gte": start_time,
                            "$lte": end_time
                        }
                    }
                ]
            }
        },
        {
            "$lookup": {
                "from": "lender_borrowers",
                "localField": "borrower_id",
                "foreignField": "_id",
                "as": "borrower",
            },
        },
        {
            "$unwind": "$borrower",
        },
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
        }
    ]))

    converted_data = []
    for loan_borrower in loans_borrowers:
        serialized = LoanBorrowerReportSchema().dump(loan_borrower)
        # access serialized data
        report = serialized.data
        # append report id
        report["regulation_report_id"] = regulation_report_id
        converted_data.append(report)
    return converted_data


def create_afpi_report_entry():
    """ query all required loan & borrower convert it into accepted values to afpi report collection """
    # we need to make every 24 hour we only have 1 report and update if we
    # found
    now = datetime.utcnow()
    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=23, minute=59)

    regulation_report = RegulationReport.find_one({
        "ca": {
            "$gte": start_time,
            "$lte": end_time
        }
    })

    if regulation_report is None:
        regulation_report = RegulationReport(
            report_type="AFPI",
            list_of_status=[{
                "status": "PROCESSING"
            }]
        )
        regulation_report.commit()
    # fetch all loans
    loans = fetch_all_loans(regulation_report.id, start_time, end_time)
    if loans == []:
        raise ReportServicesError
    # first we need to check whether this regulation report id has been
    # inserted or not if already inserted we just update the information so no
    # duplicate entry created
    afpi_reports = list(AfpiReport.find({"regulation_report_id":
                                         regulation_report.id}))
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
                loan
            )
            operations.append(query)
        AfpiReport.collection.bulk_write(operations)
    return regulation_report

def generate_afpi_filename(version):
    # pattern is
    # p2p_id + date + SIK + version
    now = datetime.utcnow()
    local_now = TIMEZONE.localize(now)
    local_date_string = local_now.strftime("%Y%m%d")
    return P2P_ID + local_date_string + "SIK" + version


def generate_afpi_report(regulation_report_id=None, version="01"):
    reports = list(AfpiReport.collection.find({
        "regulation_report_id": ObjectId(regulation_report_id)
    }))

    # initialize temporary output using stringio
    csv_buffer = io.StringIO()
    # init header name
    field_names = ["p2p_id", "borrower_id", "borrower_type", "borrower_name",
                   "identity_no", "npwp_no", "loan_id", "agreement_date",
                   "disburse_date", "loan_amount", "reported_date",
                   "remaining_loan_amount", "due_date", "quality",
                   "current_dpd", "max_dpd", "status"]
    # init csv writer using dictwriter instead of normal writer
    writer = csv.DictWriter(csv_buffer, field_names, delimiter="|",
                            extrasaction="ignore")
    for report in reports:
        writer.writerow(report)

    # generate filename according to AFPI format
    filename = generate_afpi_filename(version)
    zip_name = "{}.zip".format(filename)
    csv_name = "{}.csv".format(filename)
    # create csv file first
    with open(csv_name, mode="w") as cf:
        csv_buffer.seek(0)
        shutil.copyfileobj(csv_buffer, cf)

    password = "-p" + SERVER["ZIP_PASSWORD"]

    command = ["7z", "a", password, "-y", zip_name] + [csv_name]
    subprocess.call(command)
    # dont forget to add CREATED
    # also add link to access the file
    regulation_report = RegulationReport.find_one({
        "id": ObjectId(regulation_report_id)
    })
    regulation_report.file_url = FILE_URL.format(str(regulation_report_id))
    regulation_report.list_of_status.append({
        "status": "CREATED"
    })
    regulation_report.commit()

    return zip_name


def upload_file_via_ftp(file_, filename):
    """ send file to AFPI server through SFTP protocol """
    # disable ssh key checking
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    try:
        with pysftp.Connection(
                SERVER["HOST"],
                username=SERVER["USERNAME"],
                password=SERVER["PASSWORD"],
                cnopts=cnopts
        ) as sftp:
            sftp.putfo(file_, "/in/{}".format(filename))
    except:
        raise ReportServicesError
