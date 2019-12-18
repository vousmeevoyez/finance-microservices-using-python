import pytz

import pytest
from datetime import datetime, time, timedelta
from freezegun import freeze_time

from app.api.batch.modules.services import (
    check_executed_schedule,
    determine_batch
)
from app.api.models.batch import Schedule, TransactionQueue

# NO OF SCHEDULE SHOULD BE TESTED -> 13.0, 19.0, 8:0, 20:0


@freeze_time("2019-11-11 07:00:00")  # UTC equal to 14.00 WIB
def test_check_schedule():
    """ check schedule in afternoon, there should be 1 schedule """
    schedule_ids = check_executed_schedule()
    assert schedule_ids == []


@freeze_time("2019-11-11 06:00:00")  # UTC equal to 13.00 WIB
def test_check_schedule2():
    """ check schedule in afternoon, there should be 1 schedule """
    schedule_ids = check_executed_schedule()
    assert schedule_ids

@freeze_time("2019-11-11 12:00:00")  # UTC equal to 19.00 WIB
def test_check_schedule3():
    """ check schedule in afternoon, there should be 1 schedule """
    schedule_ids = check_executed_schedule()
    assert schedule_ids

@freeze_time("2019-11-11 01:00:00")  # UTC equal to 08.00 WIB
def test_check_schedule4():
    """ check schedule in afternoon, there should be 1 schedule """
    schedule_ids = check_executed_schedule()
    assert schedule_ids

@freeze_time("2019-11-11 13:00:00")  # UTC equal to 20.00 WIB
def test_check_schedule5():
    """ check schedule in afternoon, there should be 1 schedule """
    schedule_ids = check_executed_schedule()
    assert schedule_ids


@freeze_time("2019-11-11 11:45:00")  # UTC equal to 18.45 WIB
def test_determine_batch():
    """ test determine batch function that decide where transaction should be
    queued """
    result = determine_batch("UPFRONT_FEE")
    assert len(result)
    # because the transaction created around 18.45 this one should be queued
    # 19.00
    schedule_id = result[0]
    schedule = Schedule.find_one({"id": schedule_id})
    assert schedule.executed_at == "19:0"

@freeze_time("2019-11-11 01:45:00")  # UTC equal to 08.45 WIB
def test_determine_batch2():
    """ test determine batch function that decide where transaction should be
    queued """
    result = determine_batch("UPFRONT_FEE")
    assert len(result)
    # because the transaction created around 18.45 this one should be queued
    # 19.00
    schedule_id = result[0]
    schedule = Schedule.find_one({"id": schedule_id})
    assert schedule.executed_at == "13:0"


@freeze_time("2019-11-11 13:45:00")  # UTC equal to 20.45 WIB
def test_determine_batch3():
    """ test determine batch function that decide where transaction should be
    queued """
    result = determine_batch("INVEST_FEE")
    assert len(result)
    # because the transaction created around 18.45 this one should be queued
    # 19.00
    schedule_id = result[0]
    schedule = Schedule.find_one({"id": schedule_id})
    assert schedule.executed_at == "8:0"


@freeze_time("2019-11-11 00:45:00")  # UTC equal to 7.45 WIB
def test_determine_batch4():
    """ test determine batch function that decide where transaction should be
    queued """
    result = determine_batch("INVEST_FEE")
    assert len(result)
    # because the transaction created around 7.45 this one should be queued
    # 13.00
    schedule_id = result[0]
    schedule = Schedule.find_one({"id": schedule_id})
    assert schedule.executed_at == "8:0"

'''
@freeze_time("2019-11-11 00:00:00")  # UTC equal to 07.00 WIB
def test_upfront_fee_batch2():
    """ test upfront fee batch scheduling, if its added at 07.00 then it should
    be executed at 13.00  """
    result = determine_batch("UPFRONT_FEE")
    assert result.time() == time(13, 0)  # equal to 13.00


@freeze_time("2019-11-11 10:00:00")  # UTC equal to 17.00 WIB
def test_upfront_fee_batch3():
    """ test upfront fee batch scheduling, if its added at 17.00 then it should
    be executed at 19.00  """
    result = determine_batch("UPFRONT_FEE")
    assert result.time() == time(19, 0)  # equal to 19.00


@freeze_time("2019-11-11 12:00:00")  # UTC equal to 19.00 WIB
def test_investor_fee_batch():
    """ test investor fee batch scheduling, if its added at 19.00 then it should
    be executed at 20.00  """
    result = determine_batch("INVEST_FEE")
    assert result.time() == time(20, 0)  # equal to 20.00


@freeze_time("2019-11-11 00:00:00")  # UTC equal to 07.00 WIB
def test_investor_fee_batch2():
    """ test investor fee batch scheduling, if its added at 12.00 then it should
    be executed at 12.00  """
    result = determine_batch("INVEST_FEE")
    assert result.time() == time(12, 0)  # equal to 12.00


@freeze_time("2019-11-11 00:00:00")  # UTC 07.00 WIB
def test_upfront_fee_schedule_transaction(make_batch_with_transaction):
    """ we simulate adding a transaction to batch when transaction created in
    morning so expected result this transaction should be processed around
    13.00 """

    asian = pytz.timezone("Asia/Jakarta")
    utc_time = datetime(2019, 11, 11, 6, 0, 0)  # 13.00 WIB in utc
    local = asian.localize(utc_time)
    make_batch_with_transaction("UPFRONT_FEE")
    result = get_batch("UPFRONT_FEE", local)[0]
    assert result["executed_at"] == local
    assert len(result["transactions"]) == 1

@freeze_time("2019-11-11 10:00:00")  # UTC 15.00 WIB
def test_upfront_fee_schedule_afternoon_transaction(make_batch_with_transaction):
    """ we simulate adding a transaction to batch when transaction created in
    morning so expected result this transaction should be processed around
    20.00 """
    asian = pytz.timezone("Asia/Jakarta")
    utc_time = datetime(2019, 11, 11, 12, 0)  # 19.00 WIB in utc
    local = asian.localize(utc_time)
    make_batch_with_transaction("UPFRONT_FEE")
    result = get_batch("UPFRONT_FEE", local)[0]
    assert result["executed_at"] == local
    assert len(result["transactions"]) == 1

@freeze_time("2019-11-11 00:00:00")  # UTC
def test_invest_fee_schedule_transaction(make_batch_with_transaction):
    """ we simulate adding a transaction to batch when transaction created in
    morning so expected result this transaction should be processed around
    13.00 """
    asian = pytz.timezone("Asia/Jakarta")
    utc_time = datetime(2019, 11, 11, 5, 0)  # 12.00 WIB in utc
    local = asian.localize(utc_time)
    make_batch_with_transaction("INVEST_FEE")
    result = get_batch("INVEST_FEE", local)[0]
    assert result["executed_at"] == local
    assert len(result["transactions"]) == 1

@freeze_time("2019-11-11 08:00:00")  # UTC
def test_upfront_fee_schedule_afternoon_transaction(
    make_batch_with_transaction
):
    """ we simulate adding a transaction to batch when transaction created in
    morning so expected result this transaction should be processed around
    13.00 """
    asian = pytz.timezone("Asia/Jakarta")
    utc_time = datetime(2019, 11, 11, 12, 0)  # 12.00 WIB in utc
    local = asian.localize(utc_time)
    make_batch_with_transaction("UPFRONT_FEE")
    result = get_batch("UPFRONT_FEE", local)[0]
    assert result["executed_at"] == local
    assert len(result["transactions"]) == 1
'''
