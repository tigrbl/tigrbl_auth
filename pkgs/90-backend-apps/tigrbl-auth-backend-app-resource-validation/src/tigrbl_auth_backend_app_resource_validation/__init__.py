"""Resource validation backend application package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import (
    RESOURCE_VALIDATION_BACKEND_APP_CONTRACT,
    ResourceValidationBackendAppContract,
)

__all__ = [
    "PRODUCT_SURFACE",
    "RESOURCE_VALIDATION_BACKEND_APP_CONTRACT",
    "ResourceValidationBackendAppContract",
    "app",
    "build_app",
]
