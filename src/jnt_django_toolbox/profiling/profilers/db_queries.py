# -*- coding: utf-8 -*-

from django.db import connection
from django.test.utils import CaptureQueriesContext

from jnt_django_toolbox.profiling.profilers.base import BaseProfiler


class DatabaseQueriesProfiler(BaseProfiler):
    """Database queries count profiler."""

    def __init__(self, header: str = "Db-Queries-Count"):
        """Initializing."""
        self._header = header

    def before_request(self, request, stack):
        """Start capturing requests."""
        self._context = CaptureQueriesContext(connection)
        stack.enter_context(self._context)

    def after_request(self, request, response):
        """Add profiling info to response."""
        response[self._header] = len(self._context)
