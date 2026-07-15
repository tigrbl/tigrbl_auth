"""OIDC wire operations mapped to reportable semantic capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "oidc",
        CURRENT_VERSION.identifier,
        "oidc-id-token-decode",
        "ID Token compact JWT",
        "artifact.processing",
        "decode",
        "oidc-id-token",
    ),
    ProtocolCapabilityRequirement(
        "oidc",
        CURRENT_VERSION.identifier,
        "oidc-id-token-validation",
        "ID Token claims and JOSE protection",
        "artifact.processing",
        "validate",
        "verified-oidc-id-token",
    ),
    ProtocolCapabilityRequirement(
        "oidc-backchannel-logout",
        "1.0",
        "logout-token-jti-replay",
        "jti",
        "security.replay-protection",
        "check_and_reserve",
        "oidc:logout-token-jti",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
