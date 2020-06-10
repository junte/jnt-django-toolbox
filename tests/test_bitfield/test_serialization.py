# -*- coding: utf-8 -*-

import pickle

from jnt_django_toolbox.models.fields.bit.types import BitHandler
from tests.models import BitFieldTestModel


def test_can_unserialize_bithandler():
    bf = BitFieldTestModel()
    bf.flags.FLAG_0 = 1
    bf.flags.FLAG_1 = 0
    data = pickle.dumps(bf)
    inst = pickle.loads(data)
    assert inst.flags.FLAG_0
    assert not inst.flags.FLAG_1


def test_pickle_integration(db):
    inst = BitFieldTestModel.objects.create(flags=1)
    data = pickle.dumps(inst)
    inst = pickle.loads(data)
    assert isinstance(inst.flags, BitHandler)
    assert int(inst.flags) == 1


def test_added_field():
    bf = BitFieldTestModel()
    bf.flags.FLAG_0 = 1
    bf.flags.FLAG_1 = 0
    bf.flags.FLAG_3 = 0
    data = pickle.dumps(bf)
    inst = pickle.loads(data)
    assert "FLAG_3" in inst.flags.keys()
