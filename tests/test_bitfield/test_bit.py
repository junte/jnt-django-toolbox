from jnt_django_toolbox.models.fields.bit.types import Bit


def test_int():
    """Test cast."""
    bit = Bit(0)
    assert int(bit) == 1
    assert bool(bit)
    assert not (not bit)


def test_comparison():
    """Test comparison."""
    assert Bit(0) == Bit(0)
    assert Bit(1) != Bit(0)
    assert Bit(0, 0) != Bit(0, 1)
    assert Bit(0, 1) == Bit(0, 1)
    assert Bit(0) == 1


def test_and():
    """Test logical AND."""
    assert 1 & Bit(2) == 0
    assert 1 & Bit(0) == 1
    assert 1 & ~Bit(0) == 0
    assert Bit(0) & Bit(2) == 0
    assert Bit(0) & Bit(0) == 1
    assert Bit(0) & ~Bit(0) == 0


def test_or():
    """Test logical OR."""
    assert 1 | Bit(2) == 5
    assert 1 | Bit(5) == 33
    assert 1 | ~Bit(2) == -5
    assert Bit(0) | Bit(2) == 5
    assert Bit(0) | Bit(5) == 33
    assert Bit(0) | ~Bit(2) == -5


def test_xor():
    """Test logical XOR."""
    assert 1 ^ Bit(2) == 5
    assert 1 ^ Bit(0) == 0
    assert 1 ^ Bit(1) == 3
    assert 1 ^ Bit(5) == 33
    assert 1 ^ ~Bit(2) == -6
    assert Bit(0) ^ Bit(2) == 5
    assert Bit(0) ^ Bit(0) == 0
    assert Bit(0) ^ Bit(1) == 3
    assert Bit(0) ^ Bit(5) == 33
    assert Bit(0) ^ ~Bit(2) == -6
