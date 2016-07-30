"""API for interacting with database."""
from models import SessionScope, Schedule

def list_shifts(telegram_group_id):
    """List all shifts belonging to the telegram group."""
    with SessionScope() as session:
        schedule = session.query(Schedule).filter_by(
            telegram_group_id=telegram_group_id)[0]
        return schedule.shifts
