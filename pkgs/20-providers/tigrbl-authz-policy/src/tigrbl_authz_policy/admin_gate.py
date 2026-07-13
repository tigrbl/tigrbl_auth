"""Compatibility wrapper for the standalone AdminGate package."""

from __future__ import annotations

from tigrbl_authz_policy_admin_gate import (
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
