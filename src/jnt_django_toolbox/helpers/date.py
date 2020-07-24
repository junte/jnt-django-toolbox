# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from typing import Union

import dateparser
from django.utils import timezone

from jnt_django_toolbox.consts.time import (
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
)

Number = Union[int, float]


def date2datetime(value: date) -> datetime:  # noqa: WPS110
    """Converts date to datetime."""
    return datetime.combine(value, datetime.min.time())


def begin_of_week(value: date) -> date:  # noqa: WPS110
    """Get begin of week."""
    return value - timedelta(days=value.weekday() % 7)


def humanize_time(total_seconds: Number) -> str:
    """Provides human friendly representation for seconds."""
    if not isinstance(total_seconds, (int, float)):
        raise ValueError("Seconds should be a number")

    if total_seconds == 0:
        return "0s"

    items = []

    time_units = (
        ("d", SECONDS_PER_DAY),
        ("h", SECONDS_PER_HOUR),
        ("m", SECONDS_PER_MINUTE),
        ("s", 1),
    )

    for unit, sec_in_unit in time_units:
        val = total_seconds // sec_in_unit
        if not val:
            continue

        items.append("{0}{1}".format(int(val), unit))
        total_seconds -= sec_in_unit * val
        if not total_seconds:
            break

    return " ".join(items)


epoch = datetime.utcfromtimestamp(0)


def unix_time_seconds(dt):
    """Get unix time from datetime."""
    return (dt.replace(tzinfo=None) - epoch).total_seconds()


def parse_human_date(date_str: str):
    """Parse human presented date string."""
    return timezone.make_aware(dateparser.parse(date_str))
