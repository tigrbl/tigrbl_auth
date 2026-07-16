from __future__ import annotations

from typing import Any, Callable, Mapping

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    TokenValidationError,
)
from tigrbl_security_trust_contracts import (
    CapabilityMap,
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
)
from tigrbl_token_introspection_bases import TokenIntrospectionClientBase


class IntrospectionClient(TokenIntrospectionClientBase):
    """Convert OAuth token introspection responses into access-token claims."""

    def __init__(
        self,
        transport: Callable[[str], Mapping[str, Any] | TokenIntrospectionResult],
    ) -> None:
        self.transport = transport

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"token-introspection": ("oauth2",)})

    def introspect(
        self,
        request: TokenIntrospectionRequest,
    ) -> TokenIntrospectionResult:
        payload = self.transport(request.token)
        if isinstance(payload, TokenIntrospectionResult):
            return payload
        return TokenIntrospectionResult(
            active=bool(payload.get("active")),
            claims=dict(payload),
        )

    def introspect_claims(
        self,
        token: str | TokenIntrospectionRequest,
    ) -> AccessTokenClaims:
        request = token if isinstance(token, TokenIntrospectionRequest) else TokenIntrospectionRequest(token=token)
        result = self.introspect(request)
        if not result.active:
            raise TokenValidationError("introspection response is inactive")
        payload = dict(result.claims)
        scope_value = payload.get("scope", ())
        scopes = tuple(scope_value.split()) if isinstance(scope_value, str) else tuple(scope_value)
        aud_value = payload.get("aud", ())
        audiences = (aud_value,) if isinstance(aud_value, str) else tuple(aud_value)
        return AccessTokenClaims(
            iss=str(payload["iss"]),
            sub=str(payload["sub"]),
            aud=audiences,
            exp=int(payload["exp"]),
            iat=int(payload.get("iat", 0)),
            scope=scopes,
            cnf=payload.get("cnf", {}),
        )


__all__ = ["IntrospectionClient"]
