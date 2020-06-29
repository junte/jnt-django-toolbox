# -*- coding: utf-8 -*-

import pickle  # noqa: S403

from jnt_django_toolbox.models.fields.bit.types import BitHandler
from tests.models import BitFieldTestModel


def test_can_unserialize_bithandler():
    """Test success."""
    bf = BitFieldTestModel()
    bf.flags.FLAG1 = 1
    bf.flags.FLAG2 = 0
    data = pickle.dumps(bf)
    inst = pickle.loads(data)
    assert inst.flags.FLAG1
    assert not inst.flags.FLAG2


def test_pickle_integration(db):
    """Test pickle."""
    inst = BitFieldTestModel.objects.create(flags=1)
    data = pickle.dumps(inst)
    inst = pickle.loads(data)
    assert isinstance(inst.flags, BitHandler)
    assert int(inst.flags) == 1


def test_added_field():
    """Test add field."""
    bf = BitFieldTestModel()
    bf.flags.FLAG1 = 1
    bf.flags.FLAG2 = 0
    bf.flags.FLAG4 = 0
    data = pickle.dumps(bf)
    inst = pickle.loads(data)
    assert "FLAG4" in inst.flags.keys()
