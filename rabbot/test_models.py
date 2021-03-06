"""Empty database context manager to simplify testing."""
from nose.tools import assert_equals

from rabbot.models import User, Schedule, Shift, Mutation
from rabbot.dummydb import DummyDB

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
        session.add_all([user, schedule, shift, mutation])
        session.flush()
        assert_equals(schedule.shifts[0].name, "first shift")
