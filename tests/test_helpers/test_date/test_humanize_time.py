import pytest

from jnt_django_toolbox.helpers.date import humanize_time


@pytest.mark.parametrize(
    ("seconds", "human_present"),
    [
        (0, "0s"),
        (12, "12s"),
        (60, "1m"),
        (121.1, "2m 1s"),
        (193, "3m 13s"),
        (1830.6, "30m 30s"),
        (3599, "59m 59s"),
        (3600, "1h"),
        (90000, "1d 1h"),
        (93705, "1d 2h 1m 45s"),
    ],
)
def test_humanize_time(seconds, human_present):
    """Test right work."""
    assert humanize_time(seconds) == human_present


@pytest.mark.parametrize(
    "seconds", ["", "any string", [], [12], {}, {"test": 4}, object],
)
def test_humanize_time_no_valid_data(seconds):
    """Test if not valid args."""
    with pytest.raises(ValueError, match="Seconds should be a number"):
        humanize_time(seconds)
