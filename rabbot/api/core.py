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


def get_schedule_by_id(session, schedule_id) -> Result:
    """Fetch schedule by id."""
    result = Result()
    schedules = session.query(Schedule).filter_by(
        schedule_id=schedule_id).all()
    if len(schedules) == 0:
        result.success = False
        result.errors.append(NoScheduleWithIdError(schedule_id))
    elif len(schedules) == 1:
        result.value = schedules[0]
    else:
        result.success = False
        result.errors.append(MoreThan1ScheduleWithIdError(schedule_id))
    return result


def get_schedule(session, telegram_group_id) -> Result:
    """Fetch schedule by telegram group ID."""
    result = Result()
    schedules = session.query(Schedule).filter_by(
        telegram_group_id=telegram_group_id).all()
    if len(schedules) == 0:
        result.success = False
        result.errors.append(NoScheduleWithTelegramGroupIdError(telegram_group_id))
    elif len(schedules) == 1:
        result.value = schedules[0]
    else:
        result.success = False
        result.errors.append(
            MoreThan1ScheduleWithTelegramGroupIdError(telegram_group_id))
    return result


def add_schedule(session, telegram_group_id, telegram_admin_id) -> Result:
    """Create schedule."""
    admin_result = get_user(session, telegram_admin_id)
    if admin_result.success:
        schedule = Schedule(
            telegram_group_id=telegram_group_id,
            admin_id=admin_result.value.user_id)
        session.add(schedule)
        session.flush()
        return Result(value=schedule)
    return Result(success=False, errors=admin_result.errors)


def delete_schedule(session, schedule_id) -> Result:
    """Delete schedule."""
    schedule_result = get_schedule_by_id(session, schedule_id)
    result = Result(message="Schedule deleted")
    if schedule_result.success:
        session.delete(schedule_result.value)
        # TODO: delete shifts and mutations belonging to schedule
        session.flush()
    else:
        result.success = False
        result.errors = schedule_result.errors
    return result


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
