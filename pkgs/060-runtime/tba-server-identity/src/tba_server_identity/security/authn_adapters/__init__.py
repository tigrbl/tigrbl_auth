"""Tigrbl request authentication adapters."""

from .local import LocalAuthNAdapter
from .remote import RemoteAuthNAdapter

__all__ = ["LocalAuthNAdapter", "RemoteAuthNAdapter"]
