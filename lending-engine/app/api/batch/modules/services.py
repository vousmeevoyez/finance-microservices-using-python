"""
    Investment Services
    _________________
    This is module to process business logic from routes and return API
    response
"""
import pytz
from datetime import datetime, time
from bson import ObjectId

# models
from app.api.models.batch import Batch
# core
from app.api.lib.core.message import RESPONSE as error
from app.api.lib.core.exceptions import BaseError
from app.api.const import BATCH

TIMEZONE = pytz.timezone("Asia/Jakarta")


def which_batch(utc_current):
    """ to determine which batch this investment belongs we use time """
    current_time = utc_current.replace(tzinfo=pytz.utc).astimezone(tz=TIMEZONE).time()

    morning_batch = time(int(BATCH["START"]["HOUR"]),
                         int(BATCH["START"]["MINUTE"]))
    night_batch = time(int(BATCH["END"]["HOUR"]), int(BATCH["END"]["MINUTE"]))

    # 20:00 - 07:59
    if current_time < morning_batch:
        return "MORNING"
    elif current_time > morning_batch and current_time < night_batch:
        return "NIGHT"
    elif current_time >= night_batch:
        return "MORNING"


def create_batch(investment_id, amount):
    """ register investment into batch so we can execute it later through
    scheduler """
    current_time = datetime.now(tz=TIMEZONE)
    morning_batch = current_time
    morning_batch.hour = int(BATCH["START"]["HOUR"])
    morning_batch.minute = int(BATCH["START"]["MINUTE"])

    night_batch = current_time
    night_batch.hour = int(BATCH["END"]["HOUR"])
    night_batch.minute = int(BATCH["END"]["MINUTE"])
