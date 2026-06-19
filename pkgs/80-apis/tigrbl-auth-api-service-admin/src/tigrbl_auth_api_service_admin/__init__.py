"""Service admin API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import SERVICE_ADMIN_API_CONTRACT, ServiceAdminApiContract

__all__ = [
    "PRODUCT_SURFACE",
    "SERVICE_ADMIN_API_CONTRACT",
    "ServiceAdminApiContract",
    "app",
    "build_app",
]
