# -*- coding: utf-8 -*-

from tests.models import BitFieldTestModel
from tests.test_bitfield.forms import BitFieldTestModelForm


def test_form_new_invalid(db):
    invalid_data_dicts = [
        {"flags": ["FLAG_0", "FLAG_FLAG"]},
        {"flags": ["FLAG_4"]},
        {"flags": [1, 2]},
    ]
    for invalid_data in invalid_data_dicts:
        form = BitFieldTestModelForm(data=invalid_data)
        assert not form.is_valid()


def test_form_new(db):
    data_dicts = [
        {"flags": ["FLAG_0", "FLAG_1"]},
        {"flags": ["FLAG_3"]},
        {"flags": []},
        {},
    ]
    for data in data_dicts:
        form = BitFieldTestModelForm(data=data)
        assert form.is_valid()

        instance = form.save()
        flags = data["flags"] if "flags" in data else []
        for k in BitFieldTestModel.flags:
            assert bool(getattr(instance.flags, k)) == (k in flags)


def test_form_update(db):
    instance = BitFieldTestModel.objects.create(flags=0)
    for k in BitFieldTestModel.flags:
        assert not bool(getattr(instance.flags, k))

    data = {"flags": ["FLAG_0", "FLAG_1"]}
    form = BitFieldTestModelForm(data=data, instance=instance)
    assert form.is_valid()
    instance = form.save()
    for k in BitFieldTestModel.flags:
        assert bool(getattr(instance.flags, k)) == (k in data["flags"])

    data = {"flags": ["FLAG_2", "FLAG_3"]}
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
