from datetime import datetime

import random
import pytest
from freezegun import freeze_time

from app.api.report.modules.services import (
    fetch_all_loans,
    create_afpi_report_entry,
    generate_afpi_report,
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
    results = fetch_all_loans(setup_regulation_report.id, start_time, end_time)
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
        payment_date=now
    )
    results = fetch_all_loans(setup_regulation_report.id, start_time, end_time)
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
    results = fetch_all_loans(setup_regulation_report.id, start_time, end_time)
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

    results = fetch_all_loans(setup_regulation_report.id, start_time, end_time)
    assert results

def test_create_afpi_report_entry(setup_afpi_report):
    create_afpi_report_entry()
    reports = list(AfpiReport.find())
    assert len(reports)


def test_create_afpi_report_entry_already_exist(setup_afpi_report):
    create_afpi_report_entry()
    reports = list(AfpiReport.find())
    assert len(reports)


def test_create_afpi_report_entry_empty():
    LoanRequest.collection.delete_many({})
    with pytest.raises(ReportServicesError):
        create_afpi_report_entry()


@freeze_time("2019-12-19")
def test_generate_afpi_report(setup_afpi_report, setup_regulation_report):
    random_ver = random.randint(1, 99)
    csv_output = generate_afpi_report(setup_regulation_report.id,
                                      str(random_ver))
    assert csv_output
