"""Compatibility bridge for the storage-owned logout route."""

from __future__ import annotations

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.logout is deprecated; "
    "import tigrbl_identity_storage.tables.logout_state instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.logout_state import api, logout, router

__all__ = ["api", "logout", "router"]
