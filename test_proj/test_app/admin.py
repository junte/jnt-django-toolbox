from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.contenttypes.models import ContentType
from test_app.filters import AuthorAutocompleteFilter, TagsAutocompleteFilter
from test_app.inlines import AuthorPostInlineAdmin
from test_app.models import Author, Blog, Comment, Post, PostCategory, Tag

from src.jnt_django_toolbox.admin.content_type import BaseContentTypeAdmin
from src.jnt_django_toolbox.admin.mixins import AutocompleteAdminMixin


class BaseAdmin(AutocompleteAdminMixin, admin.ModelAdmin):
    """Base admin."""


def get_model_admin(model) -> bool:
    return site._registry.get(model)


@admin.register(Author)
class AuthorAdmin(BaseAdmin):
    search_fields = ("user__email",)
    ordering = ("user__email",)

    inlines = (AuthorPostInlineAdmin,)


@admin.register(PostCategory)
class PostCategoryAdmin(BaseAdmin):
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Post)
class PostAdmin(BaseAdmin):
    search_fields = ("title",)
    list_display = ("title", "category")
    ordering = ("title",)
    list_filter = (AuthorAutocompleteFilter, TagsAutocompleteFilter)


@admin.register(Blog)
class BlogAdmin(BaseAdmin):
    search_fields = ("title",)
    list_display = ("title",)
    ordering = ("title",)


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    search_fields = ("content",)
    list_display = ("content",)
    ordering = ("content",)


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(ContentType)
class ContentTypeAdmin(BaseAdmin, BaseContentTypeAdmin):
    """Register content type admin."""
