"""Compatibility facade for ``tigrbl_identity_storage.tables.auth_code``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.auth_code import AuthCode

__all__ = ["AuthCode"]
