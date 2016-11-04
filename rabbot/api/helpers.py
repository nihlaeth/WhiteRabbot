class InvalidInput(Exception):

    """Unusable input."""

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
