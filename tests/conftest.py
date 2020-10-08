from django.conf import settings


def pytest_configure(config):
    """Build test app settings."""
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "jnt_django_toolbox",
            "tests",
        ],
        ROOT_URLCONF="",
        DEBUG=False,
    )
