"""Empty database context manager to simplify testing."""
from pymongo import MongoClient

_client = MongoClient()

# pylint: disable=too-few-public-methods,missing-docstring
class DummyDB(object):

    """Provide a temporary, totally empty database."""

    def __init__(self):
        """Create database."""
        self._db = _client.test_white_rabbot

    def __enter__(self):
        """Return db."""
        return self._db

    def __exit__(self, e_type, e_value, traceback):
        """Destroy database."""
        _client.drop_database('test_white_rabbot')
