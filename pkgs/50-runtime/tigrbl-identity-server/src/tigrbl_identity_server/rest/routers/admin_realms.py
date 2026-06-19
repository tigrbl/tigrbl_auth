from __future__ import annotations

"""Compatibility bridge for Realm-owned admin realm routes."""

from warnings import warn

warn(
    "tigrbl_identity_server.rest.routers.admin_realms is deprecated; "
    "import tigrbl_identity_storage.tables.realm instead.",
    DeprecationWarning,
    stacklevel=2,
)

from tigrbl_identity_storage.tables.realm import (
    admin_api as api,
    admin_router as router,
    admin_create_realm,
    admin_create_realm_tenant,
    admin_delete_realm,
    admin_get_realm,
    admin_list_realm_tenants,
    admin_list_realms,
    admin_update_realm,
)

__all__ = [
    "api",
    "router",
    "admin_create_realm",
    "admin_create_realm_tenant",
    "admin_delete_realm",
    "admin_get_realm",
    "admin_list_realm_tenants",
    "admin_list_realms",
    "admin_update_realm",
]
