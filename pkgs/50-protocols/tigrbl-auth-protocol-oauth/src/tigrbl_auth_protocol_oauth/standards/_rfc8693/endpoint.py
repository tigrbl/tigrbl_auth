"""Deterministic RFC 8693 compatibility helpers; no HTTP carrier ownership."""

from __future__ import annotations

from tigrbl_auth_protocol_oauth.standards._rfc8693.runtime import (
    TOKEN_EXCHANGE_GRANT_TYPE,
    TokenExchangeRequest,
    TokenExchangeResponse,
    TokenType,
    exchange_token,
)


def makeImpersonationToken(
    *,
    subject_token: str,
    actor_token: str,
    audience: str | None = None,
    scope: str | None = None,
    issuer: str = "https://issuer.example",
    client_id: str | None = None,
) -> TokenExchangeResponse:
    request = TokenExchangeRequest(
        grant_type=TOKEN_EXCHANGE_GRANT_TYPE,
        subject_token=subject_token,
        subject_token_type=TokenType.ACCESS_TOKEN.value,
        actor_token=actor_token,
        actor_token_type=TokenType.ACCESS_TOKEN.value,
        audience=audience,
        scope=scope,
    )
    return exchange_token(request, issuer=issuer, client_id=client_id)


def makeDelegationToken(
    *,
    subject_token: str,
    audience: str | None = None,
    scope: str | None = None,
    issuer: str = "https://issuer.example",
    client_id: str | None = None,
) -> TokenExchangeResponse:
    request = TokenExchangeRequest(
        grant_type=TOKEN_EXCHANGE_GRANT_TYPE,
        subject_token=subject_token,
        subject_token_type=TokenType.ACCESS_TOKEN.value,
        audience=audience,
        scope=scope,
    )
    return exchange_token(request, issuer=issuer, client_id=client_id)


__all__ = [
    "makeDelegationToken",
    "makeImpersonationToken",
]
