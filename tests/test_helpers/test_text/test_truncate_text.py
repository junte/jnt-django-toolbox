import pytest

from jnt_django_toolbox.helpers.text import truncate_text


@pytest.mark.parametrize(
    ("source", "output", "max_length"),
    [
        ("a", "a", 5),
        ("is", "is", 5),
        ("the", "the", 5),
        ("book", "book", 5),
        ("Lorem", "Lorem", 5),
        ("simply", "s...y", 5),
        ("popularised", "p...d", 5),
        ("the", "the", 4),
        ("book", "book", 4),
        ("Lorem", "L...", 4),
        ("simply", "s...", 4),
        ("popularised", "p...", 4),
        ("Lorem", "Lorem", 6),
        ("simply", "simply", 6),
        ("seventh", "se...h", 6),
        ("printing", "pr...g", 6),
        ("printing", "pr...ng", 7),
        ("popularised", "pop...ed", 8),
        ("popularised", "pop...sed", 9),
        ("popularised", "popu...sed", 10),
        ("popularised", "popularised", 11),
        ("popularised", "popularised", 12),
        ("internationalization", "intern...ion", 12),
        ("internationalization", "internat...ion", 14),
        ("", "", 10),
        ("simply", "", 0),
    ],
)
def test_truncate_text_with_max_length(source, output, max_length):
    """Test truncate text."""
    assert truncate_text(source, max_length) == output
