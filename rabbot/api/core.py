"""API for interacting with database."""
from pymongo import MongoClient
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from .helpers import InvalidInput, validate_ordering, validate_name


client = MongoClient()
db = client.white_rabbot


def get_shift_by_name(telegram_group_id: int, shift_name: str) -> Cursor:
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

    if get_shift_by_name(telegram_group_id, name).count() > 0:
        raise InvalidInput(
            "There is already a shift named {} in this group".format(name))

    # TODO: check on result
    db.records.insert_one({
        '_id': ObjectId(),
        'type': 'shift',
        'telegram_group_id': telegram_group_id,
        'ordering': ordering,
        'name': name})

def delete_record(record_id: ObjectId) -> None:
    """Delete record."""
    # TODO: check on result
    db.records.delete_one({'_id': record_id})

def edit_shift(shift_id: ObjectId, name: str, ordering: int) -> None:
    """Edit existing shift."""
    validate_name(name)
    validate_ordering(ordering)
    # TODO: check on result
    db.records.update_one(
        {'_id': shift_id},
        {'$set': {'name': name, 'ordering': ordering}})


def get_user(telegram_user_id: int) -> Cursor:
    """Fetch user by telegram user id."""
    # TODO: check on result
    return db.records.find_one({
        'type': 'user',
        'telegram_user_id':telegram_user_id})

def add_user_to_group(telegram_user_id: int, telegram_group_id: int) -> None:
    """Add user to schedule."""
    # TODO: check on result
    db.record.update_one(
        {'type': 'user', 'telegram_user_id': telegram_user_id},
        {'$addToSet': {'groups': telegram_group_id}})

def add_or_edit_user(telegram_user_id: int, user_name: str) -> None:
    """Create new user, or change name associated with telegram_user_id."""
    validate_name(user_name)
    db.record.update_one(
        {'type': 'user', 'telegram_user_id': telegram_user_id},
        {'$set': {'name': user_name}},
        upsert=True)
