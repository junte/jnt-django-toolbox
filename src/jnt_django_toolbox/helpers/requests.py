from django.http import HttpRequest


def is_ajax(request: HttpRequest) -> bool:
    """Is request ajax request."""
    return any(
        [
            request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest",
            request.content_type == "application/json",
            request.META.get("HTTP_ACCEPT") == "application/json",
        ]
    )
