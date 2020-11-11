import time
from collections import defaultdict
from contextlib import ExitStack

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse

from jnt_django_toolbox.profiling.profilers.base import BaseProfiler

_CACHE_METHODS = (
    "add",
    "get",
    "set",
    "delete",
    "clear",
    "has_key",
    "get_many",
    "set_many",
)


class _CaptureCacheCallsContext:
    def __init__(self, cache_provider):
        self._cache = cache_provider

    def __enter__(self):
        self.stats = defaultdict(list)
        self.original_methods = {}

        for method in _CACHE_METHODS:
            self.original_methods[method] = getattr(cache, method)
            setattr(
                cache, method, self._track_call(self.original_methods[method]),
            )

    def __exit__(self, exc_type, exc_value, traceback):
        for method in _CACHE_METHODS:
            setattr(cache, method, self.original_methods[method])

    def _track_call(self, actual_cache_call):
        def wrapper(*args, **kwargs):  # noqa:WPS430
            start = time.time()
            return_value = actual_cache_call(*args, **kwargs)
            duration = time.time() - start

            self.stats[actual_cache_call.__name__].append(duration)
            return return_value

        return wrapper


class CacheCallsProfiler(BaseProfiler):
    """Cache calls count profiler."""

    def __init__(self, header: str = "Cache-Stats"):
        """Initializing."""
        self._header = header

    def before_request(self, request: HttpRequest, stack: ExitStack):
        """Start capturing cache calls."""
        self._context = _CaptureCacheCallsContext(cache)
        stack.enter_context(self._context)

    def after_request(self, request: HttpRequest, response: HttpResponse):
        """Add profiling info to response."""
        stats = self._context.stats
        formatted = [
            "cache_duration={0:.3f}".format(
                sum(sum(duration) for duration in stats.values()),
            ),
            *(
                "cache_{0}_count={1}".format(name, len(durations))
                for name, durations in sorted(stats.items())
            ),
        ]
        response[self._header] = " ".join(formatted)
