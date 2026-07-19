"""RFC 8693 token-exchange specification owner and compatibility exports."""

from __future__ import annotations

from tigrbl_identity_core.standards import StandardOwner, describe_owner

from tigrbl_auth_protocol_oauth.standards._rfc8693 import (
    RFC8693_SPEC_URL,
    TOKEN_EXCHANGE_GRANT_TYPE,
    TokenExchangeRequest,
    TokenExchangeResponse,
    TokenType,
    exchange_token,
    makeDelegationToken,
    makeImpersonationToken,
    validate_subject_token,
    validate_token_exchange_request,
)


OWNER = StandardOwner(
    label="RFC 8693",
    title="OAuth 2.0 Token Exchange",
    runtime_status="lineage-audited-token-exchange-runtime",
    public_surface=("/token/exchange",),
    notes=(
        "RFC mapping for normalized token.exchange capability execution with "
        "subject-token validation, actor delegation, target selection, sender "
        "constraints, durable lineage, and audit observation."
    ),
)


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        requested_token_types_supported=(
            "urn:ietf:params:oauth:token-type:access_token",
            "access_token",
        ),
        delegation_supported=True,
        single_effective_target=True,
        spec_url=RFC8693_SPEC_URL,
    )


__all__ = [
    "OWNER",
    "RFC8693_SPEC_URL",
    "TOKEN_EXCHANGE_GRANT_TYPE",
    "TokenExchangeRequest",
    "TokenExchangeResponse",
    "TokenType",
    "describe",
    "exchange_token",
    "makeDelegationToken",
    "makeImpersonationToken",
    "validate_subject_token",
    "validate_token_exchange_request",
]
