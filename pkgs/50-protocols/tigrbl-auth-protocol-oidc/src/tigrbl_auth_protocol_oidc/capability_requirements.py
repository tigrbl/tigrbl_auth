from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "oidc-backchannel-logout", "1.0", "logout-token-jti-replay", "jti",
        "security.replay-protection", "check_and_reserve", "oidc:logout-token-jti",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
