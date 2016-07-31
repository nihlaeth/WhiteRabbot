"""API for interacting with database."""
from models import Schedule, Shift

def list_shifts(session, telegram_group_id):
    """List all shifts belonging to the telegram group."""
    schedule = session.query(Schedule).filter_by(
        telegram_group_id=telegram_group_id)[0]
    return schedule.shifts

def add_shift(session, telegram_group_id, name, ordering):
    """Create a new shift."""
    schedule = session.query(Schedule).filder_by(
        telegram_group_id=telegram_group_id)[0]
    # TODO validate name and ordering
    shift = Shift(schedule=schedule, name=name, ordering=ordering)
    session.add(shift)
    session.flush()

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
