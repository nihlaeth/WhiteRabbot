from datetime import datetime
from typing import Optional


class Person:
    """Somebody who works, and may cover a shift."""

    def __init__(self, name: str) -> None:
        self.name = name


defaultPerson = Person('DEFAULT')


class Shift:
    """One specific shift where one Person should be working.

    If there is an evening shift from 17:00 to 19:00 every day, this might be
    the evening shift of 2016-12-31.
    """

    def __init__(
            self,
            start: datetime,
            stop: datetime,
            ) -> None:
        self.start = start
        self.stop = stop
        self.mutations = []  # type: List[Mutation]

    @property
    def cover(self) -> Optional[Person]:
        if not self.mutations:
            return defaultPerson
        else:
            return self.mutations[-1].new_person

    @cover.setter
    def cover(self, x: Optional[Person]) -> None:
        self.mutations.append(Mutation(shift=self, new_person=x))

    def is_active(self, at: datetime) -> bool:
        """Is this shift active at time `at`?"""
        return self.start <= at < self.stop

    def remove_cover(self) -> None:
        """Stop covering the shift"""
        self.cover = None

    def is_covered(self) -> bool:
        """Is there somebody covering this shift?"""
        return self.cover is not None

    class AlreadyCovered(Exception):
        """Raised if the shift is already covered (by somebody else)"""
        pass

    def set_cover(self, cover: Person) -> None:
        """Add cover if the new cover makes sense

        Parameters
        ----------
        cover: Person
            The person who will be covering this shift

        Returns
        -------
        None

        Side effects
        ------------
        The cover person will be set as the shift's cover.

        Raises
        ------
        Shift.AlreadyCovered
            if the shift already has somebody else as cover
        """
        if self.cover is None:
            # The shift is free, cover it and return
            self.cover = cover
            return
        if self.cover == cover:
            # The shift is already covered by this person, do nothing
            return
        # The shift is already covered by somebody else, you can't just take it
        raise self.AlreadyCovered  # type: ignore  # silence a mypy bug


class Mutation:
    """A change in the Person who covers a Shift"""

    def __init__(self, shift: Shift, new_person: Optional[Person]) -> None:
        self.shift = shift
        self.new_person = new_person
