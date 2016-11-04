# pylint: disable=protected-access,missing-docstring
from nose.tools import assert_raises

from rabbot.api.helpers import validate_ordering, validate_name, InvalidInput

class TestValidateOrdering():

    def test_valid_data(self):
        validate_ordering(1)

    def test_non_int(self):
        with assert_raises(InvalidInput):
            validate_ordering("not an int")


class TestValidateName():

    def test_valid_data(self):
        validate_name("test")

    def test_non_str(self):
        with assert_raises(InvalidInput):
            validate_name(0)

    def test_empty_str(self):
        with assert_raises(InvalidInput):
            validate_name("")
