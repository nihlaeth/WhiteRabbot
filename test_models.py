"""Empty database context manager to simplify testing."""
from nose.tools import assert_equals

from models import User, Schedule, Shift, Mutation
from dummydb import DummyDB

# pylint: disable=missing-docstring

def test_some_random_models():
    with DummyDB() as session:
        user = User(telegram_user_id=1, name="Testuser")
        schedule = Schedule(telegram_group_id=1, admin=user, users=[user])
        shift = Shift(schedule=schedule, name="first shift", ordering=1)
        mutation = Mutation(
            schedule=schedule,
            shift_date=None,
            shift=shift,
            mutator=user)
        assert_equals(schedule.shifts[0].name, "first shift")
