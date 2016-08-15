"""Tests for API."""
# pylint: disable=missing-docstring, invalid-name
from nose.tools import assert_equals

from dummydb import DummyDB
import api
from models import Schedule, Shift, User

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

class Test_edit_shift():

    def test_valid_data(self):
        with DummyDB() as session:
            shift = Shift(name="test", ordering=0)
            session.add(shift)
            session.flush()
            result = api.edit_shift(session, 1, "new test", 1)
            assert_equals(result.success, True)
            assert_equals(shift.name, "new test")
            assert_equals(shift.ordering, 1)

    def test_non_existing_id(self):
        with DummyDB() as session:
            result = api.edit_shift(session, 1, "new test", 1)
            assert_equals(result.success, False)

    def test_invalid_name(self):
        with DummyDB() as session:
            shift = Shift(name="test", ordering=0)
            session.add(shift)
            session.flush()
            result = api.edit_shift(session, 1, None, 1)
            assert_equals(result.success, False)

    def test_invalid_ordering(self):
        with DummyDB() as session:
            shift = Shift(name="test", ordering=0)
            session.add(shift)
            session.flush()
            result = api.edit_shift(session, 1, "test2", None)
            assert_equals(result.success, False)

class Test_get_schedule():

    def test_valid_data(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            session.add(schedule)
            session.flush()
            result = api.get_schedule(session, 1)
            assert_equals(result.success, True)

    def test_non_existing_id(self):
        with DummyDB() as session:
            result = api.get_schedule(session, 1)
            assert_equals(result.success, False)


# pylint: disable=protected-access
class Test_validate_ordering():

    def test_valid_data(self):
        result = api._validate_ordering(1)
        assert_equals(result.success, True)
        assert_equals(result.value, 1)

    def test_non_int(self):
        result = api._validate_ordering("not an int")
        assert_equals(result.success, False)


class Test_validate_shift_name():

    def test_valid_data(self):
        result = api._validate_shift_name("test")
        assert_equals(result.success, True)
        assert_equals(result.value, "test")

    def test_non_str(self):
        result = api._validate_shift_name(0)
        assert_equals(result.success, False)

    def test_empty_str(self):
        result = api._validate_shift_name("")
        assert_equals(result.success, False)


class Test_get_shift_by_id():

    def test_valid_data(self):
        with DummyDB() as session:
            shift = Shift()
            session.add(shift)
            session.flush()
            result = api.get_shift_by_id(session, 1)
            assert_equals(result.success, True)
            assert_equals(result.value.shift_id, 1)

    def test_non_valid_id(self):
        with DummyDB() as session:
            result = api.get_shift_by_id(session, 1)
            assert_equals(result.success, False)


class Test_get_shift_by_name():

    def test_valid_data(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            shift = Shift(schedule=schedule, name="test")
            session.add_all([schedule, shift])
            session.flush()
            result = api.get_shift_by_name(session, 1, "test")
            assert_equals(result.success, True)

    def test_non_existent_schedule(self):
        with DummyDB() as session:
            shift = Shift(name="test")
            session.add_all([shift])
            session.flush()
            result = api.get_shift_by_name(session, 1, "test")
            assert_equals(result.success, False)

    def test_non_related_schedule(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            shift = Shift(name="test")
            session.add_all([schedule, shift])
            session.flush()
            result = api.get_shift_by_name(session, 1, "test")
            assert_equals(result.success, False)

    def test_invalid_name(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            shift = Shift(schedule=schedule, name="test")
            session.add_all([schedule, shift])
            session.flush()
            result = api.get_shift_by_name(session, 1, 0)
            assert_equals(result.success, False)

    def test_no_matching_shift(self):
        with DummyDB() as session:
            schedule = Schedule(telegram_group_id=1)
            shift = Shift(schedule=schedule, name="Some shift")
            session.add_all([schedule, shift])
            session.flush()
            result = api.get_shift_by_name(session, 1, "test")
            assert_equals(result.success, False)


class Test_get_schedule_by_id():

    def test_valid_data(self):
        with DummyDB() as session:
            schedule = Schedule()
            session.add(schedule)
            session.flush()
            result = api.get_schedule_by_id(session, 1)
            assert_equals(result.success, True)

    def test_non_existing_id(self):
        with DummyDB() as session:
            result = api.get_schedule_by_id(session, 1)
            assert_equals(result.success, False)

class Test_get_user():

    def test_valid_data(self):
        with DummyDB() as session:
            user = User(telegram_user_id=1)
            session.add(user)
            session.flush()
            result = api.get_user(session, 1)
            assert_equals(result.success, True)

    def test_non_existing_id(self):
        with DummyDB() as session:
            result = api.get_user(session, 1)
            assert_equals(result.success, False)


class Test_add_schedule():

    def test_valid_data(self):
        with DummyDB() as session:
            user = User(telegram_user_id=1)
            session.add(user)
            session.flush()
            result = api.add_schedule(session, 1, 1)
            assert_equals(result.success, True)
            assert_equals(result.value.schedule_id, 1)

    def test_non_existent_admin(self):
        with DummyDB() as session:
            result = api.add_schedule(session, 1, 1)
            assert_equals(result.success, False)
