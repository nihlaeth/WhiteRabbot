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


def validate_ordering(us_ordering) -> Result:
    """Return Result with validated ordering, or with errors"""
    if not isinstance(us_ordering, int):
        return Result(
            success=False,
            errors=['Ordering should be an integer, and not {}'
                    .format(us_ordering)])
    else:
        return Result(value=us_ordering)


def validate_shift_name(us_name: str) -> Result:
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

