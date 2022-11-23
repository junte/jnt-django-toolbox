from django.apps import apps
from django.contrib.contenttypes.fields import (
    GenericForeignKey as BaseGenericForeignKey,
)

from jnt_django_toolbox.admin.helpers.urls import admin_url_provider


class GenericForeignKey(BaseGenericForeignKey):
    def __init__(self, *args, **kwargs):
        self.related_models = kwargs.pop("related_models", None)
        super().__init__(*args, **kwargs)

    def get_related_models(self):  # noqa: WPS615
        if self.related_models is None:
            self.related_models = [
                model
                for model in apps.get_models()
                if self.has_autocomplete_url(model)
            ]
        elif callable(self.related_models):
            self.related_models = list(self.related_models())
        return [
            apps.get_model(*m.split(".")) if isinstance(m, str) else m
            for m in self.related_models
        ]

    def has_autocomplete_url(self, model):
        return bool(admin_url_provider.autocomplete_url(model))
