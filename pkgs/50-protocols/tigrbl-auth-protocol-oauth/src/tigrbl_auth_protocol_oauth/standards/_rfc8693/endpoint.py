"""Token exchange endpoint compatibility marker.

The concrete endpoint is owned by
``tigrbl_identity_storage_runtime.token_exchange``.
"""

from __future__ import annotations

from tigrbl_auth_protocol_oauth.standards._rfc8693.runtime import *


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


__all__ = [name for name in globals() if not name.startswith("_")]
