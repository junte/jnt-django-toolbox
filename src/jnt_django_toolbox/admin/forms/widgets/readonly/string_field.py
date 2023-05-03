from jnt_django_toolbox.admin.forms.widgets.readonly.base import (
    BaseReadOnlyWidget,
)


class StringReadonlyWidget(BaseReadOnlyWidget):
    def render(
        self,
        field_value,
        field_name,
        model_admin,
        **kwargs,
    ) -> str | None:
        db_field = kwargs.get("db_field")
        if getattr(db_field, "choices", None):
            choice = [
                present
                for choice_value, present in db_field.choices
                if choice_value == field_value
            ]

            if choice:
                return choice[0]

        return field_value
