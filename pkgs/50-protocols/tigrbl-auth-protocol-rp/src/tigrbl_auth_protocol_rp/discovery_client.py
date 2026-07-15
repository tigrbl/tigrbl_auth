"""Relying-party access to pure OIDC discovery metadata semantics."""

from tigrbl_auth_protocol_oidc.standards.discovery import (
    ISSUER,
    JWKS_PATH,
    OIDC_DISCOVERY_SPEC_URL,
    OidcDiscoveryDeployment,
    build_openid_config,
)


__all__ = [
    "ISSUER",
    "JWKS_PATH",
    "OIDC_DISCOVERY_SPEC_URL",
    "OidcDiscoveryDeployment",
    "build_openid_config",
]
