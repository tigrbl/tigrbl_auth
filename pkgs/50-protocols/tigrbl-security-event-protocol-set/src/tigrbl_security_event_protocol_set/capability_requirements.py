from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "set", "RFC8417", "set-jti-replay", "jti",
        "security.replay-protection", "check_and_reserve", "set:event-jti",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
