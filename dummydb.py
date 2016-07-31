"""Empty database context manager to simplify testing."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# pylint: disable=wildcard-import,unused-wildcard-import
from models import *

# pylint: disable=too-few-public-methods,missing-docstring
class DummyDB(object):

    """Provide a temporary, totally empty, database in RAM."""

    def __init__(self, debug=False):
        """Create database, BASE metadata and sessionfactory."""
        # Normally Session is not a valid name, but sessionmaker is
        # a generator, so it will actually house a class definition.
        # pylint: disable=invalid-name
        self._Session = sessionmaker()
        self._engine = create_engine('sqlite:///:memory:', echo=debug)
        self._Session.configure(bind=self._engine)
        BASE.metadata.create_all(self._engine)
        self._session = None

    def __enter__(self):
        """Return a fresh session."""
        self._session = self._Session()
        return self._session

    def __exit__(self, e_type, e_value, traceback):
        """Commit or rollback and cleanup."""
        if e_type is not None:
            # Exception occured
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()
