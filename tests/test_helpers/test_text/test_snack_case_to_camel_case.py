import pytest

from jnt_django_toolbox.helpers.text import snack_case_to_camel_case


@pytest.mark.parametrize(
    ("source", "output"),
    [
        ("test_func", "testFunc"),
        ("test__func", "testFunc"),
        ("a", "a"),
        ("ab_c", "abC"),
        ("abc", "abc"),
        ("a_b_c_d_e", "aBCDE"),
        ("a_b_4_c", "aB4C"),
    ],
)
def test_snack_case_to_camel_case(source, output):
    """Test test_snack_case_to_camel_case."""
    assert snack_case_to_camel_case(source) == output


def test_value_error():
    """Test invalid value for snack_case_to_camel_case."""
    with pytest.raises(ValueError, match="The text should not contain spaces"):
        snack_case_to_camel_case("Value error")
