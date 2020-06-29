# -*- coding: utf-8 -*-

import pytest

from tests.models import BitFieldTestModel
from tests.test_bitfield.forms import BitFieldTestModelForm


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"flags": ["FLAG1", "FLAG_FLAG"]},
        {"flags": ["FLAG_4"]},
        {"flags": [1, 2]},
    ],
)
def test_form_new_invalid(db, invalid_data):
    """Test creating via invalid form."""
    form = BitFieldTestModelForm(data=invalid_data)
    assert not form.is_valid()


@pytest.mark.parametrize(
    "data",
    [{"flags": ["FLAG1", "FLAG2"]}, {"flags": ["FLAG4"]}, {"flags": []}, {}],
)
def test_form_new(db, data):
    """Test create with valid form."""
    form = BitFieldTestModelForm(data=data)
    assert form.is_valid()

    instance = form.save()
    flags = data["flags"] if "flags" in data else []
    for k in BitFieldTestModel.flags:
        assert bool(getattr(instance.flags, k)) == (k in flags)


def test_form_update(db):
    """Test update with form."""
    instance = BitFieldTestModel.objects.create(flags=0)
    for k in BitFieldTestModel.flags:
        assert not bool(getattr(instance.flags, k))

    data = {"flags": ["FLAG1", "FLAG2"]}
    form = BitFieldTestModelForm(data=data, instance=instance)
    assert form.is_valid()
    instance = form.save()
    for k in BitFieldTestModel.flags:
        assert bool(getattr(instance.flags, k)) == (k in data["flags"])

    data = {"flags": ["FLAG3", "FLAG4"]}
    form = BitFieldTestModelForm(data=data, instance=instance)
    assert form.is_valid()
    instance = form.save()
    for k in BitFieldTestModel.flags:
        assert bool(getattr(instance.flags, k)) == (k in data["flags"])

    data = {"flags": []}
    form = BitFieldTestModelForm(data=data, instance=instance)
    assert form.is_valid()
    instance = form.save()
    for k in BitFieldTestModel.flags:
        assert not bool(getattr(instance.flags, k))
