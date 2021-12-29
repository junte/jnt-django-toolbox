from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from jnt_django_toolbox.admin.views.autocomplete import autocomplete_view

admin.site.enable_nav_sidebar = False
admin.site.autocomplete_view = autocomplete_view

admin.autodiscover()

urlpatterns = [
    url("^admin/", admin.site.urls),
    url(
        "^static/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}
    ),
]
