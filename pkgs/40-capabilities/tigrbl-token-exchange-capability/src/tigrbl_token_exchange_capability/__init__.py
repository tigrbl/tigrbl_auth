"""Composable protocol-neutral security-token exchange capability."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.oauth.exchange import (
    TokenExchangeContext,
    TokenExchangeRequest,
    TokenExchangeResponse,
)


ExchangeTarget: TypeAlias = Callable[
    [TokenExchangeRequest, TokenExchangeContext],
    TokenExchangeResponse | Awaitable[TokenExchangeResponse],
]


class TokenExchangeCapability(Capability):
    """Delegate a normalized exchange through one reportable operation."""

    def __init__(self, exchange_token: ExchangeTarget | None) -> None:
        self._exchange_token = exchange_token
        super().__init__(
            CapabilityDefinition("token.exchange", "1.0"),
            operations={
                "exchange_token": CapabilityOperation(
                    target=self.exchange if exchange_token is not None else None,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=self._exchange_token is not None,
                status="ready" if self._exchange_token is not None else "unbound",
            ),
        )

    async def exchange(
        self,
        request: TokenExchangeRequest,
        *,
        context: TokenExchangeContext,
    ) -> TokenExchangeResponse:
        if not isinstance(request, TokenExchangeRequest):
            raise TypeError("request must be a TokenExchangeRequest")
        if not isinstance(context, TokenExchangeContext):
            raise TypeError("context must be a TokenExchangeContext")
        if self._exchange_token is None:  # construction rejects this path
            raise NotImplementedError("token exchange target is not bound")
        value = self._exchange_token(request, context)
        if inspect.isawaitable(value):
            value = await value
        if not isinstance(value, TokenExchangeResponse):
            raise TypeError("token exchange target must return TokenExchangeResponse")
        return value


__all__ = [
    "ExchangeTarget",
    "TokenExchangeCapability",
    "TokenExchangeContext",
    "TokenExchangeRequest",
    "TokenExchangeResponse",
]
