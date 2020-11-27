from contextlib import ExitStack

from django.core.cache import cache
from django.http import HttpResponse

from jnt_django_toolbox.profiling.profilers import CacheCallsProfiler


def test_cache_calls_profiler(rf):
    """Testing cache calls are appended to the response."""
    request = rf.request()
    profiler = CacheCallsProfiler("app")
    with ExitStack() as stack:
        profiler.before_request(request, stack)
        cache.get("abc")
        cache.set_many({"one": 1, "two": 3})
        cache.delete("zoo")
        response = HttpResponse(b"dummy")
        profiler.after_request(request, response)

    assert "app_total_time" in response

    expected = (("delete", 1), ("get", 1), ("set", 2), ("set_many", 1))

    for name, value in expected:
        assert response["app_{0}_count".format(name)] == str(value)
