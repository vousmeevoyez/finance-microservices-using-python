import pytest
from datetime import datetime
from freezegun import freeze_time

from app.api.batch.modules.services import which_batch


@freeze_time("2019-11-11 00:00:00")
def test_morning_batch():
    """ test indonesia local time 07:00
        should be executed at morning
    """
    timestamp = datetime.utcnow()
    result = which_batch(timestamp)
    assert result == "MORNING"


@freeze_time("2019-11-11 01:59:00")
def test_morning_batch2():
    """ test indonesia local time 08:00
        should be executed at morning
    """
    timestamp = datetime.utcnow()
    result = which_batch(timestamp)
    assert result == "NIGHT"


@freeze_time("2019-11-11 00:59:00")
def test_morning_batch3():
    """ test indonesia local time 07:00
        should be executed at morning
    """
    timestamp = datetime.utcnow()
    result = which_batch(timestamp)
    assert result == "MORNING"


@freeze_time("2019-11-11 03:00:00")
def test_afternoon_batch():
    """ test indonesia local time 10:00 
        should be executed at night then
    """
    timestamp = datetime.utcnow()
    result = which_batch(timestamp)
    assert result == "NIGHT"


@freeze_time("2019-11-11 13:00:00")
def test_night_batch():
    """ test indonesia local time 20:00 
        should be executed at night then
    """
    timestamp = datetime.utcnow()
    result = which_batch(timestamp)
    assert result == "MORNING"


@freeze_time("2019-11-11 15:00:00")
def test_night_batch2():
    """ test indonesia local time 23:00 
        should be executed at morning then
    """
    timestamp = datetime.utcnow()
    result = which_batch(timestamp)
    assert result == "MORNING"

