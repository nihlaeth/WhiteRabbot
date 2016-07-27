from datetime import datetime, timedelta

import pytest

from models import Shift


@pytest.fixture
def now():
    return datetime.now()


@pytest.fixture
def one_hour():
    return timedelta(hours=1)


class TestShift:
    def test_creation(self, now, one_hour):
        """I can create a shift using two datetimes."""
        shift = Shift(now, now + one_hour)
        assert shift.start == now
        assert shift.stop == now + one_hour

    def test_is_active(self):
        """A shift knows whether it is active."""
        pass
