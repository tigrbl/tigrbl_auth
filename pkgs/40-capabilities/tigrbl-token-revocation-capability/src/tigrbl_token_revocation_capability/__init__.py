"""Composable protocol-neutral token revocation capability."""

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
    TokenRevocationRequest,
    TokenRevocationResult,
)


RevocationTarget: TypeAlias = Callable[
    [str, str | None, str],
    str | TokenRevocationResult | Awaitable[str | TokenRevocationResult],
]
AuditTarget: TypeAlias = Callable[
    [Mapping[str, object]], None | Awaitable[None]
]


class TokenRevocationCapability(Capability):
    """Coordinate durable token revocation and optional audit recording."""

    def __init__(
        self,
        revoke_token: RevocationTarget | None,
        record_audit_event: AuditTarget | None = None,
    ) -> None:
        self._revoke_token = revoke_token
        self._record_audit_event = record_audit_event
        super().__init__(
            CapabilityDefinition("token.revocation", "1.0"),
            operations={
                "revoke_token": CapabilityOperation(
                    target=self.revoke if revoke_token is not None else None,
                    delegated=True,
                ),
                "record_audit_event": CapabilityOperation(
                    target=record_audit_event,
                    required=False,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=self._revoke_token is not None,
                status="ready" if self._revoke_token is not None else "unbound",
                details={
                    "audit_bound": self._record_audit_event is not None,
                },
            ),
        )

    async def revoke(
        self,
        request: TokenRevocationRequest,
    ) -> TokenRevocationResult:
        if not isinstance(request, TokenRevocationRequest):
            raise TypeError("request must be a TokenRevocationRequest")
        if self._revoke_token is None:  # construction rejects this path
            raise NotImplementedError("token revocation target is not bound")

        value = self._revoke_token(
            request.token,
            request.token_type_hint,
            request.reason,
        )
        if inspect.isawaitable(value):
            value = await value
        result = (
            value
            if isinstance(value, TokenRevocationResult)
            else TokenRevocationResult(token_reference=str(value))
        )

        if self._record_audit_event is not None:
            audit = self._record_audit_event(
                {
                    "event_type": "token.revoked",
                    "target_type": "token",
                    "target_id": request.token[:16],
                    "details": {"token_type_hint": request.token_type_hint},
                }
            )
            if inspect.isawaitable(audit):
                await audit
        return result


__all__ = [
    "AuditTarget",
    "RevocationTarget",
    "TokenRevocationCapability",
    "TokenRevocationRequest",
    "TokenRevocationResult",
]
