# -*- coding: utf-8 -*-

from functools import wraps

from django.conf import settings
from opentracing import global_tracer

from jnt_django_toolbox.profiling.profilers import JaegerProfiler


def trace_span(func):
    """Wrap function for jaeger tracing."""

    @wraps(func)
    def handle(*args, **kwargs):  # noqa: WPS430
        is_tracing = any(
            isinstance(profiler, JaegerProfiler)
            for profiler in settings.REQUEST_PROFILERS
        )
        if not is_tracing:
            return func(*args, **kwargs)

        caller = args[0]
        caller_class = caller.__class__

        operation_name = "{0}.{1}".format(caller_class.__name__, func.__name__)

        with global_tracer().start_active_span(
            operation_name, child_of=global_tracer().active_span,
        ):
            return func(*args, **kwargs)

    return handle
