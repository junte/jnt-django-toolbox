import typing as ty

from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.db import models, transaction
from django.urls import reverse

from jnt_django_toolbox.admin.helpers.urls import admin_url_provider
from jnt_django_toolbox.admin.views.base_admin_page import (
    AdminPageBreadcrumb,
    BaseAdminPageView,
)


class BaseModelAdminPageView(BaseAdminPageView):
    """Base admin view for object related pages."""

    model_admin: admin.ModelAdmin = None

    def get_model(self) -> models.Model:
        return self.model_admin.model

    def get_permission_required(self) -> ty.Iterable[str]:
        if self.permission_required:
            return super().get_permission_required()

        opts = self.get_model()._meta

        return (
            "{0}.{1}".format(
                opts.app_label,
                get_permission_codename("add", opts),
            ),
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def get_breadcrumbs(self) -> list[AdminPageBreadcrumb]:
        model = self.get_model()

        breadcrumbs = [
            AdminPageBreadcrumb(
                title=model._meta.app_label,
                href="{0}{1}/".format(
                    reverse(
                        "{0}:index".format(self.model_admin.admin_site.name),
                    ),
                    model._meta.app_label,
                ),
            ),
            AdminPageBreadcrumb(
                title=str(model._meta.verbose_name_plural)
                or model._meta.model_name,
                href=admin_url_provider.list_url(model),
            ),
        ]

        return [*breadcrumbs, *super().get_breadcrumbs()]
