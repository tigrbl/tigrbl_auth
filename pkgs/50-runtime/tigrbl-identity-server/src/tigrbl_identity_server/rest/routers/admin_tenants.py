from __future__ import annotations

"""Compatibility bridge for Tenant-owned admin tenant routes."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.admin_tenants is deprecated; "
    "import tigrbl_identity_storage.tables.tenant instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.tenant import (
    admin_api as api,
    admin_router as router,
    admin_create_tenant,
    admin_delete_tenant,
    admin_list_tenants,
    admin_update_tenant,
)

__all__ = [
    "api",
    "router",
    "admin_create_tenant",
    "admin_delete_tenant",
    "admin_list_tenants",
    "admin_update_tenant",
]
