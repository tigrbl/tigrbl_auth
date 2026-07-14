"""OAuth 2.0 token endpoint capability mapping."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from tigrbl_identity_contracts.tokens import (
    IssuedTokenPair,
    RefreshTokenRedemptionRequest,
    TokenPairIssueRequest,
)
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from tigrbl_token_issuance_capability import TokenIssuanceCapability


STATUS: Final[str] = "profiled-token-issuance-runtime"
RFC6749_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc6749"

OWNER = StandardOwner(
    label="RFC 6749",
    title="OAuth 2.0 Authorization Framework Token Endpoint",
    runtime_status=STATUS,
    public_surface=("/token",),
    notes=(
        "Maps normalized token issuance and refresh rotation to the "
        "protocol-neutral token.issuance capability."
    ),
)


class TokenEndpointDisabledError(RuntimeError):
    """Raised when composition disables RFC 6749 token issuance."""


@dataclass(frozen=True, slots=True)
class RFC6749TokenEndpointService:
    capability: TokenIssuanceCapability
    enabled: bool = True

    def _require_enabled(self) -> None:
        if not self.enabled:
            raise TokenEndpointDisabledError(
                f"RFC 6749 token endpoint is disabled: {RFC6749_SPEC_URL}"
            )

    async def issue(self, request: TokenPairIssueRequest) -> IssuedTokenPair:
        self._require_enabled()
        call = await self.capability.call("issue_token_pair", request)
        if not isinstance(call.value, IssuedTokenPair):
            raise TypeError("token.issuance must return IssuedTokenPair")
        return call.value

    async def refresh(
        self,
        request: RefreshTokenRedemptionRequest,
    ) -> IssuedTokenPair:
        self._require_enabled()
        call = await self.capability.call("redeem_refresh_token", request)
        if not isinstance(call.value, IssuedTokenPair):
            raise TypeError("token.issuance must return IssuedTokenPair")
        return call.value


def describe() -> dict[str, object]:
    return describe_owner(OWNER, spec_url=RFC6749_SPEC_URL)


__all__ = [
    "OWNER",
    "RFC6749_SPEC_URL",
    "RFC6749TokenEndpointService",
    "STATUS",
    "TokenEndpointDisabledError",
    "describe",
]
