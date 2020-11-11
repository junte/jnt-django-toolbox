from contextlib import suppress

from .cache_calls import CacheCallsProfiler
from .db_queries import DatabaseQueriesProfiler

with suppress(ImportError):
    from .jaeger import JaegerProfiler
