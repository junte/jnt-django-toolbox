# -*- coding: utf-8 -*-

from django.db import connection
from django.test.utils import CaptureQueriesContext

from jnt_django_toolbox.profiling.profilers.base import BaseProfiler


class DatabaseQueriesProfiler(BaseProfiler):
    """Database queries count profiler."""

    def __init__(self, cookie: str = "Db-Queries-Count"):
        """Initializing."""
        self._cookie = cookie

    def before_request(self, request, stack):
        """Start capturing requests."""
        self._context = CaptureQueriesContext(connection)
        stack.enter_context(self._context)

    def after_request(self, request, response):
        """Add profiling info to response."""
        response[self._cookie] = len(self._context)
