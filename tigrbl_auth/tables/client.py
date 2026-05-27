"""Compatibility facade for ``tigrbl_identity_storage.tables.client``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.client import Client, _CLIENT_ID_RE

__all__ = ["Client", "_CLIENT_ID_RE"]
