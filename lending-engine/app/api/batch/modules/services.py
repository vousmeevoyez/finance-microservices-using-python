"""
    Batch Processing Services
    _________________
    This is module to process business logic from routes and return API
    response
"""
import pytz
from bson import Decimal128
from datetime import datetime, time, timedelta
from bson import ObjectId
from bson.codec_options import CodecOptions

from flask import current_app

# models
from app.api.models.batch import Schedule, TransactionQueue

# core
from app.api.lib.core.message import RESPONSE as error
from app.api.lib.core.exceptions import BaseError


TIMEZONE = pytz.timezone("Asia/Jakarta")


def convert_string_to_datetime(hour_minute, is_local=True):
    """ convert stored HH:MM to datetime so it easier to operate"""
    now = datetime.utcnow()
    local_now = TIMEZONE.localize(now)

    hour, minute = hour_minute.split(":")
    result = local_now.replace(hour=int(hour), minute=int(minute))
    if is_local is False:
        # remove local timezone
        result = now.replace(hour=int(hour), minute=int(minute))
        # revert offset to original time
        result = result - timedelta(hours=7)
    return result


def convert_to_localtime(now):
    """ convert HH:MM to HH:MM offset + 7"""
    local_now = TIMEZONE.localize(now)
    return local_now + timedelta(hours=7)


def convert_start_end_to_datetime(start, end):
    start_datetime = convert_string_to_datetime(start, is_local=False)
    end_datetime = convert_string_to_datetime(end, is_local=False)
    # if start date more than end time
    if start_datetime > end_datetime:
        start_datetime = start_datetime - timedelta(days=1)
    return start_datetime, end_datetime


def convert_list_of_string_to_datetime(schedules):
    """ convert list contain string start, end and executed at to datetime """
    # we need convert all time schedule into python datetime
    converted_schedules = []
    for schedule in schedules:
        # convert start hour into datetime
        start = convert_string_to_datetime(schedule.start)
        end = convert_string_to_datetime(schedule.end)
        executed_at = convert_string_to_datetime(schedule.executed_at)
        converted_schedules.append(
            {
                "schedule_id": schedule.id,
                "start": start,
                "end": end,
                "executed_at": executed_at,
            }
        )
    return converted_schedules


def check_hour_in_range(times, compared_hour):
    result = False
    # if start time less than end time
    if times["start"] < times["end"]:
        # check if its hour in range or not
        if times["start"] <= compared_hour <= times["end"]:
            result = True
    # if start date more than end time
    else:
        # if start date more than end time
        if times["start"] <= compared_hour or compared_hour <= times["end"]:
            result = True
    return result


def check_executed_schedule():
    """ based on current time we check whether there are schedule that should
    be executed or not"""
    # convert from utc to local offset
    now = datetime.utcnow()
    local_now = convert_to_localtime(now)

    schedules = list(Schedule.find())
    # now we check whether currently there are schedule or not
    schedule_ids = []
    for schedule in schedules:
        # convert executed at to today!
        hour, minute = (schedule.executed_at).split(":")
        executed_at = local_now.replace(hour=int(hour), minute=int(minute))
        # replace micro to zero so it can enter the executed range
        executed_at = executed_at.replace(microsecond=0)
        # give some time margin because its not possible to execute at 0 ms
        tolerated_executed_at = executed_at + timedelta(minutes=1)
        is_in_range = bool(executed_at <= local_now <= tolerated_executed_at)
        if is_in_range:
            schedule_ids.append(schedule.id)
    return schedule_ids


def determine_batch(schedule_name):
    """ to determine which based on schedule name this transaction should go to
    which batch """
    # get current time
    now = datetime.utcnow()
    local_now = convert_to_localtime(now)
    # get schedules for particular schedule
    schedules = Schedule.find({"name": schedule_name})

    # we convert the array into array of datetime so it operable
    converted_schedules = convert_list_of_string_to_datetime(schedules)
    schedule_ids = []
    for x in converted_schedules:
        # if current time are in range of schedule we pick it
        is_in_range = check_hour_in_range(x, local_now)
        if is_in_range:
            schedule_ids.append(x["schedule_id"])
    return schedule_ids


def schedule_transaction(
    schedule_name,
    wallet_id,
    source_id,
    source_type,
    destination_id,
    destination_type,
    amount,
    transaction_type,
    model,
    model_id,
    status,
):
    """ schedule transaction information to transaction queue """
    # second we need to determine which batch this transaction should executed
    schedule_ids = determine_batch(schedule_name)
    queue = TransactionQueue(
        schedule_id=schedule_ids[0],
        wallet_id=wallet_id,
        source_id=source_id,
        source_type=source_type,
        destination_id=destination_id,
        destination_type=destination_type,
        amount=amount,
        transaction_type=transaction_type,
        transaction_info={"model": model, "model_id": model_id, "status": status},
    )
    queue.commit()
    return queue.id
