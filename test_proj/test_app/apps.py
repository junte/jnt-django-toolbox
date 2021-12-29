from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = "test_app"
    verbose_name = "Test application"
