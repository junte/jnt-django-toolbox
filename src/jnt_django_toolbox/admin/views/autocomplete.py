from django.contrib.admin.sites import site
from django.contrib.admin.views.autocomplete import (
    AutocompleteJsonView as BaseAutocompleteJsonView,
)
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


class AutocompleteFieldsError(Exception):
    """Autocomplete fields error."""


class AutocompleteJsonView(BaseAutocompleteJsonView):
    def get(self, request, *args, **kwargs):
        """Override from base."""
        (  # noqa: WPS414
            self.term,
            self.model_admin,
            self.source_field,
            to_field_name,
        ) = self.process_request(request)

        if not self.has_perm(request):
            raise PermissionDenied()

        self._check_inherit_model_admin()

        self.object_list = self.get_queryset()
        context = self.get_context_data()

        return JsonResponse(
            {
                "results": [
                    self.model_admin.autocomplete_item_data(instance)
                    for instance in context["object_list"]
                ],
                "pagination": {"more": context["page_obj"].has_next()},
            }
        )

    def get_queryset(self):
        """Additional filter for queryset in autocomplete."""
        queryset = super().get_queryset()

        return self.model_admin.autocomplete_queryset(self.request, queryset)

    def _check_inherit_model_admin(self) -> None:
        """Check inherit model_admin."""
        from jnt_django_toolbox.admin.mixins import (
            AutocompleteFieldsAdminMixin,
        )

        if not isinstance(self.model_admin, AutocompleteFieldsAdminMixin):
            raise AutocompleteFieldsError(
                "{0} is necessary to inherit the class from the AutocompleteAdminMixin".format(
                    self.model_admin,
                ),
            )


def autocomplete_view(request):
    return AutocompleteJsonView.as_view(admin_site=site)(request)
