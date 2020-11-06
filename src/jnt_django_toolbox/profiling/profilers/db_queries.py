from statistics import mean

from django.db import connection
from django.test.utils import CaptureQueriesContext

from jnt_django_toolbox.profiling.profilers.base import BaseProfiler


class DatabaseQueriesProfiler(BaseProfiler):
    """Database queries count profiler."""

    def __init__(self, header: str = "Db-Stats"):
        """Initializing."""
        self._header = header

    def before_request(self, request, stack):
        """Start capturing requests."""
        self._context = CaptureQueriesContext(connection)
        stack.enter_context(self._context)

    def after_request(self, request, response):
        """Add profiling info to response."""
        query_timings = [float(query["time"]) for query in self._context]
        stats = ["db_count={0}".format(len(self._context))]
        if query_timings:
            stats.extend(
                [
                    "db_total={0:.3f}".format(sum(query_timings)),
                    "db_max={0:.3f}".format(max(query_timings)),
                    "db_avg={0:.3f}".format(mean(query_timings)),
                ],
            )

        response[self._header] = " ".join(stats)
