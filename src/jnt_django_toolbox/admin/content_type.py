import typing as ty
from http import HTTPStatus

from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.text import capfirst

from jnt_django_toolbox.admin.helpers.urls import admin_url_provider


class ContentTypeAutocompleteView(AutocompleteJsonView):
    # copied from base class
    def get(self, request, *args, **kwargs):
        if not self.model_admin.get_search_fields(request):
            msg_template = (
                "{0} must have search_fields for the autocomplete_view."
            )
            raise Http404(msg_template.format(type(self.model_admin).__name__))
        if not self.has_perm(request):
            return JsonResponse(
                {"error": "403 Forbidden"},
                status=HTTPStatus.FORBIDDEN,
            )

        self.term = request.GET.get("term", "")
        self.paginator_class = self.model_admin.paginator
        self.object_list = self.filter_queryset(self.get_queryset())
        context = self.get_context_data()

        return JsonResponse(
            {
                "results": [
                    {
                        "id": str(content_type.pk),
                        "text": capfirst(content_type.model),
                        # modify
                        "autocomplete_url": self.get_autocomplete_url(
                            content_type
                        ),
                        "data_app": content_type.app_label,
                        "data_model": content_type.model,
                        "data_change_url": self._get_change_url_template(
                            content_type
                        ),
                    }
                    for content_type in context["object_list"]
                ],
                "pagination": {"more": context["page_obj"].has_next()},
            }
        )

    def get_autocomplete_url(self, content_type):
        return admin_url_provider.autocomplete(content_type.model_class())

    def filter_queryset(self, queryset):
        return self._filter_queryset_by_ids(queryset)

    def _filter_queryset_by_ids(self, queryset):
        ids = self.request.GET.getlist("ids[]")
        if ids:
            queryset = queryset.filter(id__in=ids)
        return queryset

    def _get_change_url_template(self, content_type):
        list_url = reverse(
            "admin:{0}_{1}_changelist".format(
                content_type.app_label,
                content_type.model,
            ),
        )
        return "{0}{{id}}/change/".format(list_url)


def get_model_admin(model) -> ty.Optional[admin.ModelAdmin]:
    return site._registry.get(model)


class BaseContentTypeAdmin(admin.ModelAdmin):
    """Base content type admin."""

    search_fields = ("model",)

    def has_add_permission(self, request):
        """Check has add permissions."""
        return False

    def has_change_permission(self, request, obj=None):
        """Check has change permissions."""
        return False

    def has_view_or_change_permission(self, request, obj=None):
        """Check has view or change permissions."""
        return False

    def has_view_permission(self, request, obj=None):
        """Check has view permissions."""
        return True

    def get_model_perms(self, request):
        """Return a dict of all perms for this model."""
        return {}

    def autocomplete_view(self, request):
        """Content type autocomplete view."""
        return ContentTypeAutocompleteView.as_view(model_admin=self)(request)

    def autocomplete_queryset(self, request, queryset):
        queryset = super().autocomplete_queryset(request, queryset)

        ids = []
        for content_type in queryset:
            model_class = content_type.model_class()

            if get_model_admin(model_class):
                ids.append(content_type.pk)

        return queryset.filter(id__in=ids)

    def autocomplete_item_data(self, instance, request):
        item_data = super().autocomplete_item_data(instance, request)

        model = instance.model_class()

        related_obj = None

        for related_object in model._meta.related_objects:
            model_admin = get_model_admin(related_object.related_model)
            if model_admin:
                related_obj = related_object
                break

        if not related_obj:
            return item_data

        item_data.update(
            {
                "app_label": related_obj.related_model._meta.app_label,
                "model": related_obj.related_model._meta.model_name,
                "field_name": related_obj.remote_field.name,
                "field_placeholder": model._meta.verbose_name.title(),
            }
        )

        return item_data
