# settings for django-admin-tools test project.

import os
import sys

import django

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_PATH))

DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {  # noqa: WPS407
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "testdb.sqlite",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

TIME_ZONE = "Europe/Moscow"

LANGUAGE_CODE = "en"

SITE_ID = 1

USE_I18N = False

USE_L10N = False

USE_TZ = False

MEDIA_ROOT = ""

MEDIA_URL = ""

STATIC_ROOT = os.path.join(PROJECT_PATH, "static")

STATIC_URL = "/static/"

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

SECRET_KEY = "toolbox"  # noqa: S105

ROOT_URLCONF = "urls"

WSGI_APPLICATION = "test_proj.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_USER_MODEL = "users.User"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"

version = django.get_version()


MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

TEMPLATES = [  # noqa: WPS407
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_PATH + "/templates",  # noqa: WPS336
        ],
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

INSTALLED_APPS = [  # noqa: WPS407
    "test_app",
    "users",
    "jnt_django_toolbox",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Uncomment the next line to enable the admin:
    "django.contrib.admin",
    # Uncomment the next line to enable admin documentation:
    "django.contrib.admindocs",
]
