# -*- coding: utf-8 -*-

import pytest

from jnt_django_toolbox.helpers.objects import dict2obj, getattr_nested


@pytest.mark.parametrize(
    ("field", "expected"), [("field_1", "test"), ("field_2__inner_field", 3)],
)
def test_exists(field, expected):
    instance = dict2obj(
        {"field_1": "test", "field_2": dict2obj({"inner_field": 3})},
    )

    assert getattr_nested(instance, field) == expected


def test_not_exists():
    instance = dict2obj({})

    with pytest.raises(AttributeError):
        getattr_nested(instance, "field_1")


@pytest.mark.parametrize("default", ["value", None])
def test_not_exists_but_default(default):
    instance = dict2obj({})

    assert getattr_nested(instance, "field_1", default) == default
