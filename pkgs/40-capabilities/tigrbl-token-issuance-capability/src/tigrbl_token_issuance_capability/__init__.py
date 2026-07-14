"""Composable protocol-neutral token issuance capability."""

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
    IssuedTokenPair,
    RefreshTokenRedemptionRequest,
    TokenPairIssueRequest,
)


IssueTarget: TypeAlias = Callable[
    [TokenPairIssueRequest], IssuedTokenPair | Awaitable[IssuedTokenPair]
]
RefreshTarget: TypeAlias = Callable[
    [RefreshTokenRedemptionRequest],
    IssuedTokenPair | Awaitable[IssuedTokenPair],
]
AuditTarget: TypeAlias = Callable[
    [Mapping[str, object]], None | Awaitable[None]
]


async def _issued(value: object, *, operation: str) -> IssuedTokenPair:
    if inspect.isawaitable(value):
        value = await value
    if not isinstance(value, IssuedTokenPair):
        raise TypeError(f"{operation} must return IssuedTokenPair")
    return value


class TokenIssuanceCapability(Capability):
    """Coordinate new token-pair issuance and refresh-token rotation."""

    def __init__(
        self,
        issue_token_pair: IssueTarget | None,
        redeem_refresh_token: RefreshTarget | None,
        record_audit_event: AuditTarget | None = None,
    ) -> None:
        self._issue_token_pair = issue_token_pair
        self._redeem_refresh_token = redeem_refresh_token
        self._record_audit_event = record_audit_event
        ready = issue_token_pair is not None and redeem_refresh_token is not None
        super().__init__(
            CapabilityDefinition("token.issuance", "1.0"),
            operations={
                "issue_token_pair": CapabilityOperation(
                    target=self.issue if issue_token_pair is not None else None,
                    delegated=True,
                ),
                "redeem_refresh_token": CapabilityOperation(
                    target=self.redeem if redeem_refresh_token is not None else None,
                    delegated=True,
                ),
                "record_audit_event": CapabilityOperation(
                    target=record_audit_event,
                    required=False,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=ready,
                status="ready" if ready else "unbound",
                details={"audit_bound": self._record_audit_event is not None},
            ),
        )

    async def _audit(self, event: Mapping[str, object]) -> None:
        if self._record_audit_event is None:
            return
        value = self._record_audit_event(event)
        if inspect.isawaitable(value):
            await value

    async def issue(self, request: TokenPairIssueRequest) -> IssuedTokenPair:
        if not isinstance(request, TokenPairIssueRequest):
            raise TypeError("request must be a TokenPairIssueRequest")
        if self._issue_token_pair is None:
            raise NotImplementedError("token-pair issuance target is not bound")
        result = await _issued(
            self._issue_token_pair(request),
            operation="issue_token_pair",
        )
        await self._audit(
            {
                "event_type": "token.pair.issued",
                "target_type": "token",
                "target_id": request.client_id,
                "tenant_id": request.tenant_id,
                "actor_client_id": request.client_id,
                "details": {
                    "subject": request.subject,
                    "scope": request.scope,
                    "audience": request.audience,
                    "sender_constrained": request.confirmation is not None,
                },
            }
        )
        return result

    async def redeem(
        self,
        request: RefreshTokenRedemptionRequest,
    ) -> IssuedTokenPair:
        if not isinstance(request, RefreshTokenRedemptionRequest):
            raise TypeError("request must be a RefreshTokenRedemptionRequest")
        if self._redeem_refresh_token is None:
            raise NotImplementedError("refresh redemption target is not bound")
        result = await _issued(
            self._redeem_refresh_token(request),
            operation="redeem_refresh_token",
        )
        await self._audit(
            {
                "event_type": "token.refresh.rotated",
                "target_type": "token",
                "target_id": request.client_id,
                "actor_client_id": request.client_id,
                "details": {
                    "audience": request.requested_audience,
                    "sender_constrained": (
                        request.certificate_thumbprint is not None
                    ),
                },
            }
        )
        return result


__all__ = [
    "AuditTarget",
    "IssueTarget",
    "RefreshTarget",
    "TokenIssuanceCapability",
]
