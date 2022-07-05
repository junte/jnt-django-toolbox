from django.contrib import admin
from django.urls import NoReverseMatch, reverse


class _AdminUrlProvider:
    allowed_urls_types = (
        "add",
        "change",
        "delete",
        "changelist",
        "view",
        "autocomplete",
    )

    def for_view(
        self,
        url_type: str,
        model,
        model_admin: admin.ModelAdmin | None = None,
    ) -> str | None:
        if url_type not in self.allowed_urls_types:
            raise "Type not allowed, allowed: {0}".format(
                self.allowed_urls_types,
            )

        model_id = getattr(model, "id", None)
        view_name = self._make_view_name(url_type, model, model_admin)
        return self._reverse(
            view_name,
            args=[model_id]
            if model_id and url_type not in {"add", "changelist"}
            else None,
        )

    def add_url(self, model):
        return self.for_view("add", model)

    def change_url(
        self,
        model,
        model_admin: admin.ModelAdmin | None = None,
    ) -> str | None:
        return self.for_view("change", model, model_admin)

    def delete_url(
        self,
        model,
        model_admin: admin.ModelAdmin | None = None,
    ) -> str | None:
        return self.for_view("delete", model, model_admin)

    def view_url(
        self,
        model,
        model_admin: admin.ModelAdmin | None = None,
    ) -> str | None:
        return self.for_view("view", model, model_admin)

    def list_url(
        self,
        model,
        model_admin: admin.ModelAdmin | None = None,
    ) -> str | None:
        return self.for_view("changelist", model, model_admin)

    def autocomplete_url(
        self,
        model,
        model_admin: admin.ModelAdmin | None = None,
    ) -> str | None:
        return self.for_view("autocomplete", model, model_admin)

    def __call__(self, model):
        return {
            url_type: self.for_view(url_type, model)
            for url_type in self.allowed_urls_types
        }

    def _make_view_name(
        self,
        url_type: str,
        model,
        model_admin: admin.ModelAdmin | None = None,
    ) -> str:
        if model_admin:
            site = model_admin.admin_site
        else:
            site = admin.site

        return "{0}:{1}_{2}_{3}".format(
            site.name,
            model._meta.app_label,
            model._meta.model_name,
            url_type,
        )

    def _reverse(self, view_name: str, **kwargs) -> str | None:
        try:
            return reverse(view_name, **kwargs)
        except NoReverseMatch:
            return None


admin_url_provider = _AdminUrlProvider()
