from django.forms import TypedChoiceField


class EnumChoiceField(TypedChoiceField):
    """Form field for enum."""
