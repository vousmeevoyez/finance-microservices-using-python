from datetime import date, datetime, timedelta
from freezegun import freeze_time
from task.scheduler.tasks import check_grace_period, SchedulerTask

from app.api.models.investment import Investment
from app.api.models.loan_request import LoanRequest


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
def test_calculate_overdues_past(make_loan_request):
    # setup some record that have duedate of 25
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.payment_state_status == "TIDAK_LANCAR"
    assert loan_request.overdue == 3


@freeze_time("2019-11-28")
def test_calculate_overdues_past(make_loan_request):
    # setup some record that have duedate of 25
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one({"id": loan_request.id})
    assert loan_request.payment_state_status == "TIDAK_LANCAR"
    assert loan_request.overdue == 3


def test_calculate_overdues_write_off(make_loan_request):
    # setup some record that overdue over 89
    loan_request = list(LoanRequest.find({"status": "DISBURSED"}))[0]
    loan_request = LoanRequest.find_one(
        {"id": loan_request.id}
    )
    loan_request.overdue = 89
    loan_request.commit()

    # setup some record that have duedate of 25
    SchedulerTask().calculate_overdues()

    loan_request = LoanRequest.find_one(
        {"id": loan_request.id}
    )
    assert loan_request.payment_state_status == "MACET"
    assert loan_request.status == "WRITEOFF"
    assert loan_request.overdue == 90


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
def test_remind_before_due_dates(make_loan_request):
    loan_request = make_loan_request(status="DISBURSED")
    loan_request.due_date = date.today()
    loan_request.commit()

    # setup some record that have duedate of 25
    loan_request_ids = SchedulerTask().remind_before_due_dates()
    print(loan_request_ids)
