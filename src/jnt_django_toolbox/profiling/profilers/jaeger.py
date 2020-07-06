# -*- coding: utf-8 -*-

import jaeger_client
from opentracing import global_tracer

from jnt_django_toolbox.profiling.profilers.base import BaseProfiler


class JaegerProfiler(BaseProfiler):
    """
    Jaeger profiler.

    Spans could be dropped silently, if the size exceeds udp size limit:
    https://github.com/jaegertracing/jaeger-client-node/issues/124#issuecomment-324222456
    Mac users might need to run `sudo sysctl net.inet.udp.maxdgram=65536`
    """

    def __init__(self):
        """Initializing."""
        self._init_tracer()

    def before_request(self, request, stack):
        """Start capturing requests."""
        global_tracer().start_active_span(request.path)

    def after_request(self, request, response):
        """Add profiling info to response."""

    def _init_tracer(self):
        config = jaeger_client.Config(
            config={
                "sampler": {"type": "const", "param": 1},
                "logging": True,
                "max_tag_value_length": 8192,
            },
            service_name="Backend",
            validate=True,
        )

        config.initialize_tracer()
