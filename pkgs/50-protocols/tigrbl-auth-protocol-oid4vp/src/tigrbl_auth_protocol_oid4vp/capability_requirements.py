from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "oid4vp", "1.0", "presentation-nonce-replay", "nonce",
        "security.replay-protection", "check_and_reserve", "oid4vp:presentation-nonce",
    ),
    ProtocolCapabilityRequirement(
        "oid4vp", "1.0", "transaction-binding-replay", "transaction_id",
        "security.replay-protection", "check_and_reserve", "oid4vp:transaction",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
