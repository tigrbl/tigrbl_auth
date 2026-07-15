"""Pure OIDC Discovery 1.0 metadata ownership and projection."""

from __future__ import annotations

from typing import Final

from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import (
    ISSUER,
    JWKS_PATH,
)
from tigrbl_identity_core.standards import StandardOwner, describe_owner

from .discovery_metadata import OidcDiscoveryDeployment, build_openid_config


OIDC_DISCOVERY_SPEC_URL: Final[str] = (
    "https://openid.net/specs/openid-connect-discovery-1_0.html"
)
OWNER = StandardOwner(
    label="OIDC Discovery 1.0",
    title="OpenID Connect Discovery 1.0",
    runtime_status="profile-aware-discovery-metadata",
    public_surface=("/.well-known/openid-configuration",),
    notes=(
        "Versioned metadata semantics only; HTTP publication and durable "
        "tenant/realm existence checks are composed above the protocol layer."
    ),
)


_build_openid_config = build_openid_config


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        specification_version="1.0",
        jwks_publication=True,
        tenant_and_realm_profiles=True,
        spec_url=OIDC_DISCOVERY_SPEC_URL,
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
