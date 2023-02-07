import typing as ty

from django.conf import settings


def js_jquery() -> ty.Iterable[str]:
    extra = "" if settings.DEBUG else ".min"

    return [
        "admin/js/{0}".format(path)
        for path in (
            "vendor/jquery/jquery{0}.js".format(extra),
            "jquery.init.js",
        )
    ]
