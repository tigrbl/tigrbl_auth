"""Compatibility facade for canonical identity storage persistence helpers."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.persistence import *  # noqa: F403
from tigrbl_identity_storage.persistence import __all__ as _storage_all

__all__ = list(_storage_all)
