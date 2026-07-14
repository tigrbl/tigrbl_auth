"""Composable protocol-neutral token introspection capability."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.tokens import (
    TokenIntrospectionRequest,
    TokenIntrospectionResult,
    TokenProfile,
)


IntrospectionTarget: TypeAlias = Callable[
    [str],
    TokenIntrospectionResult
    | Mapping[str, object]
    | Awaitable[TokenIntrospectionResult | Mapping[str, object]],
]


def _profile(value: object) -> TokenProfile | None:
    if isinstance(value, TokenProfile):
        return value
    if isinstance(value, str):
        try:
            return TokenProfile(value)
        except ValueError:
            return None
    return None


class TokenIntrospectionCapability(Capability):
    """Delegate normalized token-state lookup through one reportable operation."""

    def __init__(self, introspect_token: IntrospectionTarget | None) -> None:
        self._introspect_token = introspect_token
        super().__init__(
            CapabilityDefinition("token.introspection", "1.0"),
            operations={
                "introspect_token": CapabilityOperation(
                    target=self.introspect_token if introspect_token is not None else None,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=self._introspect_token is not None,
                healthy=None,
                status="ready" if self._introspect_token is not None else "unbound",
            ),
        )

    async def introspect_token(
        self,
        request: TokenIntrospectionRequest,
    ) -> TokenIntrospectionResult:
        if not isinstance(request, TokenIntrospectionRequest):
            raise TypeError("request must be a TokenIntrospectionRequest")
        if self._introspect_token is None:  # construction rejects this path
            raise NotImplementedError("token introspection target is not bound")

        value = self._introspect_token(request.token)
        if inspect.isawaitable(value):
            value = await value
        if isinstance(value, TokenIntrospectionResult):
            result = value
        elif isinstance(value, Mapping):
            payload = dict(value)
            active = bool(payload.pop("active", False))
            result = TokenIntrospectionResult(
                active=active,
                claims=payload,
                profile=_profile(payload.get("token_profile") or payload.get("profile")),
            )
        else:
            raise TypeError(
                "token introspection target must return TokenIntrospectionResult or a mapping"
            )

        if (
            result.active
            and request.expected_profile is not None
            and result.profile != request.expected_profile
        ):
            return TokenIntrospectionResult(
                active=False,
                profile=result.profile,
                reason="token profile mismatch",
            )
        return result


__all__ = [
    "IntrospectionTarget",
    "TokenIntrospectionCapability",
    "TokenIntrospectionRequest",
    "TokenIntrospectionResult",
]
