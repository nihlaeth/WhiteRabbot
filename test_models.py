from datetime import datetime, timedelta

import pytest

import models


NOW = datetime.now()


def hours(hours: int) -> timedelta:
    return timedelta(hours=hours)


@pytest.fixture
def shift() -> models.Shift:
    """Return a shift that just started"""
    return models.Shift(start=NOW, stop=NOW + hours(1))


class TestShift:

    def test_init(self):
        """I can create a shift using two datetimes."""
        shift = models.Shift(start=NOW, stop=NOW + hours(1))
        assert shift.start == NOW
        assert shift.stop == NOW + hours(1)

    @pytest.mark.parametrize(
        'start, stop, at, expected',
        [
            (NOW - hours(1), NOW           , NOW, False),  # past
            (NOW           , NOW + hours(1), NOW, True) ,  # present
            (NOW + hours(1), NOW + hours(2), NOW, False),  # future
        ]
    )
    def test_is_active(self, start, stop, at, expected):
        """Shift.is_active handles shifts before, after, and containing `at`"""
        shift = models.Shift(start=start, stop=stop)
        assert shift.is_active(at) == expected

    class Test_cover:

        def test_default_cover_is_defaultPerson(self, shift):
            """A pristine shift is covered by defaultPerson"""
            assert shift.cover == models.defaultPerson

        def test_cover_setter_to_None(self, shift):
            """A shift's cover can be set to None"""
            shift.cover = None
            assert shift.cover is None

        def test_cover_setter_to_person(self, shift):
            """A shift's cover can be set to a person"""
            alice = models.Person(name='Alice')
            shift.cover = alice
            assert shift.cover == alice

        def test_setting_cover_creates_mutations(self, shift):
            from pprint import pprint as pp
            pp(shift.mutations)
            alice = models.Person(name='Alice')
            brian = models.Person(name='Brian')
            shift.remove_cover()
            shift.cover = alice
            shift.cover = brian
            shift.remove_cover()
            expected_mutations = [
                models.Mutation(shift=shift, new_person=None),
                models.Mutation(shift=shift, new_person=alice),
                models.Mutation(shift=shift, new_person=brian),
                models.Mutation(shift=shift, new_person=None),
            ]
            assert shift.mutations == expected_mutations

    def test_a_normal_shift_is_covered(self, shift):
        """By default, a shift is covered by defaultPerson"""
        assert shift.is_covered()
        assert shift.cover is models.defaultPerson

    def test_a_shift_may_be_uncovered(self, shift):
        """You can remove a shift's cover, and it will be uncovered"""
        shift.remove_cover()
        assert not shift.is_covered()


class TestPerson:

    def test_init(self):
        """I can create a Person"""
        person = models.Person(name='Alice van Wonderland')
        assert person.name == 'Alice van Wonderland'


class TestMutation:

    def test_init(self, shift):
        """I can create a Mutation"""
        alice = models.Person(name='Alice van Wonderland')
        mutation = models.Mutation(shift=shift, new_person=alice)
        assert mutation.shift == shift
        assert mutation.new_person == alice
