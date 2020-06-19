# -*- coding: utf-8 -*-

import collections

not_provided = object()


def recursive_dict():
    """Default dict of default dicts with unlimited nesting."""
    return collections.defaultdict(recursive_dict)


def deep_get(dic, path, default=not_provided):
    """Get a nested dict value by dot-separated keys."""
    keys = path.split(".")

    try:  # noqa:WPS229
        for key in keys[:-1]:
            dic = dic[key]

        return dic[keys[-1]]
    except KeyError:
        if default == not_provided:
            raise

        return default


def deep_set(dic, path, value_to_set):
    """Set a nested dict value by dot-separated keys."""
    keys = path.split(".")

    for key in keys[:-1]:
        dic = dic[key]

    dic[keys[-1]] = value_to_set
