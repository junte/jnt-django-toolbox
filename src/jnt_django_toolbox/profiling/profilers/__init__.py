# -*- coding: utf-8 -*-

from contextlib import suppress

from .db_queries import DatabaseQueriesProfiler

with suppress(ImportError):
    from .jaeger import JaegerProfiler
