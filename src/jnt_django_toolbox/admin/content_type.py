from django.contrib import admin

from jnt_django_toolbox.admin.views.content_type_autocomplete import (
    ContentTypeAutocompleteView,
)


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
