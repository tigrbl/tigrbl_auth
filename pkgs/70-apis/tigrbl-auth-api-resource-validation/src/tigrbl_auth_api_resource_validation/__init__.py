"""Resource validation API assembly package for Tigrbl Auth."""

from __future__ import annotations

from .app import PRODUCT_SURFACE, app, build_app
from .contract import RESOURCE_VALIDATION_API_CONTRACT, ResourceValidationApiContract

__all__ = [
    "PRODUCT_SURFACE",
    "RESOURCE_VALIDATION_API_CONTRACT",
    "ResourceValidationApiContract",
    "app",
    "build_app",
]
