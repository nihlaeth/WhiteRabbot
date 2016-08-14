"""Tests for API."""
# pylint: disable=missing-docstring, invalid-name
from nose.tools import assert_equals

from dummydb import DummyDB
import api
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
        result = api.list_shifts(session, 1)
        assert_equals(len(result.value), 2)
        assert_equals(result.value[0].name, "shift1")


class Test_add_shift():

    def test_valid_data(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            session.add(schedule)
            session.flush()

            result = api.add_shift(session, 1, 'Evening shift', 0)

            assert_equals(result.success, True)
            assert_equals(result.value.name, 'Evening shift')

    def test_it_rejects_invalid_group_id(self):
        with DummyDB() as session:
            # Schedule 4 does not exist.
            result = api.add_shift(session, 4, 'Evening shift', 0)

            assert_equals(result.success, False)

    def test_it_rejects_empty_name(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            session.add(schedule)
            session.flush()

            result = api.add_shift(session, 1, '', 0)

            assert_equals(result.success, False)

    def test_it_rejects_non_string_name(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            session.add(schedule)
            session.flush()

            result = api.add_shift(session, 1, 123, 0)

            assert_equals(result.success, False)

    def test_it_rejects_non_int_ordering(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            session.add(schedule)
            session.flush()

            result = api.add_shift(session, 1, 'Evening', '2')

            assert_equals(result.success, False)


class Test_delete_shift():

    def test_valid_data(self):
        with DummyDB() as session:
            shift = Shift(name="test")
            session.add(shift)
            session.flush()
            result = api.delete_shift(session, 1)
            assert_equals(result.success, True)

    def test_non_existing_id(self):
        with DummyDB() as session:
            result = api.delete_shift(session, 1)
            assert_equals(result.success, False)
