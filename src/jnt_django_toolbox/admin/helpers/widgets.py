from django.contrib import admin
from django.urls import reverse


def render_autocomplete_badge(
    instance,
    present=None,
    admin_site: admin.AdminSite = None,
) -> str:
    admin_site = admin_site or admin.site

    return '<a href="{0}" target="_blank" title="{1}">{1}</a>'.format(
        reverse(
            "{0}:{1.app_label}_{1.model_name}_change".format(
                admin_site.name,
                instance._meta,
            ),
            args=(instance.id,),
        ),
        present or str(instance),
    )
