# -*- coding: utf-8 -*-

from django import forms

from tests.models import BitFieldTestModel


class BitFieldTestModelForm(forms.ModelForm):
    """Form for testing bitfield."""

    class Meta:
        model = BitFieldTestModel
        exclude = ()
