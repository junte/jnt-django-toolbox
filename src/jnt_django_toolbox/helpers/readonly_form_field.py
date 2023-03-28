from django.contrib.admin.utils import lookup_field
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist


def get_present_admin_readonly_field(  # noqa: WPS212
    admin_readonly_field,
) -> str | None:
    """
    Get present for AdminReadonlyField.

    Improve the logic.
    """
    field_name, instance, model_admin = (
        admin_readonly_field.field["field"],
        admin_readonly_field.form.instance,
        admin_readonly_field.model_admin,
    )

    if not instance or admin_readonly_field.is_checkbox:
        return None

    if hasattr(model_admin, field_name):  # noqa: WPS421
        return None

    try:
        field, attr, field_value = lookup_field(
            field_name,
            instance,
            model_admin,
        )
        if field is None:
            field = instance._meta.get_field(field_name)
    except (AttributeError, ValueError, ObjectDoesNotExist, FieldDoesNotExist):
        # custom values can be present at "form.initial"
        field_name = admin_readonly_field.field["name"]
        field_value = admin_readonly_field.form.initial.get(field_name)
        field = None
        if all((not field_value, not isinstance(field_value, bool))):
            return None

    func_readonly_widget = getattr(model_admin, "readonly_widget", None)
    if not func_readonly_widget:
        return None

    readonly_widget = func_readonly_widget(admin_readonly_field.field["field"])

    if readonly_widget:
        return readonly_widget.render(field_value, field_name, db_field=field)

    return None
