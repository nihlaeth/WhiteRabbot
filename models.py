from datetime import datetime


class Shift:
    """One specific shift where somebody should be working.

    If there is an evening shift from 17:00 to 19:00 every day, this might be
    the evening shift of 2016-12-31.
    """

    def __init__(self, start: datetime, stop: datetime) -> None:
        self.start = start
        self.stop = stop

    def is_active(self, at: datetime) -> bool:
        """Is this shift active at time `at`?"""
        return self.start <= at < self.stop
