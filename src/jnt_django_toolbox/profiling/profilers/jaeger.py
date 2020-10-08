from contextlib import contextmanager

import jaeger_client
from django.db import connections
from opentracing import global_tracer

from jnt_django_toolbox.profiling.db.jaeger import unwrap_cursor, wrap_cursor
from jnt_django_toolbox.profiling.profilers.base import BaseProfiler


class JaegerProfiler(BaseProfiler):
    """
    Jaeger profiler.

    Spans could be dropped silently, if the size exceeds udp size limit:
    https://github.com/jaegertracing/jaeger-client-node/issues/124#issuecomment-324222456
    Mac users might need to run `sudo sysctl net.inet.udp.maxdgram=65536`
    """

    def __init__(self, service_name: str) -> None:
        """Initializing."""
        self._service_name = service_name
        self._init_tracer()

    def before_request(self, request, stack) -> None:
        """Start capturing requests."""
        stack.enter_context(global_tracer().start_active_span(request.path))
        stack.enter_context(trace_sql_queries())

    def after_request(self, request, response):
        """Add profiling info to response."""

    def _init_tracer(self) -> None:
        config = jaeger_client.Config(
            config={
                "sampler": {"type": "const", "param": 1},
                "logging": True,
                "max_tag_value_length": 8192,
            },
            service_name=self._service_name,
            validate=True,
        )

        config.initialize_tracer()


@contextmanager
def trace_sql_queries():
    """Enable tracing sql queries count."""
    for connection in connections.all():
        wrap_cursor(connection)
        yield
        unwrap_cursor(connection)
