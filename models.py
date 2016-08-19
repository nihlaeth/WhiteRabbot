from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from db import SessionScope, get_or_create, engine

BASE = declarative_base()


class Person(BASE):
    """Somebody who works, and may cover a shift."""

    __tablename__ = 'people'
    id = Column(name='person_id', type_=Integer, primary_key=True)
    name = Column(String)


class Shift(BASE):
    """One specific shift where one Person should be working.

    If there is an evening shift from 17:00 to 19:00 every day, this might be
    the evening shift of 2016-12-31.
    """

    __tablename__ = 'shifts'
    id = Column(name='shift_id', type_=Integer, primary_key=True)
    start = Column(DateTime)
    stop = Column(DateTime)

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

    mutations = relationship("Mutation", back_populates="shift")


class Mutation(BASE):
    """A change in the Person who covers a Shift"""

    __tablename__ = 'mutations'
    id = Column(name='mutation_id', type_=Integer, primary_key=True)
    shift_id = Column('shift_id', Integer, ForeignKey('shifts.shift_id'))
    new_person = Column('new_person', Integer,
                        ForeignKey('people.person_id'))

    shift = relationship("Shift")

    def __eq__(self, other):
        return (
            type(other) is Mutation
            and type(self) is Mutation
            and self.shift == other.shift
            and self.new_person == other.new_person
        )

    def __str__(self):
        return '<Mutation {id}: {person} on shift {shift}>'.format(
            id=self.id,
            person=self.new_person.name if self.new_person is not None else 'None',
            shift=self.shift_id
        )

    def __repr__(self):
        return str(self)


BASE.metadata.create_all(engine)


# Ensure defaultPerson exists
with SessionScope() as session:
    defaultPerson = get_or_create(session, Person, name='DEFAULT')
