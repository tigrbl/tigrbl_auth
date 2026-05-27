"""Compatibility facade for ``tigrbl_identity_storage.tables.logout_state``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.logout_state import LogoutState

__all__ = ["LogoutState"]
