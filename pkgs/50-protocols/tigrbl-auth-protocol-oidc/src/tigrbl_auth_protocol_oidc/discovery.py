"""Compatibility exports for pure OIDC discovery metadata helpers."""

from tigrbl_auth_protocol_oidc.standards.discovery import (
    ISSUER,
    JWKS_PATH,
    OIDC_DISCOVERY_SPEC_URL,
    OidcDiscoveryDeployment,
    OWNER,
    _build_openid_config,
    build_openid_config,
    describe,
)

__all__ = [
    "ISSUER",
    "JWKS_PATH",
    "OIDC_DISCOVERY_SPEC_URL",
    "OidcDiscoveryDeployment",
    "OWNER",
    "_build_openid_config",
    "build_openid_config",
    "describe",
]
