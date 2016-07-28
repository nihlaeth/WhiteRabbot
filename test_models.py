from datetime import datetime, timedelta

import pytest

from models import Shift


NOW = datetime.now()


def hours(hours: int) -> timedelta:
    return timedelta(hours=hours)


class TestShift:

    def test_creation(self):
        """I can create a shift using two datetimes."""
        shift = Shift(NOW, NOW + hours(1))
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
        shift = Shift(start, stop)
        assert shift.is_active(at) == expected
