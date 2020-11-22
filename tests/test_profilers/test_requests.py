from contextlib import ExitStack

from django.http import HttpResponse

from jnt_django_toolbox.profiling.profilers import RequestsProfiler


def test_requests_provider(rf):
    """Testing cache calls are appended to the response."""
    request = rf.request()
    profiler = RequestsProfiler("app")
    with ExitStack() as stack:
        profiler.before_request(request, stack)
        response = HttpResponse(b"dummy")
        profiler.after_request(request, response)

    assert "app_time" in response
