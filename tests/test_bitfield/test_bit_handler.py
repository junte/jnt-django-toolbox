import pytest

from jnt_django_toolbox.models.fields.bit.types import BitHandler


def test_comparison():
    """Test comparison."""
    bithandler1 = BitHandler(0, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    bithandler2 = BitHandler(1, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    bithandler3 = BitHandler(0, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    assert bithandler1 == bithandler1  # noqa: WPS312
    assert bithandler1 != bithandler2
    assert bithandler1 == bithandler3


def test_defaults():
    """Test defaults."""
    bithandler = BitHandler(0, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))

    assert int(bithandler) == 0

    assert int(bithandler.FLAG1.number) == 0
    assert int(bithandler.FLAG2.number) == 1
    assert int(bithandler.FLAG3.number) == 2
    assert int(bithandler.FLAG4.number) == 3

    with pytest.raises(AttributeError):
        flag = bithandler.FLAG_4  # noqa: F841

    assert not bool(bithandler.FLAG1)
    assert not bool(bithandler.FLAG2)
    assert not bool(bithandler.FLAG3)
    assert not bool(bithandler.FLAG4)


def test_nonzero_default():
    """Test non zero defaults."""
    bithandler = BitHandler(1, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    assert bool(bithandler.FLAG1)
    assert not bool(bithandler.FLAG2)
    assert not bool(bithandler.FLAG3)
    assert not bool(bithandler.FLAG4)

    bithandler = BitHandler(2, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    assert not bool(bithandler.FLAG1)
    assert bool(bithandler.FLAG2)
    assert not bool(bithandler.FLAG3)
    assert not bool(bithandler.FLAG4)

    bithandler = BitHandler(3, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    assert bool(bithandler.FLAG1)
    assert bool(bithandler.FLAG2)
    assert not bool(bithandler.FLAG3)
    assert not bool(bithandler.FLAG4)

    bithandler = BitHandler(4, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    assert not bool(bithandler.FLAG1)
    assert not bool(bithandler.FLAG2)
    assert bool(bithandler.FLAG3)
    assert not bool(bithandler.FLAG4)


def test_mutation():
    """Test mutation."""
    bithandler = BitHandler(0, ("FLAG1", "FLAG2", "FLAG3", "FLAG4"))
    assert not bool(bithandler.FLAG1)
    assert not bool(bithandler.FLAG2)
    assert not bool(bithandler.FLAG3)
    assert not bool(bithandler.FLAG4)

    bithandler = BitHandler(bithandler | 1, bithandler._keys)
    assert bool(bithandler.FLAG1)
    assert not bool(bithandler.FLAG2)
    assert not bool(bithandler.FLAG3)
    assert not bool(bithandler.FLAG4)

    bithandler ^= 3
    assert int(bithandler) == 2

    assert not bool(bithandler & 1)

    bithandler.FLAG1 = False
    assert not bithandler.FLAG1

    bithandler.FLAG2 = True
    assert not bithandler.FLAG1
    assert bithandler.FLAG2

    bithandler.FLAG3 = False
    assert not bithandler.FLAG1
    assert bithandler.FLAG2
    assert not bithandler.FLAG3
