# -*- coding: utf-8 -*-

import re
from datetime import date, datetime, timedelta
from typing import Union

import dateparser
from django.utils import timezone

from jnt_django_toolbox.consts.time import (
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
    SECONDS_PER_MONTH,
    SECONDS_PER_YEAR,
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


def period_to_seconds(value):
    """Convert period string to seconds."""
    # https://en.wikipedia.org/wiki/ISO_8601#Durations
    # P[n]Y[n]M[n]DT[n]H[n]M[n]S

    pattern_map = {
        "years": r"([\d]+)Y",
        "months": r"([\d]+)M",
        "days": r"([\d]+)D",
        "minutes": r"([\d]+)M",
        "hours": r"([\d]+)H",
        "seconds": r"([\d]+)S",
    }

    value = value.upper()

    if value[0] != "P":
        raise ValueError("Not an ISO 8601 Duration string")

    parts = value.split("T")

    period = parts[0]
    time_period = parts[1] if len(parts) > 1 else None

    total_seconds = 0

    total_seconds += (
        _get_number_from_period(pattern_map["years"], period)
        * SECONDS_PER_YEAR
    )
    total_seconds += (
        _get_number_from_period(pattern_map["months"], period)
        * SECONDS_PER_MONTH
    )
    total_seconds += (
        _get_number_from_period(pattern_map["days"], period) * SECONDS_PER_DAY
    )

    if time_period:
        total_seconds += (
            _get_number_from_period(pattern_map["minutes"], time_period)
            * SECONDS_PER_MINUTE
        )
        total_seconds += (
            _get_number_from_period(pattern_map["hours"], time_period)
            * SECONDS_PER_HOUR
        )
        total_seconds += _get_number_from_period(
            pattern_map["seconds"], time_period,
        )

    return total_seconds


def _get_number_from_period(pattern, source):
    matches = re.findall(pattern, source)
    return int(matches[0]) if matches else 0
