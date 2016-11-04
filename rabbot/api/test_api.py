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

    def test_add_substitute_to_mutation(self):
        with DummyDB() as db:
            api.db = db
            api.add_shift(1, "testshift", 1)
            shift = api.get_shift_by_name(1, "testshift")
            api.add_mutation(1, 1, datetime(2016, 1, 1), shift['_id'])
            mutation = db.records.find_one({'type': 'mutation'})
            api.add_substitute_to_mutation(mutation['_id'], 2)
            mutation = db.records.find_one({'type': 'mutation'})
            assert_equals(mutation['sub_tuid'], 2)

    def test_list_mutations(self):
        with DummyDB() as db:
            api.db = db
            api.add_shift(1, "nomatch", 1)
            api.add_shift(1, "match", 1)
            nomatch = api.get_shift_by_name(1, "nomatch")
            match = api.get_shift_by_name(1, "match")
            api.add_mutation(1, 1, datetime(2016, 1, 1), nomatch['_id'])
            api.add_mutation(1, 1, datetime(2016, 1, 2), match['_id'])
            api.add_mutation(1, 1, datetime(2016, 1, 3), match['_id'])
            api.add_mutation(1, 1, datetime(2016, 1, 4), match['_id'])
            api.add_mutation(1, 1, datetime(2016, 1, 5), nomatch['_id'])
            result = api.list_mutations(1)
            assert_equals(result.count(), 5)
            result = api.list_mutations(1, start_date=datetime(2016, 1, 2))
            assert_equals(result.count(), 4)
            result = api.list_mutations(1, end_date=datetime(2016, 1, 2))
            assert_equals(result.count(), 2)
            result = api.list_mutations(
                1,
                start_date=datetime(2016, 1, 2),
                end_date=datetime(2016, 1, 4))
            assert_equals(result.count(), 3)
            for doc in result:
                assert_equals(doc['shift_id'], match['_id'])
