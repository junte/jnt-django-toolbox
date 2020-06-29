# -*- coding: utf-8 -*-

from django.forms import IntegerField, ValidationError

from jnt_django_toolbox.admin.widgets.bit import BitFieldWidget
from jnt_django_toolbox.models.fields.bit.types import BitHandler


class BitFieldFormField(IntegerField):
    """Form field for bit field."""

    def __init__(self, choices=(), widget=BitFieldWidget, *args, **kwargs):
        """Initializing."""
        if isinstance(kwargs["initial"], int):
            iv = kwargs["initial"]
            iv_list = []
            for i in range(0, min(len(choices), 63)):
                if (1 << i) & iv > 0:
                    iv_list += [choices[i][0]]
            kwargs["initial"] = iv_list
        self.widget = widget
        super().__init__(widget=widget, *args, **kwargs)
        self.choices = choices
        self.widget.choices = choices

    def clean(self, value):
        """Validate value."""
        if not value:
            return 0

        # Assume an iterable which contains an item per flag that's enabled
        result = BitHandler(0, [key for key, value in self.choices])
        for k in value:
            try:
                setattr(result, str(k), True)
            except AttributeError:
                raise ValidationError("Unknown choice: {0}".format(k))
        return int(result)
