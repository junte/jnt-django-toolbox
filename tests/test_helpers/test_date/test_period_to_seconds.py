# -*- coding: utf-8 -*-

import pytest

from jnt_django_toolbox.consts.time import (
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
    SECONDS_PER_MONTH,
    SECONDS_PER_YEAR,
)
from jnt_django_toolbox.helpers.date import period_to_seconds


@pytest.mark.parametrize(
    ("period", "seconds"),
    [
        ("PT2M", 2 * SECONDS_PER_MINUTE),
        ("P2Y3MT1S", 2 * SECONDS_PER_YEAR + 3 * SECONDS_PER_MONTH + 1),
        ("P1D", SECONDS_PER_DAY),
        ("PT3S", 3),
        ("PT4H3M45S", 4 * SECONDS_PER_HOUR + 3 * SECONDS_PER_MINUTE + 45),
        ("PT3H30M", 3 * SECONDS_PER_HOUR + 30 * SECONDS_PER_MINUTE),
        (
            "P1Y10M4DT2H35M12S",
            SECONDS_PER_YEAR
            + 10 * SECONDS_PER_MONTH
            + 4 * SECONDS_PER_DAY
            + 2 * SECONDS_PER_HOUR
            + 35 * SECONDS_PER_MINUTE
            + 12,
        ),
    ],
)
def test_period_to_seconds(period, seconds):
    """Test success."""
    assert period_to_seconds(period) == seconds


def test_not_valid_period_to_seconds():
    """Test invalid."""
    with pytest.raises(ValueError, match="Not an ISO 8601 Duration string"):
        period_to_seconds("T2M")
