"""API for interacting with database."""
from models import Schedule, Shift


class Result:
    """Represent a result that can be either a value or an error"""
    def __init__(self,
                 message: str,
                 success: bool=True,
                ):
        self.success = success
        self.message = message
        self.values = dict()
        self.errors = list()


def _validate_ordering(result, us_ordering) -> None:
    """Store ['ordering'] in values if valid, or append error message"""
    try:
        result.values['ordering'] = int(us_ordering)
    except ValueError:
        result.success = False
        result.errors.append(
            'Ordering should be an integer, and not {}'.format(us_ordering))


def _validate_shift_name(result, us_name) -> None:
    """Store ['shift_name'] in values if valid, or append error message"""
    if len(us_name) < 1:
        result.success = False
        result.errors.append('Shift name may not be empty')
        return
    try:
        result.values['shift_name'] = str(us_name)
    except ValueError:
        result.success = False
        result.errors.append(
            'Name should be a string, and not a {}'.format(type(us_name)))


def list_shifts(session, telegram_group_id):
    """List all shifts belonging to the telegram group."""
    schedule = session.query(Schedule).filter_by(
        telegram_group_id=telegram_group_id)[0]
    return schedule.shifts


def add_shift(session, telegram_group_id, us_name: str, us_ordering: int):
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

    result = Result(message="Shift successfully created")
    _validate_ordering(result, us_ordering)
    _validate_shift_name(result, us_name)
    # TODO: check in db that combination (shift_name, group) does not exist yet
    if result.success:
        schedule = session.query(Schedule).filter_by(
            telegram_group_id=telegram_group_id)[0]
        shift = Shift(
            schedule=schedule,
            name=result.values['shift_name'],
            ordering=result.values['ordering'])
        session.add(shift)
        session.flush()

    return result


# def add_shift():
#
#     ordering_result = validate_ordering(ordering)
#     name_result = validate_name(name)
#     if not all(ordering_result.success, name_result.success):
#         construct error result
#         Result(success=Falise, errors=...)
#     else:
#         Result(success=True, value=...)
#         success path


def delete_shift(session, shift_id):
    """Delete shift."""
    session.delete(session.query(Shift).filter_by(shift_id=shift_id)[0])
    session.flush()

def edit_shift(session, shift_id, name, ordering):
    """Edit existing shift."""
    shift = session.query(Shift).filter_by(shift_id=shift_id)[0]
    # TODO validate name and ordering
    shift.name = name
    shift.ordering = ordering

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
