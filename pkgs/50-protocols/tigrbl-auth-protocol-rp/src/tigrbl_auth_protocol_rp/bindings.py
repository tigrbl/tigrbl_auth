"""RP wire operations mapped to reportable semantic capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "rp",
        CURRENT_VERSION.identifier,
        "rp-id-token-decode",
        "ID Token compact JWT",
        "artifact.processing",
        "decode",
        "oidc-id-token",
    ),
    ProtocolCapabilityRequirement(
        "rp",
        CURRENT_VERSION.identifier,
        "rp-id-token-validation",
        "ID Token claims and JOSE protection",
        "artifact.processing",
        "validate",
        "verified-oidc-id-token",
    ),
    ProtocolCapabilityRequirement(
        "rp",
        CURRENT_VERSION.identifier,
        "rp-callback-state-replay",
        "state",
        "security.replay-protection",
        "check_and_reserve",
        "oidc:authorization-response-state",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
