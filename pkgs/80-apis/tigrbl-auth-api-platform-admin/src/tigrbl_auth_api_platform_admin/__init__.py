"""Platform admin API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import PLATFORM_ADMIN_API_CONTRACT, PlatformAdminApiContract
from .identities import (
    AdminIdentityOut,
    AdminIdentityProvisionIn,
    AdminIdentityUpdateIn,
)

__all__ = [
    "AdminIdentityOut",
    "AdminIdentityProvisionIn",
    "AdminIdentityUpdateIn",
    "PRODUCT_SURFACE",
    "PLATFORM_ADMIN_API_CONTRACT",
    "PlatformAdminApiContract",
    "app",
    "build_app",
]
