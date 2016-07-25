from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
class Mutation(BASE):
    """Mutations to the regular schedule."""
    __tablename__ = 'mutations'
    mutation_id = Column(Integer, primary_key=True)
    shift_date = Column(DateTime)
    shift_id = Column(ForeignKey)
    mutator = Column(ForeignKey)
    new_user_id = Column(ForeignKey)

engine = create_engine('sqlite:///rabbot.sqlite', echo=False)
SESSION.configure(bind=engine)
BASE.metadata.create_all(engine)
with SessionScope() as session:
    pass
