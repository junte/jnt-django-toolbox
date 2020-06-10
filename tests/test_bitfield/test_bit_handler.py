import pytest
from jnt_django_toolbox.models.fields.bit_field.types import BitHandler


def test_comparison():
    bithandler_1 = BitHandler(0, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    bithandler_2 = BitHandler(1, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    bithandler_3 = BitHandler(0, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    assert bithandler_1 == bithandler_1
    assert bithandler_1 != bithandler_2
    assert bithandler_1 == bithandler_3


def test_defaults():
    bithandler = BitHandler(0, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))

    assert int(bithandler) == 0

    assert int(bithandler.FLAG_0.number) == 0
    assert int(bithandler.FLAG_1.number) == 1
    assert int(bithandler.FLAG_2.number) == 2
    assert int(bithandler.FLAG_3.number) == 3

    with pytest.raises(AttributeError):
        flag = bithandler.FLAG_4

    assert not bool(bithandler.FLAG_0)
    assert not bool(bithandler.FLAG_1)
    assert not bool(bithandler.FLAG_2)
    assert not bool(bithandler.FLAG_3)


def test_nonzero_default():
    bithandler = BitHandler(1, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    assert bool(bithandler.FLAG_0)
    assert not bool(bithandler.FLAG_1)
    assert not bool(bithandler.FLAG_2)
    assert not bool(bithandler.FLAG_3)

    bithandler = BitHandler(2, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    assert not bool(bithandler.FLAG_0)
    assert bool(bithandler.FLAG_1)
    assert not bool(bithandler.FLAG_2)
    assert not bool(bithandler.FLAG_3)

    bithandler = BitHandler(3, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    assert bool(bithandler.FLAG_0)
    assert bool(bithandler.FLAG_1)
    assert not bool(bithandler.FLAG_2)
    assert not bool(bithandler.FLAG_3)

    bithandler = BitHandler(4, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    assert not bool(bithandler.FLAG_0)
    assert not bool(bithandler.FLAG_1)
    assert bool(bithandler.FLAG_2)
    assert not bool(bithandler.FLAG_3)


def test_mutation():
    bithandler = BitHandler(0, ("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"))
    assert not bool(bithandler.FLAG_0)
    assert not bool(bithandler.FLAG_1)
    assert not bool(bithandler.FLAG_2)
    assert not bool(bithandler.FLAG_3)

    bithandler = BitHandler(bithandler | 1, bithandler._keys)
    assert bool(bithandler.FLAG_0)
    assert not bool(bithandler.FLAG_1)
    assert not bool(bithandler.FLAG_2)
    assert not bool(bithandler.FLAG_3)

    bithandler ^= 3
    assert int(bithandler) == 2

    assert not bool(bithandler & 1)

    bithandler.FLAG_0 = False
    assert not bithandler.FLAG_0

    bithandler.FLAG_1 = True
    assert not bithandler.FLAG_0
    assert bithandler.FLAG_1

    bithandler.FLAG_2 = False
    assert not bithandler.FLAG_0
    assert bithandler.FLAG_1
    assert not bithandler.FLAG_2
