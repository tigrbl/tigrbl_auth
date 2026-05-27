"""Compatibility facade for ``tigrbl_identity_storage.tables.client_registration``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.client_registration import ClientRegistration

__all__ = ["ClientRegistration"]
