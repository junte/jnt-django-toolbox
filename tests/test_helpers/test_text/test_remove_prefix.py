import pytest

from jnt_django_toolbox.helpers.text import remove_prefix


@pytest.mark.parametrize(
    ("source", "prefix", "output"),
    [
        ("3-text", "3-", "text"),
        ("0", "1", "0"),
        ("", "", ""),
        ("Aabc", "a", "Aabc"),
        ("Bbcd", "Bbc", "d"),
        ("Test", "Test", ""),
        ("Tes", "Test", "Tes"),
        ("_-A", "_-", "A"),
    ],
)
def test_remove_prefix(source, prefix, output):
    """Test remove prefix."""
    assert remove_prefix(source, prefix) == output
