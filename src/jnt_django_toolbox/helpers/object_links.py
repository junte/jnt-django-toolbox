import contextlib
import typing as ty

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.urls import NoReverseMatch
from django.utils.html import format_html

from jnt_django_toolbox.admin.helpers.urls import admin_url_provider
from jnt_django_toolbox.helpers.objects import copy_func

EMPTY_VALUE = "-"


def add_object_link_present_function(model_admin, field_name):
    field = "_{0}_object_link".format(field_name)

    copied_func = copy_func(_get_display_related_field)
    copied_func.__defaults__ = (field_name,)

    setattr(model_admin, field, copied_func)
    getattr(model_admin, field).__dict__.update(
        {"short_description": _get_short_description(model_admin, field_name)},
    )
    return format_html(field)


def object_change_link(
    instance,
    empty_description="-",
    field_present=None,
    target: str = None,
) -> str:
    if not instance:
        return empty_description

    obj_present = str(
        getattr(instance, field_present) if field_present else instance
    )

    with contextlib.suppress(NoReverseMatch):
        url = admin_url_provider.change_url(instance)

    if url:
        return format_html(
            '<a href="{0}"{1}>{2}</a>',
            url,
            ' target="{0}"'.format(target) if target else "",
            obj_present,
        )

    return "{0} [id: {1}]".format(instance, instance.id)


def _parse_list_field_attr(attr) -> ty.Tuple[str, str]:
    unpack_attr = attr.split("__")
    return unpack_attr[0], unpack_attr[1] if len(unpack_attr) > 1 else None


def get_display_for_gfk(instance) -> str:
    if not instance:
        return ""

    return format_html(
        '<span class="gfk-object-type">{0}</span> {1}'.format(
            instance._meta.model_name,
            object_change_link(instance),
        ),
    )


def _get_display_related_field(instance, attr):
    attr, field_name = _parse_list_field_attr(attr)

    obj = getattr(instance, attr, None)

    if not obj:
        return format_html(EMPTY_VALUE)

    model_field = instance._meta.get_field(attr)

    if model_field.many_to_many or model_field.one_to_many:
        return get_display_for_many(obj.all(), field_name)
    elif isinstance(model_field, GenericForeignKey):
        return get_display_for_gfk(obj)

    return object_change_link(obj)


def get_display_for_many(instances, field_present=None) -> str:
    if not instances.exists():
        return EMPTY_VALUE

    return format_html(
        ", ".join(
            map(
                object_change_link,
                (
                    getattr(instance, field_present)
                    if field_present
                    else instance
                    for instance in instances
                ),
            ),
        ),
    )


def _get_short_description(model_admin, field_name) -> str:
    """Get verbose name for target field."""
    default_present = field_name.split("__")[-1].replace("_", " ")
    try:
        field = model_admin.model._meta.get_field(field_name)
    except FieldDoesNotExist:
        return default_present

    return getattr(field, "verbose_name", default_present)
