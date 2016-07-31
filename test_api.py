"""Tests for API."""
from nose.tools import assert_equals

from dummydb import DummyDB
from api import list_shifts
from models import Schedule, Shift

def test_list_shifts():
    with DummyDB() as session:
        schedule = Schedule(telegram_group_id=1)
        shift1 = Shift(schedule=schedule, name="shift1", ordering=1)
        shift2 = Shift(schedule=schedule, name="shift2", ordering=2)
        other_schedule = Schedule(telegram_group_id=2)
        shift3 = Shift(schedule=other_schedule, name="shift3", ordering=1)
        session.add_all([schedule, other_schedule, shift1, shift2, shift3])
        session.flush()
        result = list_shifts(session, 1)
        assert_equals(len(result), 2)
        assert_equals(result[0].name, "shift1")
