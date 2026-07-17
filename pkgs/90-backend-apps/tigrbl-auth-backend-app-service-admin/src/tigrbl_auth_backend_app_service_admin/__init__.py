"""Service admin backend application package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import SERVICE_ADMIN_BACKEND_APP_CONTRACT, ServiceAdminBackendAppContract

__all__ = [
    "PRODUCT_SURFACE",
    "SERVICE_ADMIN_BACKEND_APP_CONTRACT",
    "ServiceAdminBackendAppContract",
    "app",
    "build_app",
]
