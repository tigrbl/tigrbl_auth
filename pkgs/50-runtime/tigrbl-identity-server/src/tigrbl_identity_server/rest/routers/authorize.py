"""Compatibility bridge for the storage-owned authorization route."""

from __future__ import annotations

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.authorize is deprecated; "
    "import tigrbl_identity_storage.tables.auth_code instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.auth_code import api, authorize, router

__all__ = ["api", "authorize", "router"]
