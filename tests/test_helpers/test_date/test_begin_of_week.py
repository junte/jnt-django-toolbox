import calendar
from datetime import datetime

import pytest

from jnt_django_toolbox.helpers.date import begin_of_week


@pytest.mark.parametrize(
    ("current_date", "expected_date"),
    [
        (datetime(2020, 1, 1), datetime(2019, 12, 30)),
        (datetime(2020, 1, 2), datetime(2019, 12, 30)),
        (datetime(2020, 1, 3), datetime(2019, 12, 30)),
        (datetime(2020, 1, 4), datetime(2019, 12, 30)),
        (datetime(2020, 1, 5), datetime(2019, 12, 30)),
        (datetime(2020, 1, 6), datetime(2020, 1, 6)),
        (datetime(2020, 1, 7), datetime(2020, 1, 6)),
        (datetime(2020, 1, 8), datetime(2020, 1, 6)),
    ],
)
def test_begin_week_monday(current_date, expected_date):
    """Test begin of week for monday."""
    assert begin_of_week(current_date, calendar.MONDAY) == expected_date


@pytest.mark.parametrize(
    ("current_date", "expected_date"),
    [
        (datetime(2020, 1, 1), datetime(2019, 12, 31)),
        (datetime(2020, 1, 2), datetime(2019, 12, 31)),
        (datetime(2020, 1, 3), datetime(2019, 12, 31)),
        (datetime(2020, 1, 4), datetime(2019, 12, 31)),
        (datetime(2020, 1, 5), datetime(2019, 12, 31)),
        (datetime(2020, 1, 6), datetime(2019, 12, 31)),
        (datetime(2020, 1, 7), datetime(2020, 1, 7)),
        (datetime(2020, 1, 8), datetime(2020, 1, 7)),
    ],
)
def test_begin_week_tuesday(current_date, expected_date):
    """Test begin of week for tuesday."""
    assert begin_of_week(current_date, calendar.TUESDAY) == expected_date


@pytest.mark.parametrize(
    ("current_date", "expected_date"),
    [
        (datetime(2020, 1, 1), datetime(2020, 1, 1)),
        (datetime(2020, 1, 2), datetime(2020, 1, 1)),
        (datetime(2020, 1, 3), datetime(2020, 1, 1)),
        (datetime(2020, 1, 4), datetime(2020, 1, 1)),
        (datetime(2020, 1, 5), datetime(2020, 1, 1)),
        (datetime(2020, 1, 6), datetime(2020, 1, 1)),
        (datetime(2020, 1, 7), datetime(2020, 1, 1)),
        (datetime(2020, 1, 8), datetime(2020, 1, 8)),
    ],
)
def test_begin_week_wednesday(current_date, expected_date):
    """Test begin of week for wednesday."""
    assert begin_of_week(current_date, calendar.WEDNESDAY) == expected_date


@pytest.mark.parametrize(
    ("current_date", "expected_date"),
    [
        (datetime(2020, 1, 1), datetime(2019, 12, 26)),
        (datetime(2020, 1, 2), datetime(2020, 1, 2)),
        (datetime(2020, 1, 3), datetime(2020, 1, 2)),
        (datetime(2020, 1, 4), datetime(2020, 1, 2)),
        (datetime(2020, 1, 5), datetime(2020, 1, 2)),
        (datetime(2020, 1, 6), datetime(2020, 1, 2)),
        (datetime(2020, 1, 7), datetime(2020, 1, 2)),
        (datetime(2020, 1, 8), datetime(2020, 1, 2)),
    ],
)
def test_begin_week_thursday(current_date, expected_date):
    """Test begin of week for thursday."""
    assert begin_of_week(current_date, calendar.THURSDAY) == expected_date


@pytest.mark.parametrize(
    ("current_date", "expected_date"),
    [
        (datetime(2020, 1, 1), datetime(2019, 12, 27)),
        (datetime(2020, 1, 2), datetime(2019, 12, 27)),
        (datetime(2020, 1, 3), datetime(2020, 1, 3)),
        (datetime(2020, 1, 4), datetime(2020, 1, 3)),
        (datetime(2020, 1, 5), datetime(2020, 1, 3)),
        (datetime(2020, 1, 6), datetime(2020, 1, 3)),
        (datetime(2020, 1, 7), datetime(2020, 1, 3)),
        (datetime(2020, 1, 8), datetime(2020, 1, 3)),
    ],
)
def test_begin_week_friday(current_date, expected_date):
    """Test begin of week for friday."""
    assert begin_of_week(current_date, calendar.FRIDAY) == expected_date


@pytest.mark.parametrize(
    ("current_date", "expected_date"),
    [
        (datetime(2020, 1, 1), datetime(2019, 12, 28)),
        (datetime(2020, 1, 2), datetime(2019, 12, 28)),
        (datetime(2020, 1, 3), datetime(2019, 12, 28)),
        (datetime(2020, 1, 4), datetime(2020, 1, 4)),
        (datetime(2020, 1, 5), datetime(2020, 1, 4)),
        (datetime(2020, 1, 6), datetime(2020, 1, 4)),
        (datetime(2020, 1, 7), datetime(2020, 1, 4)),
        (datetime(2020, 1, 8), datetime(2020, 1, 4)),
    ],
)
def test_begin_week_saturday(current_date, expected_date):
    """Test begin of week for saturday."""
    assert begin_of_week(current_date, calendar.SATURDAY) == expected_date


@pytest.mark.parametrize(
    ("current_date", "expected_date"),
    [
        (datetime(2020, 1, 1), datetime(2019, 12, 29)),
        (datetime(2020, 1, 2), datetime(2019, 12, 29)),
        (datetime(2020, 1, 3), datetime(2019, 12, 29)),
        (datetime(2020, 1, 4), datetime(2019, 12, 29)),
        (datetime(2020, 1, 5), datetime(2020, 1, 5)),
        (datetime(2020, 1, 6), datetime(2020, 1, 5)),
        (datetime(2020, 1, 7), datetime(2020, 1, 5)),
        (datetime(2020, 1, 8), datetime(2020, 1, 5)),
    ],
)
def test_begin_week_sunday(current_date, expected_date):
    """Test begin of week for sunday."""
    assert begin_of_week(current_date, calendar.SUNDAY) == expected_date
