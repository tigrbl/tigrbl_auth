"""Compatibility facade for canonical database engine wiring."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.db import ENGINE, dsn, get_db

__all__ = ["ENGINE", "dsn", "get_db"]
