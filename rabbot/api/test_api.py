"""Tests for the API's public functions."""
# pylint: disable=missing-docstring, invalid-name
from datetime import datetime
from nose.tools import assert_equals

import rabbot.api.core as api
from rabbot.dummydb import DummyDB, client

class TestAPI():

    """Test all api functions."""

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

    def test_list_shifts(self):
        with DummyDB() as db:
            api.db = db
            api.add_shift(1, "1", 1)
            api.add_shift(1, "2", 2)
            api.add_shift(2, "1", 1)
            result = api.list_shifts(1)
            assert_equals(result.count(), 2)

    def test_add_or_edit_user(self):
        with DummyDB() as db:
            api.db = db
            api.add_or_edit_user(1, "1")
            assert_equals(db.records.find().count(), 1)
            api.add_or_edit_user(1, "better name")
            assert_equals(db.records.find().count(), 1)

    def test_get_user(self):
        with DummyDB() as db:
            api.db = db
            api.add_or_edit_user(1, "testuser")
            result = api.get_user(1)
            assert_equals(result['name'], "testuser")

    def test_add_user_to_group(self):
        with DummyDB() as db:
            api.db = db
            api.add_or_edit_user(1, "testuser")
            api.add_user_to_group(1, 24)
            user = api.get_user(1)
            assert_equals(len(user['groups']), 1)
            assert_equals(user['groups'][0], 24)

    def test_remove_user_from_group(self):
        with DummyDB() as db:
            api.db = db
            api.add_or_edit_user(1, "testuser")
            api.add_user_to_group(1, 24)
            api.add_user_to_group(1, 5)
            api.remove_user_from_group(1, 24)
            user = api.get_user(1)
            assert_equals(len(user['groups']), 1)
            assert_equals(user['groups'][0], 5)

    def test_add_mutation(self):
        with DummyDB() as db:
            api.db = db
            api.add_shift(1, "testshift", 1)
            shift = api.get_shift_by_name(1, "testshift")
            api.add_mutation(1, 1, datetime(2016, 1, 1), shift['_id'])
            assert_equals(db.records.find().count(), 2)
