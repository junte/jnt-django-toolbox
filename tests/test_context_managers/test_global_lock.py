import time

import pytest
from django.core.cache import cache

from jnt_django_toolbox.context_managers import global_lock


@pytest.fixture(autouse=True)
def _setup_cache(settings):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "KEY_PREFIX": "test",
        },
    }

    yield

    cache.clear()


class _ExecuteContext:
    acquired = False


@pytest.fixture()
def context():
    """Execution context."""
    return _ExecuteContext()


def test_simple(context):
    """Test single execution."""

    def demo():  # noqa: WPS430
        with global_lock("test_lock") as acquired:
            context.acquired = acquired

    demo()
    assert context.acquired
    assert cache.get(global_lock.build_global_cache_key("test_lock")) is None


def test_many_executes(context):
    """Test many executes."""

    def demo():  # noqa: WPS430
        with global_lock("test_lock") as acquired:
            context.acquired = acquired

    demo()
    assert context.acquired
    assert cache.get(global_lock.build_global_cache_key("test_lock")) is None

    demo()
    assert context.acquired
    assert cache.get(global_lock.build_global_cache_key("test_lock")) is None


def test_with_exception(context):
    """Test exception."""

    def demo():  # noqa: WPS430
        with global_lock("test_lock") as acquired:
            if acquired:
                raise ValueError("test")

    with pytest.raises(ValueError, match="test"):
        demo()

    assert cache.get(global_lock.build_global_cache_key("test_lock")) is None


def test_already_runned(context):
    """Test if already runned."""

    def demo():  # noqa: WPS430
        with global_lock("test_lock") as acquired:
            context.acquired = acquired

    cache_key = global_lock.build_global_cache_key("test_lock")
    cache.add(cache_key, 1, global_lock.LOCK_EXPIRE)

    demo()
    assert not context.acquired
    assert cache.get(cache_key) == 1


def test_already_runned_expired(context):
    """Test expiration."""

    def demo():  # noqa: WPS430
        with global_lock("test_lock") as acquired:
            context.acquired = acquired

    cache.add(global_lock.build_global_cache_key("test_lock"), 1, 1)

    time.sleep(1)

    demo()

    assert context.acquired
    assert cache.get(global_lock.build_global_cache_key("test_lock")) is None
