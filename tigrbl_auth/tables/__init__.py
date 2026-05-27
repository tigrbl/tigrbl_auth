"""Compatibility facade for canonical identity storage tables.

The authoritative implementations live in ``tigrbl_identity_storage.tables``.
"""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables import *  # noqa: F403
from tigrbl_identity_storage.tables import __all__ as _storage_all

__all__ = list(_storage_all)
