from typing import Optional


class BitFieldReadOnlyWidget:
    """Readonly widget for bit field."""

    empty_value = "-"

    def __init__(self, formfield) -> None:
        """Initializing."""
        self._formfield = formfield

    def render(self, name, value) -> Optional[str]:
        """Render html-string."""
        checked_values = [
            choice for choice, checked in list(value.items()) if checked
        ]

        if not checked_values:
            return self.empty_value

        return ", ".join(
            (
                str(value._labels[value.keys().index(choice)])
                for choice in checked_values
            ),
        )
