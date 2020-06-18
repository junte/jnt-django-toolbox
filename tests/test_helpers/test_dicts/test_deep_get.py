# -*- coding: utf-8 -*-

import pytest

from jnt_django_toolbox.helpers import dicts


@pytest.fixture()
def dictionary():
    return {
        "field_1_1": {"field_2_1": 1, "field_2_2": {"field_3_1": 2}},
        "field_1_2": 3,
    }


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("field_1_2", 3),
        ("field_1_1.field_2_1", 1),
        ("field_1_1.field_2_2.field_3_1", 2),
    ],
)
def test_success(dictionary, path, expected):
    assert dicts.deep_get(dictionary, path) == expected


@pytest.mark.parametrize(
    "path",
    ["field_1_3", "field_1_1.field_2_3", "field_1_1.field_2_2.field_3_2"],
)
def test_fail(dictionary, path):
    with pytest.raises(KeyError):
        assert dicts.deep_get(dictionary, path)


@pytest.mark.parametrize(
    "path",
    ["field_1_3", "field_1_1.field_2_3", "field_1_1.field_2_2.field_3_2"],
)
def test_fail_but_default(dictionary, path):
    assert dicts.deep_get(dictionary, path, 5) == 5


@pytest.mark.parametrize(
    "path",
    ["field_1_3", "field_1_1.field_2_3", "field_1_1.field_2_2.field_3_2"],
)
def test_fail_but_default_none(dictionary, path):
    assert dicts.deep_get(dictionary, path, None) is None
