from datetime import datetime


class Shift:
    def __init__(self, start: datetime, stop: datetime) -> None:
        self.start = start
        self.stop = stop
