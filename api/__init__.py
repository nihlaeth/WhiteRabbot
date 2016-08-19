"""API for interacting with database."""
from ..models import Schedule, Shift, User

from .errors import ApiError

class Result:
    """Represent a result that can be either a value or an error"""
    def __init__(self,
                 message: str="",
                 success: bool=True,
                 value=None,
                 errors: list=None
                ):
        self.success = success
        self.message = message
        self.value = value
        if errors is None:
            self.errors = list()
        else:
            self.errors = errors


def _validate_ordering(us_ordering) -> Result:
    """Return Result with validated ordering, or with errors"""
    if not isinstance(us_ordering, int):
        return Result(
            success=False,
            errors=[ApiError.shift_ordering_is_not_an_int
                    .value.format(us_ordering)])
    else:
        return Result(value=us_ordering)


def _validate_shift_name(us_name: str) -> Result:
    """Return Result with validated shift name, or with errors"""
    result = Result()
    if not isinstance(us_name, str):
        result.success = False
        result.errors.append('Shift name must be a string')
    elif len(us_name) < 1:
        result.success = False
        result.errors.append('Shift name may not be empty')
    else:
        result.value = us_name
    return result


def get_shift_by_id(session, shift_id: int) -> Result:
    """Fetch shift by id."""
    result = Result()
    query = session.query(Shift).filter_by(shift_id=shift_id).all()
    if len(query) == 0:
        result.success = False
        result.errors.append("No shifts with id {}".format(shift_id))
    elif len(query) == 1:
        result.value = query[0]
    else:
        result.success = False
        result.errors.append("More than 1 shift with id {}".format(shift_id))
    return result

def get_shift_by_name(session, telegram_group_id, us_shift_name: str) -> Result:
    """Fetch shift by name."""
    schedule_result = get_schedule(session, telegram_group_id)
    shift_name_result = _validate_shift_name(us_shift_name)
    if not all((shift_name_result.success, schedule_result.success)):
        return Result(
            success=False,
            errors=shift_name_result.errors + schedule_result.errors)
    shifts = session.query(Shift).\
        filter_by(name=shift_name_result.value).\
        filter_by(schedule_id=schedule_result.value.schedule_id).all()
    if len(shifts) == 0:
        return Result(
            success=False,
            errors=["No shifts with name {} in this group"
                    .format(shift_name_result.value)])
    elif len(shifts) == 1:
        return Result(
            success=True,
            value=shifts[0])
    else:
        # More than 1 result
        return Result(
            success=False,
            errors=["More than 1 shift with name {} in group"
                    .format(shift_name_result.value)])


def list_shifts(session, telegram_group_id) -> Result:
    """List all shifts belonging to the telegram group."""
    schedule_result = get_schedule(session, telegram_group_id)
    result = Result()
    if schedule_result.success:
        # pylint: disable=no-member
        # Result.value can have dynamic members
        result.value = schedule_result.value.shifts
    else:
        result.success = False
        result.errors = schedule_result.errors
    return result


def add_shift(session, telegram_group_id, us_name: str, us_ordering: int) -> Result:
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
    #   -> return added shift

    ordering_result = _validate_ordering(us_ordering)
    shift_name_result = _validate_shift_name(us_name)
    schedule_result = get_schedule(session, telegram_group_id)
    shift_exists_result = get_shift_by_name(session, telegram_group_id, us_name)
    result = Result(message="Shift successfully created")
    result.success = all([
        ordering_result.success,
        shift_name_result.success,
        schedule_result.success,
        not shift_exists_result.success])
    if result.success:
        shift = Shift(
            schedule=schedule_result.value,
            name=shift_name_result.value,
            ordering=ordering_result.value)
        session.add(shift)
        session.flush()
        result.value = shift
    else:
        result.errors = (
            ordering_result.errors + shift_name_result.errors + schedule_result.errors)
        if shift_exists_result.success:
            result.errors.append(
                "There is already a shift with the name {} in this group".format(
                    shift_name_result.value))
    return result


def delete_shift(session, shift_id) -> Result:
    """Delete shift."""
    shift_result = get_shift_by_id(session, shift_id)
    result = Result(message="Shift deleted")
    if shift_result.success:
        session.delete(shift_result.value)
        session.flush()
    else:
        result.success = False
        result.errors = shift_result.errors
    return result


def edit_shift(session, shift_id, us_name, us_ordering) -> Result:
    """Edit existing shift."""
    name_result = _validate_shift_name(us_name)
    ordering_result = _validate_ordering(us_ordering)
    shift_result = get_shift_by_id(session, shift_id)
    result = Result(message="Shift successfully edited")
    result.success = all([name_result.success, ordering_result.success, shift_result.success])
    if result.success:
        shift_result.value.name = us_name
        shift_result.value.ordering = us_ordering
        result.value = shift_result.value
    else:
        result.errors = name_result.errors + ordering_result.errors + shift_result.errors
    return result

def get_user(session, telegram_user_id) -> Result:
    """Fetch user by telegram user id."""
    users = session.query(User).filter_by(
        telegram_user_id=telegram_user_id).all()
    if len(users) == 0:
        return Result(success=False, errors=[
            "No users with telegram user id {}".format(telegram_user_id)])
    elif len(users) == 1:
        return Result(value=users[0])
    else:
        return Result(success=False, errors=[
            "More than 1 user with telegram user id {}".format(telegram_user_id)])

def get_schedule_by_id(session, schedule_id) -> Result:
    """Fetch schedule by id."""
    result = Result()
    schedules = session.query(Schedule).filter_by(
        schedule_id=schedule_id).all()
    if len(schedules) == 0:
        result.success = False
        result.errors.append("No schedule with this group ID")
    elif len(schedules) == 1:
        result.value = schedules[0]
    else:
        result.success = False
        result.errors.append("More than one schedule with ID {}".format(schedule_id))
    return result

def get_schedule(session, telegram_group_id) -> Result:
    """Fetch schedule by telegram group ID."""
    result = Result()
    schedules = session.query(Schedule).filter_by(
        telegram_group_id=telegram_group_id).all()
    if len(schedules) == 0:
        result.success = False
        result.errors.append("No schedule with this telegram group ID")
    elif len(schedules) == 1:
        result.value = schedules[0]
    else:
        result.success = False
        result.errors.append("More than one schedule with ID {}".format(telegram_group_id))
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
