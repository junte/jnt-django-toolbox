# -*- coding: utf-8 -*-

from jnt_django_toolbox.models.fields.bit_field.types import Bit


def test_int():
    bit = Bit(0)
    assert int(bit) == 1
    assert bool(bit)
    assert not (not bit)


def test_comparison():
    assert Bit(0) == Bit(0)
    assert Bit(1) != Bit(0)
    assert Bit(0, 0) != Bit(0, 1)
    assert Bit(0, 1) == Bit(0, 1)
    assert Bit(0) == 1


def test_and():
    assert 1 & Bit(2) == 0
    assert 1 & Bit(0) == 1
    assert 1 & ~Bit(0) == 0
    assert Bit(0) & Bit(2) == 0
    assert Bit(0) & Bit(0) == 1
    assert Bit(0) & ~Bit(0) == 0


def test_or():
    assert 1 | Bit(2) == 5
    assert 1 | Bit(5) == 33
    assert 1 | ~Bit(2) == -5
    assert Bit(0) | Bit(2) == 5
    assert Bit(0) | Bit(5) == 33
    assert Bit(0) | ~Bit(2) == -5


def test_xor():
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
