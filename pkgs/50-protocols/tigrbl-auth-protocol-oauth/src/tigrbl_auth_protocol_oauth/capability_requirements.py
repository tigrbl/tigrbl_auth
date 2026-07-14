from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "oauth-token-revocation", "RFC7009", "token-revocation",
        "/revoke", "token.revocation", "revoke_token", "oauth:rfc7009",
    ),
    ProtocolCapabilityRequirement(
        "oauth-token-introspection", "RFC7662", "token-introspection",
        "/introspect", "token.introspection", "introspect_token",
        "oauth:rfc7662",
    ),
    ProtocolCapabilityRequirement(
        "oauth-dpop", "RFC9449", "dpop-jti-replay", "jti",
        "security.replay-protection", "check_and_reserve", "oauth:dpop-jti",
    ),
    ProtocolCapabilityRequirement(
        "oauth-dpop", "RFC9449", "dpop-nonce-replay", "nonce",
        "security.replay-protection", "check_and_reserve", "oauth:dpop-nonce",
    ),
)

__all__ = ["CAPABILITY_REQUIREMENTS"]
