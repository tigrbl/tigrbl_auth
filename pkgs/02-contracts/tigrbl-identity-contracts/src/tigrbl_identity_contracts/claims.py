"""Protocol-neutral claims selection and production contracts."""

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol


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
    user: Any | None = None
    session: Any | None = None
    consents: tuple[Any, ...] = ()
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ClaimsResult:
    claims: Mapping[str, Any]
    omitted: tuple[str, ...] = ()


class ClaimsProviderPort(Protocol):
    async def claims(self, request: ClaimsRequest, /) -> ClaimsResult: ...


__all__ = ["ClaimDescriptor", "ClaimsProviderPort", "ClaimsRequest", "ClaimsResult"]
