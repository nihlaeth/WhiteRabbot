"""API for interacting with database."""
from typing import Optional, Dict
from datetime import date

from pymongo import MongoClient
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from .helpers import (
    InvalidInput,
    validate_ordering,
    validate_name,
    validate_delete_result,
    validate_insert_one_result,
    validate_update_result)


client = MongoClient()
db = client.white_rabbot


def get_shift_by_name(telegram_group_id: int, shift_name: str) -> Optional[Dict]:
    """Fetch shift by name."""
    validate_name(shift_name)
    return db.records.find_one({
        'telegram_group_id': telegram_group_id,
        'name': shift_name,
        'type': 'shift'})


def list_shifts(telegram_group_id: int) -> Cursor:
    """List all shifts belonging to the telegram group."""
    return db.records.find({
        'telegram_group_id': telegram_group_id,
        'type': 'shift'})


def add_shift(telegram_group_id: int, name: str, ordering: int) -> None:
    """Add a new shift to the session."""
    # scenarios
    # - name already exists for this group_id
    #   -> Telegram iface should say "name already exists for this group"
    # - name is an empty string
    #   -> Telegram iface should say "you must enter a name"
    # - name cannot be converted to string
    #   -> raise Error
    # - ordering cannot be converted to int
    #   -> "please use a whole number" for ordering
    # - everything is fine and dandy
    #   -> add shift to database

    validate_ordering(ordering)
    validate_name(name)

    if get_shift_by_name(telegram_group_id, name) is not None:
        raise InvalidInput(
            "There is already a shift named {} in this group".format(name))

    validate_insert_one_result(db.records.insert_one({
        '_id': ObjectId(),
        'type': 'shift',
        'telegram_group_id': telegram_group_id,
        'ordering': ordering,
        'name': name}))

def delete_record(record_id: ObjectId) -> None:
    """Delete record."""
    validate_delete_result(db.records.delete_one({'_id': record_id}))

def edit_shift(shift_id: ObjectId, name: str, ordering: int) -> None:
    """Edit existing shift."""
    validate_name(name)
    validate_ordering(ordering)
    validate_update_result(db.records.update_one(
        {'_id': shift_id},
        {'$set': {'name': name, 'ordering': ordering}}))


def get_user(telegram_user_id: int) -> Cursor:
    """Fetch user by telegram user id."""
    return db.records.find_one({
        'type': 'user',
        'telegram_user_id':telegram_user_id})

def add_user_to_group(telegram_user_id: int, telegram_group_id: int) -> None:
    """Add user to schedule."""
    validate_update_result(db.record.update_one(
        {'type': 'user', 'telegram_user_id': telegram_user_id},
        {'$addToSet': {'groups': telegram_group_id}}))

def add_or_edit_user(telegram_user_id: int, user_name: str) -> None:
    """Create new user, or change name associated with telegram_user_id."""
    validate_name(user_name)
    validate_update_result(db.records.update_one(
        {'type': 'user', 'telegram_user_id': telegram_user_id},
        {'$set': {'name': user_name}},
        upsert=True))

def list_mutations(
        telegram_group_id: int,
        start_date: Optional[date]=None,
        end_date: Optional[date]=None) -> Cursor:
    """List all mutations in date range belonging to the telegram group."""
    query = {
        'telegram_group_id': telegram_group_id,
        'type': 'mutation'}
    if start_date is not None:
        query['date'] = {'$gre': start_date}
    if start_date is not None and end_date is not None:
        query['date']['$lte'] = end_date
    if end_date is not None:
        query['date'] = {'$lte': end_date}
    return db.records.find(query)

def add_mutation(
        telegram_group_id: int,
        owner_tuid: int,
        mutation_date: date,
        shift_id: ObjectId) -> None:
    """Add new mutation to database."""
    validate_insert_one_result(db.records.insert_one({
        '_id': ObjectId(),
        'type': 'mutation',
        'telegram_group_id': telegram_group_id,
        'owner_tuid': owner_tuid,
        'date': mutation_date,
        'shift_id': shift_id}))

def add_substitute_to_mutation(mutation_id: ObjectId, sub_tuid: int) -> None:
    """Fill open mutation."""
    validate_update_result(db.records.update_one(
        {'_id': mutation_id, 'type': 'mutation'},
        {'sub_tuid': sub_tuid}))
