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


def test_fetch_all_loans(make_loan_request, setup_regulation_report):
    make_loan_request(
        status="DISBURSED",
        payment_state_status="LANCAR",
        list_of_status=[
            {"status": "SEND_TO_MODANAKU_COMPLETED"}
        ]
    )
    results = fetch_all_loans(setup_regulation_report.id)
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
