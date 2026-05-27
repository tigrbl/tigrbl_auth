"""Compatibility facade for ``tigrbl_identity_storage.tables.pushed_authorization_request``."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables.pushed_authorization_request import (
    DEFAULT_PAR_EXPIRY,
    PushedAuthorizationRequest,
)

__all__ = ["PushedAuthorizationRequest", "DEFAULT_PAR_EXPIRY"]
