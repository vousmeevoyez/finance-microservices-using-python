""" Test Report Modules """
from datetime import datetime
import pytest
from unittest.mock import patch

from freezegun import freeze_time

from app.api.report.modules.services import (
    DateTimeReportServices,
    ReportServicesError
)
from app.api.models.report import AfpiReport
from app.api.models.loan_request import LoanRequest


@freeze_time("2020-1-1")
def test_fetch_all_loans_outstanding_only(
        make_loan_request, setup_regulation_report
):
    """ simulate fetching all loan that is outstanding only """
    now = datetime.utcnow()
    start_time = now.replace(hour=0, minute=0)
    end_time = now.replace(hour=23, minute=59)

    make_loan_request(
        status="DISBURSED",
        payment_state_status="LANCAR",
        list_of_status=[
            {"status": "SEND_TO_MODANAKU_COMPLETED"}
        ]
    )
    results = DateTimeReportServices.fetch_all_loans(
        setup_regulation_report.id, start_time, end_time
    )
    assert results


@freeze_time("2020-1-1")
def test_fetch_all_loans_paid_only(make_loan_request, setup_regulation_report):
    """ simulate fetching all loan that is already paid """
    now = datetime.utcnow()
    start_time = now.replace(hour=0, minute=0)
    end_time = now.replace(hour=23, minute=59)

    make_loan_request(
        status="PAID",
        payment_state_status="LANCAR",
        list_of_status=[
            {"status": "SEND_TO_MODANAKU_COMPLETED"}
        ],
        payment_date=now.date()
    )
    results = DateTimeReportServices.fetch_all_loans(setup_regulation_report.id, start_time, end_time)
    assert results


@freeze_time("2020-1-1")
def test_fetch_all_loans_writeoff_only(make_loan_request, setup_regulation_report):
    """ simulate fetching all loan that is already writeoff """
    now = datetime.utcnow()
    start_time = now.replace(hour=0, minute=0)
    end_time = now.replace(hour=23, minute=59)

    make_loan_request(
        status="WRITEOFF",
        payment_state_status="MACET",
        list_of_status=[
            {"status": "SEND_TO_MODANAKU_COMPLETED"}
        ],
        ua=now
    )
    results = DateTimeReportServices.fetch_all_loans(setup_regulation_report.id, start_time, end_time)
    assert results


@freeze_time("2020-1-2")
def test_fetch_all_loans(make_loan_request, setup_regulation_report):
    """ simulate fetching all loan that is have disburse, paid and writeoff """
    now = datetime.utcnow()
    start_time = now.replace(hour=0, minute=0)
    end_time = now.replace(hour=23, minute=59)

    make_loan_request(
        status="WRITEOFF",
        payment_state_status="MACET",
        list_of_status=[
            {"status": "SEND_TO_MODANAKU_COMPLETED"}
        ],
        ua=now
    )

    results = DateTimeReportServices.fetch_all_loans(setup_regulation_report.id, start_time, end_time)
    assert results


def test_create_or_increment_regulation_report():
    """ test create new regulation report """
    regulation_report = DateTimeReportServices(
        is_today=False
    ).create_or_increment_regulation_report()
    assert regulation_report.version == 1


def test_create_or_increment_regulation_report_existing():
    """ test increment existing regulation report """
    regulation_report = DateTimeReportServices(
        is_today=True
    ).create_or_increment_regulation_report()
    assert regulation_report.version == 2


def test_create_or_update_loans(make_loan_request):
    """ test create or update loans """
    now = datetime.utcnow()

    make_loan_request(
        status="WRITEOFF",
        payment_state_status="MACET",
        list_of_status=[
            {"status": "SEND_TO_MODANAKU_COMPLETED"}
        ],
        ua=now
    )

    loans, regulation_report_id = DateTimeReportServices(
        is_today=True
    ).create_or_update_loans()
    assert len(loans) >= 1


def test_create_or_update_no_loans():
    """ test create or update but no matching loans """
    # wipe loans
    LoanRequest.collection.delete_many({})

    with pytest.raises(ReportServicesError):
        DateTimeReportServices(
            is_today=False
        ).create_or_update_loans()

def test_generate_afpi_report():
    """ test generate actual file for afpi report """
    zip_name = DateTimeReportServices(
        is_today=True
    ).generate_afpi_report()
    assert zip_name
    pytest.zip_name = zip_name


@patch("pysftp.Connection")
def test_upload_file_via_ftp(mock_sftp):
    """ test generate actual file for afpi report """
    filename = pytest.zip_name

    with open(filename, "rb") as file_:
        DateTimeReportServices(
            is_today=True
        ).upload_file_via_ftp(file_, filename)
