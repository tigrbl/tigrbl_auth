"""RFC 8417 wire/lifecycle operations mapped to semantic capabilities."""

from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

from .versions import CURRENT_VERSION

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-jwt-decode",
        "application/secevent+jwt",
        "artifact.processing",
        "decode",
        "set-claims",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-jwt-validation",
        "typ and SET claims",
        "artifact.processing",
        "validate",
        "verified-set",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-jwt-encode",
        "application/secevent+jwt",
        "artifact.processing",
        "encode",
        "set",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-transmission",
        "SET delivery",
        "security-events.delivery",
        "transmit",
        "security-event-delivery",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-receipt",
        "SET receipt",
        "security-events.delivery",
        "receive",
        "security-event",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-subscription-resolution",
        "event type URI",
        "security-events.delivery",
        "resolve_subscription",
        "security-event-subscription",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-event-recording",
        "jti and events",
        "security-events.delivery",
        "record_event",
        "security-event",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-delivery-recording",
        "delivery result",
        "security-events.delivery",
        "record_delivery",
        "security-event-delivery",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-delivery-replay-reservation",
        "verified issuer and jti",
        "security-events.delivery",
        "reserve_replay",
        "security-event-replay",
    ),
    ProtocolCapabilityRequirement(
        "set",
        CURRENT_VERSION.identifier,
        "set-jti-replay",
        "jti",
        "security.replay-protection",
        "check_and_reserve",
        "set:event-jti",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
