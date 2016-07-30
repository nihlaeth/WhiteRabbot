"""Database models."""
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


# pylint: disable=no-init

class User(BASE):
    """Usertable."""
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer)
    name = Column(String)

class Shift(BASE):
    """Shift definitions."""
    __tablename__ = 'shifts'
    shift_id = Column(Integer, primary_key=True)
    schedule_id = Column(ForeignKey('schedules.schedule_id'))
    schedule = relationship("Schedule", back_populates="shifts")
    name = Column(String)
    ordering = Column(Integer)
    mutations = relationship("Mutation", back_populates="shifts")

class Mutation(BASE):
    """Mutations to the regular schedule."""
    __tablename__ = 'mutations'
    mutation_id = Column(Integer, primary_key=True)
    schedule_id = Column(ForeignKey('schedules.schedule_id'))
    schedule = relationship("Schedule", back_populates="mutations")
    shift_date = Column(DateTime)
    shift_id = Column(ForeignKey('shifts.shift_id'))
    shift = relationship("Shift", back_populates="mutations")
    mutator = Column(ForeignKey('users.user_id'))
    new_user_id = Column(ForeignKey('users.user_id'))

class Schedule(BASE):
    """Schedule for users and mutations to belong to."""
    __tablename__ = 'schedules'
    schedule_id = Column(Integer, primary_key=True)
    telegram_group_id = Column(Integer)
    admin_id = Column(ForeignKey('users.user_id'))
    mutations = relationship("Mutation", back_populates="schedules")
    shifts = relationship("Shift", back_populates="schedules")

# pylint: disable=invalid-name
engine = create_engine('sqlite:///:memory:', echo=True)
SESSION.configure(bind=engine)
BASE.metadata.create_all(engine)
with SessionScope() as session:
    pass
