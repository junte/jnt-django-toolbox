from contextlib import suppress

from .db_queries import DatabaseQueriesProfiler
from .cache_calls import CacheCallsProfiler

with suppress(ImportError):
    from .jaeger import JaegerProfiler
