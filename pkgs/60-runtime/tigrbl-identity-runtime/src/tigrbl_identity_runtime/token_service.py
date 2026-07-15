"""Typed runtime token service backed by the effective capability registry."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_contracts.capabilities import CapabilityCallContext
from tigrbl_identity_contracts.tokens import (
    IssuedTokenPair,
    RefreshTokenRedemptionRequest,
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
    TokenPairIssueRequest,
    TokenRevocationRequest,
    TokenRevocationResult,
)

from .capability_registry import CapabilityRegistry


class RuntimeTokenService:
    def __init__(self, registry: CapabilityRegistry, *, db: Any) -> None:
        self._registry = registry
        self._db = db

    async def issue_token_pair(
        self,
        request: TokenPairIssueRequest,
        *,
        context: CapabilityCallContext | None = None,
    ) -> IssuedTokenPair:
        capability = self._registry.materialize("token.issuance", self._db)
        result = await capability.call("issue_token_pair", request, context=context)
        if not isinstance(result.value, IssuedTokenPair):
            raise TypeError("token.issuance.issue_token_pair returned an invalid result")
        return result.value

    async def redeem_refresh_token(
        self,
        request: RefreshTokenRedemptionRequest,
        *,
        context: CapabilityCallContext | None = None,
    ) -> IssuedTokenPair:
        capability = self._registry.materialize("token.issuance", self._db)
        result = await capability.call(
            "redeem_refresh_token",
            request,
            context=context,
        )
        if not isinstance(result.value, IssuedTokenPair):
            raise TypeError(
                "token.issuance.redeem_refresh_token returned an invalid result"
            )
        return result.value

    async def introspect_token(
        self,
        request: TokenIntrospectionRequest,
        *,
        context: CapabilityCallContext | None = None,
    ) -> TokenIntrospectionResult:
        result = await self._registry.call(
            "token.introspection",
            "introspect_token",
            request,
            context=context,
        )
        if not isinstance(result.value, TokenIntrospectionResult):
            raise TypeError(
                "token.introspection.introspect_token returned an invalid result"
            )
        return result.value

    async def revoke_token(
        self,
        request: TokenRevocationRequest,
        *,
        context: CapabilityCallContext | None = None,
    ) -> TokenRevocationResult:
        result = await self._registry.call(
            "token.revocation",
            "revoke_token",
            request,
            context=context,
        )
        if not isinstance(result.value, TokenRevocationResult):
            raise TypeError("token.revocation.revoke_token returned an invalid result")
        return result.value


_COMPAT_EXPORTS = {
    "DEFAULT_ACCESS_TOKEN_TTL",
    "DEFAULT_REFRESH_TOKEN_TTL",
    "InvalidRefreshTokenError",
    "InvalidTokenError",
    "JWTCoder",
    "RefreshTokenError",
    "RefreshTokenReuseError",
    "TokenCoder",
    "exchange_token_for_context",
    "get_token_for_context",
    "introspect_token_for_context",
    "issue_persisted_token_pair",
    "list_tokens_for_context",
    "redeem_refresh_token",
    "revoke_all_tokens_for_context",
    "revoke_token_for_context",
    "_ACCESS_TTL",
    "_REFRESH_TTL",
    "_header_alg",
    "_load_runtime",
    "_run",
    "_svc",
    "_svc_async",
}


def __getattr__(name: str) -> object:
    if name in _COMPAT_EXPORTS:
        from . import token_service_compat

        return getattr(token_service_compat, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["RuntimeTokenService", *sorted(_COMPAT_EXPORTS)]
