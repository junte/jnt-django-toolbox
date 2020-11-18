import time

from jnt_django_toolbox.profiling.profilers.base import BaseProfiler


class RequestsProfiler(BaseProfiler):
    """Request profiler."""

    def __init__(self, header: str = "Request-Stats"):
        """Initializing."""
        self._header = header

    def before_request(self, request, stack):
        """Start capturing requests."""
        self._start_time = time.time()

    def after_request(self, request, response):
        """Add profiling info to response."""
        response[self._header] = "req_time={0:.3f}".format(
            time.time() - self._start_time,
        )
