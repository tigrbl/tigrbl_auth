from __future__ import annotations

"""Compatibility bridge for RevokedToken-owned revocation route."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.revoke is deprecated; "
    "import tigrbl_identity_storage.tables.revoked_token instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.revoked_token import api, revoke, router

__all__ = ["api", "router", "revoke"]
