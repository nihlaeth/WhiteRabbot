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
        'start,stop,expected',
        [
            (NOW - hours(1), NOW, False),  # past
            (NOW, NOW + hours(1), True),  # present
            (NOW + hours(1), NOW + hours(2), False),  # future
        ]
    )
    def test_is_active(self, start, stop, expected):
        """Test is_active"""
        shift = Shift(start, stop)
        assert shift.is_active() == expected
