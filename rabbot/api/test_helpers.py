from nose.tools import assert_equals

from . import helpers

# pylint: disable=protected-access
class Test_validate_ordering():

    def test_valid_data(self):
        result = helpers.validate_ordering(1)
        assert_equals(result.success, True)
        assert_equals(result.value, 1)

    def test_non_int(self):
        result = helpers.validate_ordering("not an int")
        assert_equals(result.success, False)


class Test_validate_shift_name():

    def test_valid_data(self):
        result = helpers.validate_shift_name("test")
        assert_equals(result.success, True)
        assert_equals(result.value, "test")

    def test_non_str(self):
        result = helpers.validate_shift_name(0)
        assert_equals(result.success, False)

    def test_empty_str(self):
        result = helpers.validate_shift_name("")
        assert_equals(result.success, False)
