# -*- coding: utf-8 -*-

import pytest

from jnt_django_toolbox.helpers.date import humanize_time


@pytest.mark.parametrize(
    ("seconds", "human_present"),
    [
        (0, "00:00"),
        (12, "00:12"),
        (60, "01:00"),
        (121.1, "02:02"),
        (193, "03:13"),
        (1830.6, "30:31"),
        (3599, "59:59"),
        (3600, "01:00:00"),
        (90000, "25:00:00"),
        (93705, "26:01:45"),
    ],
)
def test_humanize_time(seconds, human_present):
    assert humanize_time(seconds) == human_present


@pytest.mark.parametrize(
    "seconds", ["", "any string", [], [12], {}, {"test": 4}, object],
)
def test_humanize_time_no_valid_data(seconds):
    with pytest.raises(ValueError, match="Seconds should be a number"):
        humanize_time(seconds)
