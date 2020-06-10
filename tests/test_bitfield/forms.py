from django import forms

from tests.models import BitFieldTestModel


class BitFieldTestModelForm(forms.ModelForm):
    class Meta:
        model = BitFieldTestModel
        exclude = tuple()
