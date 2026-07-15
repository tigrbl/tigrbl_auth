"""OID4VP wire operations mapped to presentation capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-presentation-decode",
        "vp_token",
        "artifact.processing",
        "decode",
        "verifiable-presentation",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-presentation-validation",
        "vp_token",
        "artifact.processing",
        "validate",
        "verified-presentation-artifact",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-consent",
        "DCQL selection",
        "digital-credential.presentation",
        "check_consent",
        "presentation-consent",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-replay-reservation",
        "client_id and nonce",
        "digital-credential.presentation",
        "reserve_replay",
        "presentation-replay",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-verification",
        "vp_token",
        "digital-credential.presentation",
        "verify_presentation",
        "presentation-result",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-transaction-recording",
        "authorization response transaction",
        "digital-credential.presentation",
        "record_transaction",
        "presentation-transaction",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-result-recording",
        "presentation result",
        "digital-credential.presentation",
        "record_result",
        "presentation-result-record",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "oid4vp-presentation",
        "authorization response",
        "digital-credential.presentation",
        "present",
        "presentation-result",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "presentation-nonce-replay",
        "nonce",
        "security.replay-protection",
        "check_and_reserve",
        "oid4vp:presentation-nonce",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp",
        CURRENT_VERSION.identifier,
        "transaction-binding-replay",
        "transaction_id",
        "security.replay-protection",
        "check_and_reserve",
        "oid4vp:transaction",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
