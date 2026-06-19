from __future__ import annotations

"""Compatibility bridge for User-owned admin identity routes."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.admin_identities is deprecated; "
    "import tigrbl_identity_storage.tables.user instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.user import (
    admin_api as api,
    admin_router as router,
    admin_create_identity,
    admin_delete_identity,
    admin_list_identities,
    admin_update_identity,
)

__all__ = [
    "api",
    "router",
    "admin_create_identity",
    "admin_delete_identity",
    "admin_list_identities",
    "admin_update_identity",
]
