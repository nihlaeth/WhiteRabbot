from pymongo.results import UpdateResult, InsertOneResult, DeleteResult

class InvalidInput(Exception):

    """Unusable input."""

class DBError(Exception):

    """Database error."""

class DataWarning(Exception):

    """Data does not meet expectations."""

def validate_ordering(ordering) -> None:
    """Raise InvalidInput if ordering is not valid."""
    if not isinstance(ordering, int):
        raise InvalidInput('Ordering should be an integer, and not {}')


def validate_name(name: str) -> None:
    """Raise InvalidInput if name is not valid."""
    if not isinstance(name, str):
        raise InvalidInput('Shift name must be a string')
    elif len(name) < 1:
        raise InvalidInput('Shift name may not be empty')

def validate_delete_result(result: DeleteResult, count: int=1) -> None:
    """Check everything went ok at the db side."""
    if not result.acknowledged:
        raise DBError("Unable to update record.")
    if result.deleted_count != count:
        raise DataWarning(
            "expected delete_count of {}, but got {}".format(
                count,
                result.deleted_count))

def validate_insert_one_result(result: InsertOneResult) -> None:
    """Check everything went ok at the db side."""
    if not result.acknowledged:
        raise DBError("Unable to update record.")

def validate_update_result(result: UpdateResult) -> None:
    """Check everything went ok at the db side."""
    if not result.acknowledged:
        raise DBError("Unable to update record.")
    if result.upserted_id is None and result.matched_count < 1:
        raise DataWarning("No matches found in database.")
