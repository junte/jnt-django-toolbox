# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class BaseProfiler(ABC):
    """Base class for custom profilers."""

    @abstractmethod
    def before_request(self, request, stack):
        """Call on recieve request."""

    @abstractmethod
    def after_request(self, request, response):
        """Call after is processed and response available."""
