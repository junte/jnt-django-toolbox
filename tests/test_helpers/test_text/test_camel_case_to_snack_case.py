# -*- coding: utf-8 -*-

import pytest

from jnt_django_toolbox.helpers.text import camel_case_to_snack_case


@pytest.mark.parametrize(
    ("source", "output"),
    [
        ("TestFunc", "test_func"),
        ("testFunc", "test_func"),
        ("test_Func", "test__func"),
        ("A", "a"),
        ("AbC", "ab_c"),
        ("abc", "abc"),
        ("ABCDE", "abcde"),
        ("SendByHTTPStatus", "send_by_http_status"),
        ("GoToHTTP", "go_to_http"),
        ("specialty3Name", "specialty3_name"),
        ("TestValue ", "test_value"),
    ],
)
def test_camel_case_to_snack_case(source, output):
    """Test camel_case_to_snack_case."""
    assert camel_case_to_snack_case(source) == output


def test_value_error():
    """Test invalid value for camel_case_to_snack_case."""
    with pytest.raises(ValueError, match="The text should not contain spaces"):
        camel_case_to_snack_case("Value error")
