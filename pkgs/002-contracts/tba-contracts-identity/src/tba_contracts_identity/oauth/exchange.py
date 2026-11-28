"""Protocol-neutral token-exchange capability contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol


@dataclass(frozen=True, slots=True)
class TokenExchangeRequest:
    """Normalized request to exchange one security token for another."""

    subject_token: str
    subject_token_type: str
    actor_token: str | None = None
    actor_token_type: str | None = None
    resources: tuple[str, ...] = ()
    audience: str | None = None
    scope: str | None = None
    requested_token_type: str | None = None
    delegation_grant_id: str | None = None

    def __post_init__(self) -> None:
        if not self.subject_token:
            raise ValueError("subject_token is required")
        if not self.subject_token_type:
            raise ValueError("subject_token_type is required")
        if bool(self.actor_token) != bool(self.actor_token_type):
            raise ValueError(
                "actor_token and actor_token_type must be supplied together"
            )


@dataclass(frozen=True, slots=True)
class TokenExchangeSenderConstraint:
    """Normalized proof-of-possession result for an exchange request."""

    mechanism: str
    token_type: str
    confirmation_claim: Mapping[str, object] | None = None
    certificate_thumbprint: str | None = None


@dataclass(frozen=True, slots=True)
class TokenExchangeContext:
    """Trusted runtime context supplied after carrier/security validation."""

    issuer: str
    protected_resource_identifier: str | None
    sender_constraint: TokenExchangeSenderConstraint
    verifier_logic_id: str
    required_claims: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TokenExchangeResponse:
    """Normalized successful exchange result."""

    access_token: str
    issued_token_type: str
    token_type: str
    scope: str | None = None
    audience: str | None = None
    exchange_mode: str | None = None
    extensions: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.access_token:
            raise ValueError("access_token is required")
        if not self.issued_token_type:
            raise ValueError("issued_token_type is required")
        if not self.token_type:
            raise ValueError("token_type is required")

    def to_mapping(self) -> dict[str, object]:
        result: dict[str, object] = {
            "access_token": self.access_token,
            "issued_token_type": self.issued_token_type,
            "token_type": self.token_type,
        }
        if self.scope:
            result["scope"] = self.scope
        if self.audience:
            result["audience"] = self.audience
        if self.exchange_mode:
            result["exchange_mode"] = self.exchange_mode
        result.update(self.extensions)
        return result


class TokenExchangeServicePort(Protocol):
    async def exchange(
        self,
        request: TokenExchangeRequest,
        /,
        *,
        context: TokenExchangeContext,
    ) -> TokenExchangeResponse: ...


__all__ = [
    "TokenExchangeContext",
    "TokenExchangeRequest",
    "TokenExchangeResponse",
    "TokenExchangeSenderConstraint",
    "TokenExchangeServicePort",
]
