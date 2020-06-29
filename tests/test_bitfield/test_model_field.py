# -*- coding: utf-8 -*-

import math

import pytest
from django.db import connection, models
from django.db.models import F
from django.db.models.fields import BigIntegerField

from jnt_django_toolbox.models.fields import BitField
from tests.models import BitFieldTestModel


def test_basic(db):
    """Create instance and make sure flags are working properly."""
    instance = BitFieldTestModel.objects.create(flags=1)
    assert instance.flags.FLAG1
    assert not instance.flags.FLAG2
    assert not instance.flags.FLAG3
    assert not instance.flags.FLAG4


def test_negative(db):
    """Creating new instances shouldn't allow negative values."""
    instance = BitFieldTestModel.objects.create(flags=-1)
    assert instance.flags._value == 15
    assert instance.flags.FLAG1
    assert instance.flags.FLAG2
    assert instance.flags.FLAG3
    assert instance.flags.FLAG4

    assert BitFieldTestModel.objects.filter(flags=15).count() == 1
    assert not BitFieldTestModel.objects.filter(flags__lt=0).exists()


def test_negative_in_raw_sql(db):
    """Creating new instances shouldn't allow negative values."""
    cursor = connection.cursor()
    flags_field = BitFieldTestModel._meta.get_field("flags")
    flags_db_column = flags_field.db_column or flags_field.name
    cursor.execute(
        "INSERT INTO {0} ({1}) VALUES (-1)".format(
            BitFieldTestModel._meta.db_table, flags_db_column,
        ),
    )
    # There should only be the one row we inserted through the cursor.
    instance = BitFieldTestModel.objects.get(flags=-1)
    assert instance.flags.FLAG1
    assert instance.flags.FLAG2
    assert instance.flags.FLAG3
    assert instance.flags.FLAG4
    instance.save()

    assert BitFieldTestModel.objects.filter(flags=15).count() == 1
    assert not BitFieldTestModel.objects.filter(flags__lt=0).exists()


def test_select(db):
    """Test filtering."""
    BitFieldTestModel.objects.create(flags=3)
    assert BitFieldTestModel.objects.filter(
        flags=BitFieldTestModel.flags.FLAG2,
    ).exists()
    assert BitFieldTestModel.objects.filter(
        flags=BitFieldTestModel.flags.FLAG1,
    ).exists()
    assert not BitFieldTestModel.objects.exclude(
        flags=BitFieldTestModel.flags.FLAG1,
    ).exists()
    assert not BitFieldTestModel.objects.exclude(
        flags=BitFieldTestModel.flags.FLAG2,
    ).exists()


def test_update(db):
    """Test update."""
    instance = BitFieldTestModel.objects.create(flags=0)
    assert not instance.flags.FLAG1

    BitFieldTestModel.objects.filter(pk=instance.pk).update(
        # flags=bitor(F("flags"), BitFieldTestModel.flags.FLAG2),
        flags=F("flags").bitor(BitFieldTestModel.flags.FLAG2),
    )
    instance = BitFieldTestModel.objects.get(pk=instance.pk)
    assert instance.flags.FLAG2

    BitFieldTestModel.objects.filter(pk=instance.pk).update(
        flags=F("flags").bitor(
            (~BitFieldTestModel.flags.FLAG1 | BitFieldTestModel.flags.FLAG4),
        ),
    )
    instance = BitFieldTestModel.objects.get(pk=instance.pk)
    assert not instance.flags.FLAG1
    assert instance.flags.FLAG2
    assert instance.flags.FLAG4
    assert not BitFieldTestModel.objects.filter(
        flags=BitFieldTestModel.flags.FLAG1,
    ).exists()

    BitFieldTestModel.objects.filter(pk=instance.pk).update(
        flags=F("flags").bitand(~BitFieldTestModel.flags.FLAG4),
    )
    instance = BitFieldTestModel.objects.get(pk=instance.pk)
    assert not instance.flags.FLAG1
    assert instance.flags.FLAG2
    assert not instance.flags.FLAG4


def test_update_with_handler(db):
    """Test update with handler."""
    instance = BitFieldTestModel.objects.create(flags=0)
    assert not instance.flags.FLAG1

    instance.flags.FLAG2 = True

    BitFieldTestModel.objects.filter(pk=instance.pk).update(
        flags=F("flags").bitor(instance.flags),
    )
    instance = BitFieldTestModel.objects.get(pk=instance.pk)
    assert instance.flags.FLAG2


def test_negate(db):
    """Test filter negate."""
    BitFieldTestModel.objects.create(
        flags=BitFieldTestModel.flags.FLAG1 | BitFieldTestModel.flags.FLAG2,
    )
    BitFieldTestModel.objects.create(flags=BitFieldTestModel.flags.FLAG2)
    assert (
        BitFieldTestModel.objects.filter(
            flags=~BitFieldTestModel.flags.FLAG1,
        ).count()
        == 1
    )
    assert not BitFieldTestModel.objects.filter(
        flags=~BitFieldTestModel.flags.FLAG2,
    ).exists()
    assert (
        BitFieldTestModel.objects.filter(
            flags=~BitFieldTestModel.flags.FLAG3,
        ).count()
        == 2
    )


def test_default_value(db):
    """Test default value."""
    instance = BitFieldTestModel.objects.create()
    assert instance.flags.FLAG1
    assert instance.flags.FLAG2
    assert not instance.flags.FLAG3
    assert not instance.flags.FLAG4


def test_binary_capacity(db):
    """Test capacity."""
    # Local maximum value, slow canonical algorithm
    MAX_COUNT = int(math.floor(math.log(BigIntegerField.MAX_BIGINT, 2)))

    # Big flags list
    flags = ["f{0}".format(i) for i in range(100)]

    BitField(flags=flags[:MAX_COUNT])

    with pytest.raises(ValueError, match="Too many flags"):
        BitField(flags=flags[: (MAX_COUNT + 1)])


def test_dictionary_init(db):
    """Test initialization with dict."""
    flags = {
        0: "zero",
        1: "first",
        10: "tenth",
        2: "second",
        "wrongkey": "wrongkey",
        100: "bigkey",
        -100: "smallkey",
    }

    bf = BitField(flags)

    assert bf.flags == [
        "zero",
        "first",
        "second",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "tenth",
    ]

    with pytest.raises(ValueError, match="Wrong keys or empty dictionary"):
        BitField(flags={})

    with pytest.raises(ValueError, match="Wrong keys or empty dictionary"):
        BitField(flags={"wrongkey": "wrongkey"})

    with pytest.raises(ValueError, match="Wrong keys or empty dictionary"):
        BitField(flags={"1": "non_int_key"})


class DefaultKeyNamesModel(models.Model):
    """Model for testing key names as a bitfield keys."""

    flags = BitField(
        flags=("FLAG1", "FLAG2", "FLAG3", "FLAG4"), default=("FLAG2", "FLAG3"),
    )


def test_defaults_as_key_names(db):
    """Test defaults as key names."""
    field = DefaultKeyNamesModel._meta.get_field("flags")
    assert (
        field.default
        == DefaultKeyNamesModel.flags.FLAG2 | DefaultKeyNamesModel.flags.FLAG3
    )
