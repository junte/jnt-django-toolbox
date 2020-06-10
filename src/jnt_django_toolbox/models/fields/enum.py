# -*- coding: utf-8 -*-

from django.db import models


class EnumField(models.TextField):
    """
    Wrapper around django choices.

    Allow better using of django 3 choices.
    """

    def __init__(self, enum, *args, **kwargs):
        """Initializer."""
        self.enum = enum
        kwargs["choices"] = enum.choices

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Deconstruct field for clone."""
        name, path, args, kwargs = super().deconstruct()
        kwargs["enum"] = self.enum

        return name, path, args, kwargs
