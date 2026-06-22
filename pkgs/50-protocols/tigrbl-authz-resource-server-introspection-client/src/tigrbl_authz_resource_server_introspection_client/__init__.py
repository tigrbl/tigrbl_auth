from __future__ import annotations

from tigrbl_identity_contracts.resource_server import (
    AccessTokenClaims,
    IntrospectionTransport,
    TokenValidationError,
)


class IntrospectionClient:
    """Convert OAuth token introspection responses into access-token claims."""

    def __init__(self, transport: IntrospectionTransport) -> None:
        self.transport = transport

    def introspect(self, token: str) -> AccessTokenClaims:
        payload = dict(self.transport(token))
        if not payload.get("active"):
            raise TokenValidationError("introspection response is inactive")
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
