# -*- coding: utf-8 -*-

from functools import reduce
from typing import Dict


def getattr_nested(instance, attr, *args):
    """Get object attribute."""
    try:
        return reduce(getattr, [instance] + attr.split("__"))
    except AttributeError:
        if not len(args):
            raise

        return args[0]


class ObjectView:
    """Object view."""

    def __init__(self, dictionary: Dict[str, object]):
        """Initialize self."""
        self.__dict__ = dictionary


def dict2obj(dictionary: Dict[str, object]) -> ObjectView:
    """Create ObjectView from dictionary."""
    return ObjectView(dictionary)
