from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models

from jnt_django_toolbox.models.fields.widgets import FlagsArrayWidget


class FlagsArrayField(ArrayField):
    def __init__(self, choices, **kwargs):
        if "default" not in kwargs:
            kwargs["default"] = list

        super().__init__(models.TextField(choices=choices), **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": FlagsArrayWidget,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        return super(ArrayField, self).formfield(**defaults)  # noqa:WPS608

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.update(
            {
                "choices": self.base_field.choices,
            },
        )
        kwargs.pop("base_field")
        return name, path, args, kwargs
