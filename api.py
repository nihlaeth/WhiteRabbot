"""API for interacting with database."""
from models import Schedule

def list_shifts(session, telegram_group_id):
    """List all shifts belonging to the telegram group."""
    schedule = session.query(Schedule).filter_by(
        telegram_group_id=telegram_group_id)[0]
    return schedule.shifts
