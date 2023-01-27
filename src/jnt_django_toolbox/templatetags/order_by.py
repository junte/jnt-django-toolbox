from django import template
from django.db import models

register = template.Library()


@register.filter_function
def order_by(queryset: models.QuerySet, args):
    """Ordering queryset."""
    return queryset.order_by(
        *[order_field.strip() for order_field in args.split(",")],
    )
