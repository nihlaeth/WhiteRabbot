"""Database models."""
from sqlalchemy.schema import Table
from sqlalchemy import ForeignKey, Column, Integer, DateTime, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SESSION = sessionmaker()
BASE = declarative_base()

# This is a context manager, it does not need any public methods.
# pylint: disable=too-few-public-methods
class SessionScope(object):
    """Content manager that creates sessions."""
    def __init__(self):
        """Create a session."""
        self._session = SESSION()
    def __enter__(self):
        """Return the session."""
        return self._session
    def __exit__(self, e_type, e_value, trace):
        """Commit or roll back, then do cleanup."""
        if e_type is not None:
            # Exception occured
            self._session.rollback()
        else:
            self._session.commit()
            self._session.close()


# pylint: disable=no-init,invalid-name

association_table = Table(
    'association',
    BASE.metadata,
    Column('schedule_id', Integer, ForeignKey('schedules.schedule_id')),
    Column('user_id', Integer, ForeignKey('users.user_id')))

class User(BASE):
    """Usertable."""
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer)
    name = Column(String)
    schedules = relationship(
        "Schedule",
        secondary=association_table,
        back_populates="users")

class Shift(BASE):
    """Shift definitions."""
    __tablename__ = 'shifts'
    shift_id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedules.schedule_id'))
    schedule = relationship("Schedule", back_populates="shifts")
    name = Column(String)
    ordering = Column(Integer)
    mutations = relationship("Mutation", back_populates="shift")

class Mutation(BASE):
    """Mutations to the regular schedule."""
    __tablename__ = 'mutations'
    mutation_id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedules.schedule_id'))
    schedule = relationship("Schedule", back_populates="mutations")
    shift_date = Column(DateTime)
    shift_id = Column(Integer, ForeignKey('shifts.shift_id'))
    shift = relationship("Shift", back_populates="mutations")
    mutator_id = Column(Integer, ForeignKey('users.user_id'))
    mutator = relationship(
        "User",
        # back_populates="mutations",
        foreign_keys=[mutator_id])
    new_user_id = Column(Integer, ForeignKey('users.user_id'))
    new_user = relationship(
        "User",
        # back_populates="mutations",
        foreign_keys=[new_user_id])

class Schedule(BASE):
    """Schedule for users and mutations to belong to."""
    __tablename__ = 'schedules'
    schedule_id = Column(Integer, primary_key=True)
    telegram_group_id = Column(Integer)
    admin_id = Column(Integer, ForeignKey('users.user_id'))
    admin = relationship(
        "User",
        # back_populates="schedules",
        foreign_keys=[admin_id])
    mutations = relationship("Mutation", back_populates="schedule")
    shifts = relationship(
        "Shift",
        back_populates="schedule",
        order_by="asc(Shift.ordering)")
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="schedules")

def init_db():
    engine = create_engine('sqlite:///:memory:', echo=True)
    SESSION.configure(bind=engine)
    BASE.metadata.create_all(engine)
