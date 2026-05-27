"""Compatibility facade for canonical identity storage ORM imports."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm.auth_session import AuthSession

__all__ = ["AuthSession"]
