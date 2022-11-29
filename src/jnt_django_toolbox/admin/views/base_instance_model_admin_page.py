import typing as ty

from django.contrib.auth import get_permission_codename
from django.db import models

from jnt_django_toolbox.admin.helpers.urls import admin_url_provider
from jnt_django_toolbox.admin.views import (
    AdminPageBreadcrumb,
    BaseModelAdminPageView,
)


class BaseInstanceModelAdminPageView(BaseModelAdminPageView):
    """Base admin view for object related pages."""

    instance: models.Model = None

    def get_permission_required(self) -> ty.Iterable[str]:
        if self.permission_required:
            return super().get_permission_required()

        opts = self.get_model()._meta

        return (
            "{0}.{1}".format(
                opts.app_label,
                get_permission_codename("change", opts),
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            instance=self.instance,
            subtitle=str(self.instance),
        )

        return context

    def get_breadcrumbs(self) -> list[AdminPageBreadcrumb]:
        breadcrumbs = list(super().get_breadcrumbs())
        breadcrumbs.insert(
            -1,
            AdminPageBreadcrumb(
                title=str(self.instance),
                href=admin_url_provider.change_url(
                    self.instance,
                    model_admin=self.model_admin,
                ),
            ),
        )

        return breadcrumbs
