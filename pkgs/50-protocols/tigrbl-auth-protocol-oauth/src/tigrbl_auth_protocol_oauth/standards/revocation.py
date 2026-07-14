"""RFC 7009 capability mapping without HTTP or persistence ownership."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from tigrbl_identity_contracts.tokens import (
    TokenRevocationRequest,
    TokenRevocationResult,
)
from tigrbl_token_revocation_capability import TokenRevocationCapability


RFC7009_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7009"
CANONICAL_REVOCATION_PATH: Final[str] = "/revoke"


class RevocationDisabledError(RuntimeError):
    """Raised when composition disables the RFC 7009 protocol feature."""


@dataclass(frozen=True, slots=True)
class RFC7009RevocationService:
    """Map RFC 7009 semantics to protocol-neutral token revocation."""

    capability: TokenRevocationCapability
    enabled: bool = True

    async def revoke(
        self,
        token: str,
        *,
        token_type_hint: str | None = None,
    ) -> TokenRevocationResult:
        if not self.enabled:
            raise RevocationDisabledError(
                f"RFC 7009 support is disabled: {RFC7009_SPEC_URL}"
            )
        call = await self.capability.call(
            "revoke_token",
            TokenRevocationRequest(
                token,
                token_type_hint=token_type_hint,
                reason="revoked_via_endpoint",
            ),
        )
        result = call.value
        if not isinstance(result, TokenRevocationResult):
            raise TypeError("token.revocation must return TokenRevocationResult")
        return result


__all__ = [
    "CANONICAL_REVOCATION_PATH",
    "RFC7009RevocationService",
    "RFC7009_SPEC_URL",
    "RevocationDisabledError",
]
