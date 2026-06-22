"""AdminGate surface for generated Tigrbl auth control-plane routes."""

from __future__ import annotations

from .gate import (
    ADMIN_API_KEY_ENV,
    ADMIN_API_KEY_HEADER,
    ADMIN_BEARER_SCHEME,
    ADMIN_HEADER_SCHEME,
    ADMIN_OPENAPI_SECURITY_DEPENDENCIES,
    ADMIN_SECURITY_REQUIREMENT,
    ADMIN_SECURITY_SCHEMES,
    AdminGate,
)

__all__ = [
    "ADMIN_API_KEY_ENV",
    "ADMIN_API_KEY_HEADER",
    "ADMIN_BEARER_SCHEME",
    "ADMIN_HEADER_SCHEME",
    "ADMIN_OPENAPI_SECURITY_DEPENDENCIES",
    "ADMIN_SECURITY_REQUIREMENT",
    "ADMIN_SECURITY_SCHEMES",
    "AdminGate",
]
