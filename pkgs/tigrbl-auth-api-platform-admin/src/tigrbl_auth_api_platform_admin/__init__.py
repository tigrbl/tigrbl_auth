"""Platform admin API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import PLATFORM_ADMIN_API_CONTRACT, PlatformAdminApiContract

__all__ = [
    "PRODUCT_SURFACE",
    "PLATFORM_ADMIN_API_CONTRACT",
    "PlatformAdminApiContract",
    "app",
    "build_app",
]
