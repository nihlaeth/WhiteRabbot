"""API for interacting with database."""
from pymongo import MongoClient
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from .helpers import InvalidInput, validate_ordering, validate_shift_name


client = MongoClient()
db = client.white_rabbot


def get_shift_by_name(telegram_group_id: int, shift_name: str) -> Cursor:
    """Fetch shift by name."""
    validate_shift_name(shift_name)
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
    validate_shift_name(name)

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
    validate_shift_name(name)
    validate_ordering(ordering)
    # TODO: check on result
    db.records.update_one(
        {'_id': shift_id},
        {'$set': {'name': name, 'ordering': ordering}})


def get_user(session, telegram_user_id) -> Result:
    """Fetch user by telegram user id."""
    users = session.query(User).filter_by(
        telegram_user_id=telegram_user_id).all()
    if len(users) == 0:
        return Result(success=False, errors=[
            NoUserWithTelegramUserIdError(telegram_user_id)])
    elif len(users) == 1:
        return Result(value=users[0])
    else:
        return Result(success=False, errors=[
            MoreThan1UserWithTelegramUserIdError(telegram_user_id)])



def add_user_to_schedule(session, telegram_user_id, telegram_group_id) -> Result:
    """Add user to schedule."""
    user_result = get_user(session, telegram_user_id)
    schedule_result = get_schedule(session, telegram_group_id)
    if user_result.success and schedule_result.success:
        schedule_result.value.users.append(user_result.value)
        return Result(message="User added to schedule.")
    else:
        return Result(
            success=False,
            errors=user_result.errors + schedule_result.errors)
