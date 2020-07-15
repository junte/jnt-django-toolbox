# -*- coding: utf-8 -*-

import re


def truncate_text(text: str, max_length: int = 50) -> str:
    """Trancate long text."""
    if not text:
        return ""

    s = text[:max_length]
    if len(s) > max_length:
        i = max(0, (max_length - 3) // 2)
        j = max(0, max_length - 3 - i)
        s = text[:i] + text[len(text) - j :]
        s = "{0}...{1}".format(s[:i], s[len(s) - j :])
    return s


def camel_case_to_snack_case(text):
    """Convert CamelCase -> snake_case."""
    return re.sub(r"(?!^)([A-Z]+)", r"_\1", text).lower()


def snack_case_to_camel_case(text):
    """Convert snake_case -> CamelCase."""
    first, *words = text.split("_")
    return "{0}{1}".format(first, "".join(map(lambda x: x.title(), words)))
