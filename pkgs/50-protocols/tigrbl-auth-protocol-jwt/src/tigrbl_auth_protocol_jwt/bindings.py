"""RFC 7519 structural operations mapped to semantic capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "jwt",
        CURRENT_VERSION.identifier,
        "jwt-compact-decode",
        "compact JWT",
        "artifact.processing",
        "decode",
        "jwt-claims",
    ),
    ProtocolCapabilityRequirement(
        "jwt",
        CURRENT_VERSION.identifier,
        "jwt-structural-validation",
        "registered JWT claims and JOSE structure",
        "artifact.processing",
        "validate",
        "structurally-valid-jwt",
    ),
    ProtocolCapabilityRequirement(
        "jwt",
        CURRENT_VERSION.identifier,
        "jwt-compact-encode",
        "application/jwt",
        "artifact.processing",
        "encode",
        "jwt",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
