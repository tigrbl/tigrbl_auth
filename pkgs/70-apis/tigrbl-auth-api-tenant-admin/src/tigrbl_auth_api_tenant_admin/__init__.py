"""Tenant admin API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import TENANT_ADMIN_API_CONTRACT, TenantAdminApiContract

__all__ = [
    "PRODUCT_SURFACE",
    "TENANT_ADMIN_API_CONTRACT",
    "TenantAdminApiContract",
    "app",
    "build_app",
]
