"""API for interacting with database."""
from models import Schedule, Shift


class Result:
    """Represent a result that can be either a value or an error"""
    def __init__(self,
                 message: str="",
                 success: bool=True,
                 value=None
                ):
        self.success = success
        self.message = message
        self.value = value
        self.errors = list()


def _validate_ordering(us_ordering) -> Result:
    """Store ['ordering'] in values if valid, or append error message"""
    result = Result()
    try:
        result.value = int(us_ordering)
    except ValueError:
        result.success = False
        result.errors.append(
            'Ordering should be an integer, and not {}'.format(us_ordering))
    return result


def _validate_shift_name(us_name) -> Result:
    """Store ['shift_name'] in values if valid, or append error message"""
    result = Result()
    if len(us_name) < 1:
        result.success = False
        result.errors.append('Shift name may not be empty')
        return result
    try:
        result.value = str(us_name)
    except ValueError:
        result.success = False
        result.errors.append(
            'Name should be a string, and not a {}'.format(type(us_name)))
    return result


def get_shift_by_id(session, shift_id: int) -> Result:
    """Fetch shift by id."""
    result = Result()
    query = session.query(Shift).filter_by(shift_id=shift_id)[0]
    if len(query) == 0:
        result.success = False
        result.errors.append("No shifts with id {}".format(shift_id))
    elif len(query) == 1:
        result.value = query[0]
    else:
        result.success = False
        result.errors.append("More than 1 shift with id {}".format(shift_id))
    return result

def list_shifts(session, telegram_group_id):
    """List all shifts belonging to the telegram group."""
    schedule = session.query(Schedule).filter_by(
        telegram_group_id=telegram_group_id)[0]
    return schedule.shifts


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
    # TODO: check in db that combination (shift_name, group) does not exist yet
    result = Result(message="Shift successfully created")
    result.success = all([ordering_result.success, shift_name_result.success])
    if result.success:
        schedule = session.query(Schedule).filter_by(
            telegram_group_id=telegram_group_id)[0]
        shift = Shift(
            schedule=schedule,
            name=shift_name_result.value,
            ordering=ordering_result.value)
        session.add(shift)
        session.flush()
        result.value = shift
    else:
        result.errors = ordering_result.errors + shift_name_result.errors
    return result


def delete_shift(session, shift_id):
    """Delete shift."""
    session.delete(session.query(Shift).filter_by(shift_id=shift_id)[0])
    session.flush()


def edit_shift(session, shift_id, us_name, us_ordering) -> Result:
    """Edit existing shift."""
    name_result = _validate_shift_name(us_name)
    ordering_result = _validate_ordering(us_ordering)
    shift_result = get_shift_by_id(session, shift_id)
    result = Result(message="Shift successfully edited")
    result.success = all([name_result.success, ordering_result.success, shift_result])
    if result.success:
        shift_result.value.name = us_name
        shift_result.value.ordering = us_ordering
        result.value = shift_result.value
    else:
        result.errors = name_result.errors + ordering_result.errors + shift_result.errors
    return result

def schedule_exists(session, telegram_group_id):
    """Check if a schedule exists for a given telegram group id."""
    num_schedules = session.query(Schedule).filter_by(
        telegram_group_id=telegram_group_id)
    if num_schedules == 0:
        return False
    elif num_schedules == 1:
        return True
    else:
        # TODO warn for corrupt data, more than 1 schedule per
        # telegram group
        pass
