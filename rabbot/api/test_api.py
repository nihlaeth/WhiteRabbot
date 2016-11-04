"""Tests for the API's public functions."""
# pylint: disable=missing-docstring, invalid-name
from nose.tools import assert_equals

import rabbot.api.core as api
from rabbot.dummydb import DummyDB, client

class TestShifts():

    """Test all shift functions."""

    def __init__(self):
        api.client = client

    def test_add_shift(self):
        with DummyDB() as db:
            api.db = db
            api.add_shift(1, "test", 1)
            assert_equals(
                db.records.find().count(),
                1)

    def test_delete_record(self):
        with DummyDB() as db:
            api.db = db
            api.add_shift(1, "test", 1)
            shift = db.records.find_one()
            api.delete_record(shift['_id'])
            assert_equals(
                db.records.find().count(),
                0)

    def test_get_shift_by_name(self):
        with DummyDB() as db:
            api.db = db
            api.add_shift(1, "test", 1)
            shift = api.get_shift_by_name(1, "test")
            assert_equals(shift['name'], "test")
