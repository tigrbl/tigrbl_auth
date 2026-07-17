"""Tenant admin backend application package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import TENANT_ADMIN_BACKEND_APP_CONTRACT, TenantAdminBackendAppContract

__all__ = [
    "PRODUCT_SURFACE",
    "TENANT_ADMIN_BACKEND_APP_CONTRACT",
    "TenantAdminBackendAppContract",
    "app",
    "build_app",
]
