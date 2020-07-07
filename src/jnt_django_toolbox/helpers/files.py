# -*- coding: utf-8 -*-

import os


def file_ext(filename: str) -> str:
    """Getting file extension."""
    return os.path.splitext(filename)[-1].lower()
