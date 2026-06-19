"""Compatibility bridge for the storage-owned token route."""

from __future__ import annotations

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.token is deprecated; "
    "import tigrbl_identity_storage.tables.token_record instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.token_record import api, router, token

__all__ = ["api", "router", "token"]
