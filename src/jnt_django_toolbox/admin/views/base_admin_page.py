import typing as ty
from dataclasses import dataclass

from django import forms
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView


class _EmptyForm(forms.Form):
    """Empty form."""


@dataclass
class AdminPageBreadcrumb:
    title: str
    href: str | None = None


class SubmitButton:
    def __init__(
        self,
        name: str,
        label: str,
        clazz: str = "default",
        style: str = "",
        confirm_text: str = "",
    ):
        self._name = name
        self._label = label
        self._class = clazz
        self._style = style
        self._confirm_text = confirm_text

    @property
    def html(self) -> str | None:
        onclick = (
            "return confirm('{0}')".format(self._confirm_text)
            if self._confirm_text
            else None
        )
        button_attrs = {
            "type": "submit",
            "class": self._class,
            "value": self._label,
            "name": self._name,
            "style": self._style,
            "onclick": onclick,
        }
        return mark_safe(  # noqa: S703, S308
            "<input {0}/>".format(
                " ".join(
                    (
                        '{0}="{1}"'.format(tag_attr, tag_value)
                        for tag_attr, tag_value in button_attrs.items()
                        if tag_value
                    ),
                ),
            ),
        )


class BaseAdminPageView(PermissionRequiredMixin, FormView):
    site_title = _("Django site admin")
    site_header = _("Django administration")
    site_url = "/"
    title = "Admin Page"
    help_text: str | None = None
    template_name = "jnt_django_toolbox/admin/admin_page.html"
    submit_label = ""  # obsolete
    success_url = "."
    message_safe = True
    form_class = _EmptyForm
    permission_required: str | ty.Iterable[str] | None = None
    submit_buttons: ty.Iterable[SubmitButton] = []

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"
        js = [
            "vendor/jquery/jquery{0}.js".format(extra),
            "jquery.init.js",
        ]
        return forms.Media(
            js=["admin/js/{0}".format(url) for url in js],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submit_buttons = list(self.submit_buttons)
        if self.submit_label:
            submit_buttons.append(
                SubmitButton(
                    name=self.submit_label,
                    label=self.submit_label,
                )
            )

        context.update(
            site_url=self.site_url,
            site_title=self.site_title,
            site_header=self.site_header,
            title=self.title,
            help_text=self.help_text,
            media=self.media + context["form"].media,
            message_safe=self.message_safe,
            request=self.request,
            user=self.request.user,
            has_permission=self.has_permission(),
            breadcrumbs=self.get_breadcrumbs(),
            has_file_field=context["form"].is_multipart(),
            submit_buttons=submit_buttons,
        )
        return context

    def has_permission(self) -> bool:
        """Return True if the given HttpRequest has permission to view page."""
        user = self.request.user
        if not user.is_authenticated:
            return False

        if not (user.is_active and user.is_staff):
            return False

        perms = self.get_permission_required()
        if perms:
            return self.request.user.has_perms(perms)

        return True

    def get_permission_required(self) -> ty.Iterable[str]:  # noqa: WPS615
        if not self.permission_required:
            return ()
        elif isinstance(self.permission_required, str):
            return (self.permission_required,)

        return self.permission_required

    def get_admin_permissions(self) -> list[str]:
        return []

    def get_breadcrumbs(self) -> list[AdminPageBreadcrumb]:
        return [
            AdminPageBreadcrumb(
                title=self.title,
            ),
        ]
