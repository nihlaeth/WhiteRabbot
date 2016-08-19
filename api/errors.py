from enum import Enum

class ApiError(Enum):
    shift_ordering_is_not_an_int = "Ordering should be an integer and not {}"
    shift_name_is_not_a_string = "Shift name must be a string"
    shift_name_is_empty = "Shift name may not be empty"
    no_shift_with_id = "No shifts with id {}"
    more_than_1_shift_with_id = "More than 1 shift with id {}"
    no_shift_with_name = "No shifts with name {} in this group"
    more_than_1_shift_with_name = "More than 1 shift with name {} in group"
    already_shift_with_name = "There is already a shift with the name {} in this group"
    no_users_with_telegram_user_id = "No users with telegram user id {}"
    more_than_1_user_with_telegram_user_id = "More than 1 user with telegram user id {}"
    no_schedule_with_id = "No schedule with this group ID"
    more_than_1_schedule_with_id = "More than one schedule with ID {}"
    no_schedule_with_telegram_group_id = "No schedule with this telegram group ID"
    more_than_1_schedule_with_telegram_group_id = "More than one schedule with ID {}"
