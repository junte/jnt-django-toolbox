from django.contrib import admin
from test_app.models import Post

from jnt_django_toolbox.admin.mixins import AutocompleteFieldsAdminMixin


class AuthorPostInlineAdmin(AutocompleteFieldsAdminMixin, admin.StackedInline):
    model = Post
    extra = 0
