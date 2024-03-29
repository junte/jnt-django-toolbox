from jnt_django_toolbox.admin.forms.widgets.readonly.base import (
    BaseReadOnlyWidget,
)
from jnt_django_toolbox.helpers.object_links import object_change_link


class ForeignKeyReadonlyWidget(BaseReadOnlyWidget):
    """Foreign key readonly widget."""

    def render(self, field_value, field_name, model_admin, **kwargs) -> str:
        """Render foreign key field."""
        if isinstance(field_value, str):
            return field_value

        return object_change_link(
            field_value,
            field_present=kwargs.get("field_present"),
            model_admin=model_admin,
        )
