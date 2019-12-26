import pytz
from datetime import date, datetime, timedelta
from freezegun import freeze_time
from task.scheduler.tasks import (
    check_grace_period,
    determine_loan_quality,
    SchedulerTask
)

from app.api.models.batch import Schedule, TransactionQueue
from app.api.models.investment import Investment
from app.api.models.loan_request import LoanRequest


TIMEZONE = pytz.timezone("Asia/Jakarta")


def test_determine_loan_quality():
    # 0 < 30 lancar
    loan_status, payment_status = determine_loan_quality(1)
    assert loan_status == "DISBURSED"
    assert payment_status == "LANCAR"

    # 0 < 30 lancar
    loan_status, payment_status = determine_loan_quality(29)
    assert loan_status == "DISBURSED"
    assert payment_status == "LANCAR"

    # 31 < 90 tidak lancar
    loan_status, payment_status = determine_loan_quality(31)
    assert loan_status == "DISBURSED"
    assert payment_status == "TIDAK_LANCAR"

    # 31 < 90 tidak lancar
    loan_status, payment_status = determine_loan_quality(89)
    assert loan_status == "DISBURSED"
    assert payment_status == "TIDAK_LANCAR"

    # 31 < 90 tidak lancar
    loan_status, payment_status = determine_loan_quality(90)
    assert loan_status == "DISBURSED"
    assert payment_status == "TIDAK_LANCAR"

    # 90 > macet
    loan_status, payment_status = determine_loan_quality(91)
    assert loan_status == "WRITEOFF"
    assert payment_status == "MACET"

@freeze_time("2019-11-25")
def test_check_grace_period_on_time():
    current_date = datetime.now()
    due_date = datetime.now()
    grace_period = 2

    result = check_grace_period(due_date, grace_period, current_date)
    assert result


@freeze_time("2019-11-25")
def test_check_grace_period_past_2_day():
    # imagine today its 27
    current_date = datetime.now() + timedelta(days=2)
    due_date = datetime.now()
    grace_period = 2

    result = check_grace_period(due_date, grace_period, current_date)
    assert result


@freeze_time("2019-11-25")
def test_check_grace_period_expire():
    # imagine today its 27
    current_date = datetime.now() + timedelta(days=3)
    due_date = datetime.now()
    grace_period = 2

    result = check_grace_period(due_date, grace_period, current_date)
    assert result is False


@freeze_time("2019-11-25")
def test_calculate_overdues_on_time(make_loan_request):
    loan_request = make_loan_request(status="DISBURSED")

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.payment_state_status == "LANCAR"
    assert loan_request.overdue == 0


@freeze_time("2019-11-26")
def test_calculate_overdues_grace1():
    """ due date is 25 and today is 26 so it should be grace period """
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.payment_state_status == "LANCAR"
    assert loan_request.overdue == 1


@freeze_time("2019-11-27")
def test_calculate_overdues_grace2(make_loan_request):
    # setup some record that have duedate of 25
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.payment_state_status == "LANCAR"
    assert loan_request.overdue == 2


@freeze_time("2019-11-28")
def test_calculate_overdues_3_day(make_loan_request):
    # setup some record that have duedate of 25
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.payment_state_status == "LANCAR"
    assert loan_request.overdue == 3


@freeze_time("2019-12-29")
def test_calculate_overdues_31_day(make_loan_request):
    # setup some record that have duedate of 25
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]
    loan_request.overdue = 30
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.payment_state_status == "TIDAK_LANCAR"
    assert loan_request.overdue == 31


def test_calculate_overdues_write_off(make_loan_request):
    # setup some record that overdue over 89
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]
    loan_request = LoanRequest.find_one(
        {"id": loan_request.id}
    )
    loan_request.overdue = 90
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one(
        {"id": loan_request.id}
    )
    assert loan_request.payment_state_status == "MACET"
    assert loan_request.status == "WRITEOFF"
    assert loan_request.overdue == 91


def test_calculate_late_fees_case1(setup_investment, setup_investor, make_loan_request):
    # create some loan that already disbursed
    loan_request = make_loan_request(status="DISBURSED")
    loan_request.overdue = 3
    loan_request.investment_id = setup_investment.id
    loan_request.investor_id = setup_investor.id
    loan_request.commit()

    investment_loan_request = {
        "loan_request_id": loan_request.id,
        "disburse_amount": 46000,
        "total_fee": 40000,
        "fees": [
            {
                "name": "upfrontFee",
                "investor_fee": 4000,
                "profit_fee": 36000
            }
        ]
    }
    setup_investment.loan_requests.append(investment_loan_request)
    setup_investment.commit()

    loan_request_ids = []
    loan_request_ids.append(str(loan_request.id))

    SchedulerTask().calculate_late_fees(loan_request_ids)

    loan_request = Investment.extract_investment_loan(loan_request.id)
    assert loan_request["fees"][0]["if"].to_decimal() == 4000
    assert loan_request["fees"][0]["af"].to_decimal() == 36000
    assert loan_request["fees"][1]["if"].to_decimal() == 4500
    assert loan_request["fees"][1]["af"].to_decimal() == 10500
    assert loan_request["fees"][1]["lf"].to_decimal() == 15000


def test_calculate_late_fees_case2(setup_investment, setup_investor, make_loan_request):
    # create some loan that already disbursed
    loan_request = make_loan_request(
        status="DISBURSED",
        requested_loan_request=1000000
    )
    loan_request.overdue = 10
    loan_request.investment_id = setup_investment.id
    loan_request.investor_id = setup_investor.id
    loan_request.commit()

    investment_loan_request = {
        "loan_request_id": loan_request.id,
        "disburse_amount": 920000,
        "total_fee": 80000,
        "fees": [
            {
                "name": "upfrontFee",
                "investor_fee": 24000,
                "profit_fee": 56000
            }
        ]
    }
    setup_investment.loan_requests.append(investment_loan_request)
    setup_investment.commit()

    loan_request_ids = []
    loan_request_ids.append(str(loan_request.id))

    SchedulerTask().calculate_late_fees(loan_request_ids)

    loan_request = Investment.extract_investment_loan(loan_request.id)
    assert loan_request["fees"][0]["if"].to_decimal() == 24000
    assert loan_request["fees"][0]["af"].to_decimal() == 56000
    assert loan_request["fees"][1]["lf"].to_decimal() == 100000
    assert loan_request["fees"][1]["if"].to_decimal() == 30000
    assert loan_request["fees"][1]["af"].to_decimal() == 70000


def test_calculate_late_fees_case3(setup_investment, setup_investor, make_loan_request):
    """ test calculate late fee after 20 day, should be reach amx late fee"""
    # create some loan that already disbursed
    loan_request = make_loan_request(
        status="DISBURSED",
        requested_loan_request=1000000
    )
    loan_request.overdue = 20
    loan_request.investment_id = setup_investment.id
    loan_request.investor_id = setup_investor.id
    loan_request.commit()

    investment_loan_request = {
        "loan_request_id": loan_request.id,
        "disburse_amount": 920000,
        "total_fee": 80000,
        "fees": [
            {
                "name": "upfrontFee",
                "investor_fee": 24000,
                "profit_fee": 56000
            }
        ]
    }
    setup_investment.loan_requests.append(investment_loan_request)
    setup_investment.commit()

    loan_request_ids = []
    loan_request_ids.append(str(loan_request.id))

    SchedulerTask().calculate_late_fees(loan_request_ids)

    loan_request = Investment.extract_investment_loan(loan_request.id)
    assert loan_request["fees"][0]["if"].to_decimal() == 24000
    assert loan_request["fees"][0]["af"].to_decimal() == 56000
    assert loan_request["fees"][1]["lf"].to_decimal() == 200000
    assert loan_request["fees"][1]["if"].to_decimal() == 60000
    assert loan_request["fees"][1]["af"].to_decimal() == 140000


@freeze_time("2019-12-02")
def test_auto_cancel_verifying_loan(make_loan_request):
    """ simulate loan that has been created in the morning but not approved so
    it should be cancelled on the same day """
    local_time = TIMEZONE.localize(
        datetime(year=2019, month=12, day=2, hour=9, minute=10)
    )
    utc_time = local_time.astimezone(pytz.UTC)
    loan_request = make_loan_request(status="VERIFYING")
    loan_request.ca = utc_time
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().auto_cancel_verifying_loan()
    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.status == "CANCELLED"


@freeze_time("2019-12-02")
def test_auto_cancel_verifying_loan2(make_loan_request):
    """ simulate loan that has been created in the afternoon but not approved
    so it should be not cancelled today but next day"""
    local_time = TIMEZONE.localize(
        datetime(year=2019, month=12, day=2, hour=13, minute=10)
    )
    utc_time = local_time.astimezone(pytz.UTC)
    loan_request = make_loan_request(status="VERIFYING")
    loan_request.ca = utc_time
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().auto_cancel_verifying_loan()
    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.status == "VERIFYING"


@freeze_time("2019-12-03")
def test_auto_cancel_verifying_loan3(make_loan_request):
    """ simulate loan that has been created in the afternoon yesterday but not
    approved so it should be cancelled h+1"""
    local_time = TIMEZONE.localize(
        datetime(year=2019, month=12, day=2, hour=13, minute=10)
    )
    utc_time = local_time.astimezone(pytz.UTC)
    loan_request = make_loan_request(status="VERIFYING")
    loan_request.ca = utc_time
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().auto_cancel_verifying_loan()
    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.status == "CANCELLED"


@freeze_time("2019-12-02")
def test_auto_cancel_verifying_loan4(make_loan_request):
    """ simulate loan that has been created in the morning and afternoon the
    one should be updated is the one in the morning"""
    local_time = TIMEZONE.localize(
        datetime(year=2019, month=12, day=2, hour=7, minute=10)
    )
    utc_time = local_time.astimezone(pytz.UTC)
    morning_loan = make_loan_request(status="VERIFYING")
    morning_loan.ca = utc_time
    morning_loan.commit()

    local_time = TIMEZONE.localize(
        datetime(year=2019, month=12, day=2, hour=14, minute=10)
    )
    utc_time = local_time.astimezone(pytz.UTC)
    afternoon_loan = make_loan_request(status="VERIFYING")
    afternoon_loan.ca = utc_time
    afternoon_loan.commit()

    SchedulerTask().auto_cancel_verifying_loan()
    morning_loan = LoanRequest.find_one({"id": morning_loan.id})
    assert morning_loan.status == "CANCELLED"

    SchedulerTask().auto_cancel_verifying_loan()
    afternoon_loan = LoanRequest.find_one({"id": afternoon_loan.id})
    assert afternoon_loan.status == "VERIFYING"


@freeze_time("2019-12-02")
def test_auto_cancel_approved_loan(make_loan_request):
    """ simulate loan that has been approved in the morning but not disbursed so
    it should be cancelled on the same day """
    local_time = TIMEZONE.localize(
        datetime(year=2019, month=12, day=2, hour=9, minute=10)
    )
    utc_time = local_time.astimezone(pytz.UTC)
    loan_request = make_loan_request(status="APPROVED")
    approvals = [{
        "status": "APPROVED",
        "ca": utc_time
    }]
    loan_request.approvals = approvals
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().auto_cancel_approved_loan()
    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.status == "CANCELLED"


@freeze_time("2019-12-02")
def test_auto_cancel_approved_loan2(make_loan_request):
    """ simulate loan that has been approved in the afternoon but not disbursed so
    it should be cancelled on the next day """
    local_time = TIMEZONE.localize(
        datetime(year=2019, month=12, day=2, hour=13, minute=10)
    )
    utc_time = local_time.astimezone(pytz.UTC)
    loan_request = make_loan_request(status="APPROVED")
    approvals = [{
        "status": "APPROVED",
        "ca": utc_time
    }]
    loan_request.approvals = approvals
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().auto_cancel_approved_loan()
    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.status == "APPROVED"


@freeze_time("2019-12-02")
def test_reminder_due_date(make_loan_request):
    """ simulate auto reminder before due date in the morning """
    loan_request = make_loan_request(status="DISBURSED")
    loan_request.due_date = date(year=2019, month=12, day=2)
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().remind_before_due_dates()


@freeze_time("2019-12-02")
def test_reminder_after_due_date(make_loan_request):
    """ simulate auto reminder after due date in the evening """
    loan_request = make_loan_request(status="DISBURSED")
    loan_request.due_date = date(year=2019, month=12, day=2)
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().remind_after_due_dates()

'''
@freeze_time("06:00:59")  # in utc is 13.00
def test_execute_transaction_batch(make_transaction_queue):
    """ simulate executing schedules """
    # create a transaction queue that already queued 2 hours ago
    queue_at = datetime.utcnow() - timedelta(hours=2)
    queue = make_transaction_queue("UPFRONT_AFTERNOON", queue_at)

    # setup some record that have duedate of 25
    SchedulerTask().execute_transaction_batch()
'''
@freeze_time("12:00:59")  # in utc is 13.00
def test_execute_transaction_batch2(make_transaction_queue):
    """ simulate executing schedules """
    # create a transaction queue that already queued 2 hours ago
    queue_at = datetime.utcnow() - timedelta(hours=2)
    queue = make_transaction_queue("UPFRONT_NIGHT", queue_at)

    # setup some record that have duedate of 25
    SchedulerTask().execute_transaction_batch()


def test_generate_ojk_report():
    """ test generating ojk report"""
    SchedulerTask().generate_ojk_report()
