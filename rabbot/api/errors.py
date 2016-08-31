from typing import Any


# This class does not inherit from Exception because these errors are
# not raised, but returned as part of Result's error list.
class APIError():

    @property
    def code(self):
        raise NotImplementedError

    @property
    def message_template(self):
        raise NotImplementedError

    def __str__(self):
        return self.code


class ShiftOrderingIsNotAnIntError(APIError):
    code = 'shift-ordering-is-not-an-int'
    message_template = "Ordering should be an integer and not {}"
    def __init__(self, ordering: Any) -> None:
        self.message = self.message_template.format(repr(ordering))


class ShiftNameIsNotAStringError(APIError):
    code = 'shift-name-is-not-a-string'
    message_template = "Shift name must be a string"
    def __init__(self) -> None:
        self.message = self.message_template


class ShiftNameIsEmptyError(APIError):
    code = 'shift-name-is-empty'
    message_template = "Shift name may not be empty"
    def __init__(self) -> None:
        self.message = self.message_template


class NoShiftWithIdError(APIError):
    code = 'no-shift-with-id'
    message_template = "No shifts with ID {}"
    def __init__(self, shift_id: int) -> None:
        self.message = self.message_template.format(id)


class MoreThan1ShiftWithIdError(APIError):
    code = 'more-than-1-shift-with-id'
    message_template = "More than 1 shift with ID {}"
    def __init__(self, shift_id: int) -> None:
        self.message = self.message_template.format(shift_id)


class NoShiftWithNameError(APIError):
    code = 'no-shift-with-name'
    message_template = "No shifts named {} in this group"
    def __init__(self, shift_name: str) -> None:
        self.message = self.message_template.format(repr(shift_name))


class MoreThan1ShiftWithNameError(APIError):
    code = 'more-than-1-shift-with-name'
    message_template = "More than 1 shift named {} in group"
    def __init__(self, shift_name: str) -> None:
        self.message = self.message_template.format(repr(shift_name))


class AlreadyShiftWithNameError(APIError):
    code = 'already-shift-with-name'
    message_template = "There is already a shift named {} in this group"
    def __init__(self, shift_name: str) -> None:
        self.message = self.message_template.format(repr(shift_name))


class NoUserWithTelegramUserIdError(APIError):
    code = 'no-users-with-telegram-user-id'
    message_template = "No users with telegram user ID {}"
    def __init__(self, telegram_user_id: int) -> None:
        self.message = self.message_template.format(telegram_user_id)


class MoreThan1UserWithTelegramUserIdError(APIError):
    code = 'more-than-1-user-with-telegram-user-id'
    message_template = "More than 1 user with telegram user ID {}"
    def __init__(self, telegram_user_id: int) -> None:
        self.message = self.message_template.format(telegram_user_id)


class NoScheduleWithIdError(APIError):
    code = 'no-schedule-with-id'
    message_template = "No schedule with ID {}"
    def __init__(self, schedule_id: int) -> None:
        self.message = self.message_template.format(schedule_id)


class MoreThan1ScheduleWithIdError(APIError):
    code = 'more-than-1-schedule-with-id'
    message_template = "More than one schedule with ID {}"
    def __init__(self, schedule_id: int) -> None:
        self.message = self.message_template.format(schedule_id)


class NoScheduleWithTelegramGroupIdError(APIError):
    code = 'no-schedule-with-telegram-group-id'
    message_template = "No schedule for Telegram group ID {}"
    def __init__(self, telegram_group_id: int) -> None:
        self.message = self.message_template.format(telegram_group_id)


class MoreThan1ScheduleWithTelegramGroupId(APIError):
    code = 'more-than-1-schedule-with-telegram-group-id'
    message_template = "More than one schedule for Telegram group ID {}"
    def __init__(self, telegram_group_id: int) -> None:
        self.message = self.message_template.format(telegram_group_id)
