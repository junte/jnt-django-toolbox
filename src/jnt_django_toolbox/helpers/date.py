# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from math import ceil
from typing import Union

from jnt_django_toolbox.consts.time import SECONDS_PER_HOUR, SECONDS_PER_MINUTE

Number = Union[int, float]


def date2datetime(value: date) -> datetime:  # noqa: WPS110
    """Converts date to datetime."""
    return datetime.combine(value, datetime.min.time())


def begin_of_week(value: date) -> date:  # noqa: WPS110
    """Get begin of week."""
    return value - timedelta(days=value.weekday() % 7)


def humanize_time(total_seconds: Number) -> str:
    """Convert seconds to humanize_time."""
    if not isinstance(total_seconds, (int, float)):
        raise ValueError("Seconds should be a number")

    hours, seconds = divmod(ceil(total_seconds), SECONDS_PER_HOUR)
    minutes, seconds = divmod(seconds, SECONDS_PER_MINUTE)

    time_parts = [minutes, seconds]
    if hours:
        time_parts.insert(0, hours)

    return ":".join(("{0:02d}".format(part) for part in time_parts))
