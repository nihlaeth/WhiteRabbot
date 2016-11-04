"""Empty database context manager to simplify testing."""
from pymongo import MongoClient

client = MongoClient()

# pylint: disable=too-few-public-methods,missing-docstring
class DummyDB(object):

    """Provide a temporary, totally empty database."""

    def __init__(self):
        """Create database."""
        self._db = client.test_white_rabbot

    def __enter__(self):
        """Return db."""
        return self._db

    def __exit__(self, e_type, e_value, traceback):
        """Destroy database."""
        client.drop_database('test_white_rabbot')
