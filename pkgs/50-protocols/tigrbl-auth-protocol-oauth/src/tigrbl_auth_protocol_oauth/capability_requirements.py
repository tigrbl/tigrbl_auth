from tigrbl_identity_contracts.capabilities import ProtocolCapabilityRequirement

CAPABILITY_REQUIREMENTS = (
    ProtocolCapabilityRequirement(
        "oauth-token-endpoint", "RFC6749", "issue-token-pair",
        "POST /token", "token.issuance", "issue_token_pair",
        "oauth:rfc6749",
    ),
    ProtocolCapabilityRequirement(
        "oauth-token-endpoint", "RFC6749", "rotate-refresh-token",
        "refresh_token grant", "token.issuance", "redeem_refresh_token",
        "oauth:rfc6749",
    ),
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
        "oauth-token-exchange", "RFC8693", "token-exchange",
        "POST /token/exchange", "token.exchange", "exchange_token",
        "oauth:rfc8693",
    ),
    ProtocolCapabilityRequirement(
        "oauth-pushed-authorization", "RFC9126", "pushed-authorization",
        "/par", "oauth.pushed-authorization", "push_authorization_request",
        "oauth:rfc9126",
    ),
    ProtocolCapabilityRequirement(
        "oauth-dynamic-client-registration", "RFC7591", "register-client",
        "POST /register", "client.registration", "register_client",
        "oauth:rfc7591",
    ),
    ProtocolCapabilityRequirement(
        "oauth-client-registration-management", "RFC7592", "read-registration",
        "GET /register/{client_id}", "client.registration", "get_registration",
        "oauth:rfc7592",
    ),
    ProtocolCapabilityRequirement(
        "oauth-client-registration-management", "RFC7592", "update-registration",
        "PUT /register/{client_id}", "client.registration", "update_registration",
        "oauth:rfc7592",
    ),
    ProtocolCapabilityRequirement(
        "oauth-client-registration-management", "RFC7592", "delete-registration",
        "DELETE /register/{client_id}", "client.registration", "disable_registration",
        "oauth:rfc7592",
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
