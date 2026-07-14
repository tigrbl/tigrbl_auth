"""Platform admin API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import PLATFORM_ADMIN_API_CONTRACT, PlatformAdminApiContract
from .identities import (
    AdminIdentityOut,
    AdminIdentityProvisionIn,
    AdminIdentityUpdateIn,
)
from .realms import AdminRealmOut, AdminRealmProvisionIn, AdminRealmUpdateIn
from .tenants import AdminTenantOut, AdminTenantProvisionIn, AdminTenantUpdateIn

__all__ = [
    "AdminIdentityOut",
    "AdminIdentityProvisionIn",
    "AdminIdentityUpdateIn",
    "AdminRealmOut",
    "AdminRealmProvisionIn",
    "AdminRealmUpdateIn",
    "AdminTenantOut",
    "AdminTenantProvisionIn",
    "AdminTenantUpdateIn",
    "PRODUCT_SURFACE",
    "PLATFORM_ADMIN_API_CONTRACT",
    "PlatformAdminApiContract",
    "app",
    "build_app",
]
