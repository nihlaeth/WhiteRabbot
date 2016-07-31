from datetime import datetime, timedelta

import pytest

import models


NOW = datetime.now()


def hours(hours: int) -> timedelta:
    return timedelta(hours=hours)


class TestShift:

    def test_init(self):
        """I can create a shift using two datetimes."""
        shift = models.Shift(NOW, NOW + hours(1))
        assert shift.start == NOW
        assert shift.stop == NOW + hours(1)

    @pytest.mark.parametrize(
        'start, stop, at, expected',
        [
            (NOW - hours(1), NOW           , NOW, False) , # past
            (NOW           , NOW + hours(1), NOW, True)  , # present
            (NOW + hours(1), NOW + hours(2), NOW, False) , # future
        ]
    )
    def test_is_active(self, start, stop, at, expected):
        """Shift.is_active handles shifts before, after, and containing `at`"""
        shift = models.Shift(start, stop)
        assert shift.is_active(at) == expected

    class Test_cover:

        def test_default_cover_is_defaultPerson(self):
            """A pristine shift is covered by defaultPerson"""
            shift = models.Shift(NOW, NOW)
            assert shift.cover == models.defaultPerson

        def test_cover_setter_to_None(self):
            """A shift's cover can be set to None"""
            shift = models.Shift(NOW, NOW)
            shift.cover = None
            assert shift.cover is None

        def test_cover_setter_to_person(self):
            """A shift's cover can be set to a person"""
            shift = models.Shift(NOW, NOW)
            alice = models.Person('Alice')
            shift.cover = alice
            assert shift.cover == alice

    def test_a_normal_shift_is_covered(self):
        """By default, a shift is covered by defaultPerson"""
        shift = models.Shift(NOW, NOW)
        assert shift.is_covered()
        assert shift.cover is models.defaultPerson

    def test_a_shift_may_be_uncovered(self):
        """You can remove a shift's cover, and it will be uncovered"""
        shift = models.Shift(NOW, NOW)
        shift.remove_cover()
        assert not shift.is_covered()


class TestPerson:

    def test_init(self):
        """I can create a Person"""
        person = models.Person(name='Alice van Wonderland')
        assert person.name == 'Alice van Wonderland'


class TestMutation:

    def test_init(self):
        """I can create a Mutation"""
        shift = models.Shift(NOW, NOW)
        alice = models.Person(name='Alice van Wonderland')
        mutation = models.Mutation(shift=shift, new_person=alice)
        assert mutation.shift == shift
        assert mutation.new_person == alice
