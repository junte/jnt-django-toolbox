import re
from contextlib import ExitStack

from django.core.cache import cache
from django.http import HttpResponse

from jnt_django_toolbox.profiling.profilers import CacheCallsProfiler


def test_cache_calls_provider(rf):
    """Testing cache calls are appended to the response."""
    request = rf.request()
    profiler = CacheCallsProfiler("Foobar Cache")
    with ExitStack() as stack:
        profiler.before_request(request, stack)
        cache.get("abc")
        cache.set_many({"one": 1, "two": 3})
        cache.delete("zoo")
        response = HttpResponse(b"dummy")
        profiler.after_request(request, response)

    assert re.match(
        r"cache_duration=([.\d]+) cache_delete_count=1 cache_get_count=1 cache_set_count=2 cache_set_many_count=1",  # noqa: E501
        response["Foobar Cache"],
    )
