"""Compatibility facade for ``tigrbl_identity_storage.tables.api_key``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.api_key import ApiKey

__all__ = ["ApiKey"]
