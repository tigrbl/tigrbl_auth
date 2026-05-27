"""Compatibility facade for ``tigrbl_identity_storage.tables.user``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.user import User

__all__ = ["User"]
