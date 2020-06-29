# -*- coding: utf-8 -*-

from jnt_django_toolbox.helpers.objects import dict2obj


def test_create():
    """Test if new object with fields are created."""
    instance = dict2obj({"field": "value"})

    assert hasattr(instance, "field")  # noqa: WPS421
    assert not hasattr(instance, "not_exists_field")  # noqa: WPS421
