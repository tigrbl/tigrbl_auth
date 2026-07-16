"""Composable protocol-neutral grant negotiation capability."""

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
from tigrbl_identity_contracts.gnap import (
    GrantContinuationRequest,
    GrantNegotiationRequest,
    GrantNegotiationResult,
)

RequestGrantTarget: TypeAlias = Callable[
    [GrantNegotiationRequest],
    GrantNegotiationResult | Awaitable[GrantNegotiationResult],
]
ContinueGrantTarget: TypeAlias = Callable[
    [GrantContinuationRequest],
    GrantNegotiationResult | Awaitable[GrantNegotiationResult],
]


class GrantNegotiationCapability(Capability):
    """Delegate negotiated grant lifecycles through typed reportable operations."""

    def __init__(
        self,
        request_grant: RequestGrantTarget | None,
        *,
        continue_grant: ContinueGrantTarget | None = None,
        rotate_access_token: ContinueGrantTarget | None = None,
    ) -> None:
        self._request_grant = request_grant
        self._continue_grant = continue_grant
        self._rotate_access_token = rotate_access_token
        super().__init__(
            CapabilityDefinition("grant.negotiation", "1.0"),
            operations={
                "request_grant": CapabilityOperation(
                    target=self.request if request_grant is not None else None,
                    delegated=True,
                ),
                "continue_grant": CapabilityOperation(
                    target=self.continue_request
                    if continue_grant is not None
                    else None,
                    required=False,
                    delegated=True,
                ),
                "rotate_access_token": CapabilityOperation(
                    target=(self.rotate if rotate_access_token is not None else None),
                    required=False,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=self._request_grant is not None,
                status="ready" if self._request_grant is not None else "unbound",
                details={
                    "continuation_bound": self._continue_grant is not None,
                    "rotation_bound": self._rotate_access_token is not None,
                },
            ),
        )

    async def _result(self, value: object) -> GrantNegotiationResult:
        if inspect.isawaitable(value):
            value = await value
        if not isinstance(value, GrantNegotiationResult):
            raise TypeError("grant target must return GrantNegotiationResult")
        return value

    async def request(self, request: GrantNegotiationRequest) -> GrantNegotiationResult:
        if not isinstance(request, GrantNegotiationRequest):
            raise TypeError("request must be a GrantNegotiationRequest")
        if self._request_grant is None:  # construction rejects this path
            raise NotImplementedError("grant request target is not bound")
        return await self._result(self._request_grant(request))

    async def continue_request(
        self, request: GrantContinuationRequest
    ) -> GrantNegotiationResult:
        if not isinstance(request, GrantContinuationRequest):
            raise TypeError("request must be a GrantContinuationRequest")
        if self._continue_grant is None:
            raise NotImplementedError("grant continuation target is not bound")
        return await self._result(self._continue_grant(request))

    async def rotate(self, request: GrantContinuationRequest) -> GrantNegotiationResult:
        if not isinstance(request, GrantContinuationRequest):
            raise TypeError("request must be a GrantContinuationRequest")
        if self._rotate_access_token is None:
            raise NotImplementedError("access-token rotation target is not bound")
        return await self._result(self._rotate_access_token(request))


__all__ = [
    "ContinueGrantTarget",
    "GrantNegotiationCapability",
    "RequestGrantTarget",
]
