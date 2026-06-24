"""Pure deployment-resolution helpers for profiles, surfaces, slices, and boundaries.

This module intentionally avoids importing runtime-heavy dependencies so that
contracts, claims, evidence manifests, and governance tooling can resolve the
active deployment shape without initializing the full Tigrbl/SQLAlchemy stack.
"""

from __future__ import annotations

from typing import Any, Final

from .._surfaces.registries import all_surface_capability_registry as all_surface_capability_registry
from .._surfaces.registries import route_registry as _surface_route_registry

surface_route_registry = _surface_route_registry

# ---------------------------------------------------------------------------
# Pure defaults mirrored from ``config.settings`` for governance tooling.
# ---------------------------------------------------------------------------
DEFAULT_VALUES: Final[dict[str, Any]] = {
    "deployment_profile": "baseline",
    "issuer": "https://authn.example.com",
    "protected_resource_identifier": "https://authn.example.com/resource",
    "strict_boundary_enforcement": True,
    "surface_public_enabled": True,
    "surface_admin_enabled": False,
    "surface_operator_enabled": True,
    "surface_diagnostics_enabled": False,
    "surface_plugin_mode": "public-only",
    "runtime_style": "standalone",
    "active_surface_sets": "",
    "active_protocol_slices": "",
    "active_extensions": "",
    "jwt_secret": "insecure-dev-secret",
    "log_level": "INFO",
    "enable_id_token_encryption": False,
    "require_tls": True,
    "session_cookie_name": "sid",
    "session_cookie_path": "/",
    "session_cookie_domain": None,
    "session_cookie_samesite": "lax",
    "session_cookie_max_age_seconds": 3600,
    "session_cookie_renewal_seconds": 900,
    "session_cookie_cross_site": False,
    "session_cookie_force_secure": True,
    "enable_rfc6749": True,
    "enable_rfc6750": True,
    "enable_rfc6750_query": False,
    "enable_rfc6750_form": False,
    "enable_rfc7636": True,
    "enable_rfc8414": True,
    "enable_rfc8615": True,
    "enable_rfc7515": True,
    "enable_rfc7516": True,
    "enable_rfc7517": True,
    "enable_rfc7518": True,
    "enable_rfc7519": True,
    "enable_rfc7520": True,
    "enable_rfc7638": True,
    "enable_rfc8037": True,
    "enable_rfc8176": True,
    "enable_rfc8725": True,
    "enable_rfc7009": True,
    "enable_rfc7521": True,
    "enable_rfc7523": True,
    "enable_rfc7591": True,
    "enable_rfc7592": True,
    "enable_rfc7662": True,
    "enforce_rfc8252": True,
    "enable_rfc8252": True,
    "enable_rfc9068": False,
    "enable_rfc9207": True,
    "enable_rfc9728": True,
    "enable_oidc_core": True,
    "enable_oidc_discovery": True,
    "enable_oidc_userinfo": True,
    "enable_oidc_session_management": True,
    "enable_oidc_rp_initiated_logout": True,
    "enable_rfc8628": True,
    "enable_rfc8693": True,
    "enable_rfc8705": False,
    "enable_rfc8707": True,
    "enable_rfc9101": True,
    "enable_rfc9126": True,
    "enable_rfc9396": True,
    "enable_rfc9449": True,
    "enable_rfc9700": True,
    "enable_oidc_frontchannel_logout": True,
    "enable_oidc_backchannel_logout": True,
    "oauth21_alignment_mode": "tracked",
    "enable_rfc7800": False,
    "enable_rfc7952": False,
    "enable_rfc8291": False,
    "enable_rfc8812": False,
    "enable_rfc8932": False,
    "enable_rfc8523": False,
}

PROFILE_DEFAULT_OVERRIDES: Final[dict[str, dict[str, Any]]] = {
    "fapi2-security": {
        "enable_rfc8705": True,
        "enable_id_token_encryption": True,
        "require_tls": True,
        "strict_boundary_enforcement": True,
    },
}

SURFACE_SET_REGISTRY: Final[dict[str, dict[str, bool]]] = {
    "public-rest": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "admin-rest": {
        "surface_public_enabled": False,
        "surface_admin_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "diagnostics": {
        "surface_public_enabled": False,
        "surface_admin_enabled": False,
        "surface_diagnostics_enabled": True,
    },
    "public-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "platform-admin-api": {
        "surface_public_enabled": False,
        "surface_admin_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "tenant-admin-api": {
        "surface_public_enabled": False,
        "surface_admin_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "developer-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "service-admin-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "resource-validation-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "my-account-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_diagnostics_enabled": False,
    },
}

