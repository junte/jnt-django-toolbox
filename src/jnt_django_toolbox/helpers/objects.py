# -*- coding: utf-8 -*-

from functools import reduce


def getattr_nested(instance, attr):
    return reduce(getattr, [instance] + attr.split("__"))
