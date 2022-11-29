from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from jnt_django_toolbox.admin.views.autocomplete import autocomplete_view

admin.site.enable_nav_sidebar = False
admin.site.autocomplete_view = autocomplete_view

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
