"""RFC 9635 wire operations mapped to reportable capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "gnap",
        CURRENT_VERSION.identifier,
        "grant-request",
        "grant endpoint POST",
        "grant.negotiation",
        "request_grant",
        "grant-negotiation-result",
    ),
    ProtocolCapabilityRequirement(
        "gnap",
        CURRENT_VERSION.identifier,
        "grant-continuation",
        "continuation endpoint POST/PATCH/DELETE",
        "grant.negotiation",
        "continue_grant",
        "grant-negotiation-result",
        False,
    ),
    ProtocolCapabilityRequirement(
        "gnap",
        CURRENT_VERSION.identifier,
        "access-token-rotation",
        "token management rotate",
        "grant.negotiation",
        "rotate_access_token",
        "rotated-access-token",
        False,
    ),
    ProtocolCapabilityRequirement(
        "gnap",
        CURRENT_VERSION.identifier,
        "client-key-proof",
        "GNAP request signature",
        "artifact.processing",
        "validate",
        "verified-gnap-key-proof",
    ),
    ProtocolCapabilityRequirement(
        "gnap",
        CURRENT_VERSION.identifier,
        "request-replay",
        "GNAP request digest and proof",
        "security.replay-protection",
        "check_and_reserve",
        "reserved-gnap-request",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
