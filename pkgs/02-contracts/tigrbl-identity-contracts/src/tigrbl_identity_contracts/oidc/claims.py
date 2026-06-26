"""OIDC claims provider contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from ..schemas import AuthSessionReadResponse, ConsentReadResponse, UserReadResponse


@dataclass(frozen=True, slots=True)
class ClaimDescriptor:
    name: str
    source: str = "user"
    essential: bool = False


@dataclass(frozen=True, slots=True)
class ClaimsRequest:
    subject: str
    scopes: tuple[str, ...] = ()
    requested_claims: tuple[ClaimDescriptor, ...] = ()
    user: UserReadResponse | None = None
    session: AuthSessionReadResponse | None = None
    consents: tuple[ConsentReadResponse, ...] = ()
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ClaimsResult:
    claims: Mapping[str, Any]
    omitted: tuple[str, ...] = ()


class ClaimsProviderPort(Protocol):
    async def claims(self, request: ClaimsRequest, /) -> ClaimsResult: ...


__all__ = [
    "ClaimDescriptor",
    "ClaimsProviderPort",
    "ClaimsRequest",
    "ClaimsResult",
    "AuthSessionReadResponse",
    "ConsentReadResponse",
    "UserReadResponse",
]
