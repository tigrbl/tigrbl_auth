"""RFC 7662 capability mapping without HTTP or persistence ownership."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from tigrbl_identity_contracts.tokens import (
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
)
from tigrbl_token_introspection_capability import TokenIntrospectionCapability

from ._introspection_activity import apply_introspection_activity_constraints


RFC7662_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7662"


class IntrospectionDisabledError(RuntimeError):
    """Raised when composition disables the RFC 7662 protocol feature."""


@dataclass(frozen=True, slots=True)
class RFC7662IntrospectionService:
    """Map RFC 7662 semantics to protocol-neutral token introspection."""

    capability: TokenIntrospectionCapability
    enabled: bool = True

    async def introspect(self, token: str) -> dict[str, object]:
        if not self.enabled:
            raise IntrospectionDisabledError(
                f"RFC 7662 support is disabled: {RFC7662_SPEC_URL}"
            )

        call = await self.capability.call(
            "introspect_token",
            TokenIntrospectionRequest(token),
        )
        result = call.value
        if not isinstance(result, TokenIntrospectionResult):
            raise TypeError("token.introspection must return TokenIntrospectionResult")

        payload: dict[str, object] = dict(result.claims)
        payload["active"] = result.active
        if result.reason is not None:
            payload.setdefault("inactive_reason", result.reason)
        return apply_introspection_activity_constraints(payload)


__all__ = [
    "IntrospectionDisabledError",
    "RFC7662IntrospectionService",
    "RFC7662_SPEC_URL",
]
