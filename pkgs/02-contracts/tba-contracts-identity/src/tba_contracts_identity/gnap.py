"""Protocol-neutral grant negotiation contracts used by GNAP mappings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol


@dataclass(frozen=True, slots=True)
class GrantAccessRequest:
    access: tuple[object, ...]
    label: str | None = None
    flags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class GrantNegotiationRequest:
    access_tokens: tuple[GrantAccessRequest, ...]
    client_instance: Mapping[str, object] | str
    interaction: Mapping[str, object] | None = None
    subject: Mapping[str, object] | None = None


@dataclass(frozen=True, slots=True)
class GrantContinuationRequest:
    continuation_token: str
    proof: str | bytes | Mapping[str, object] | None = None


@dataclass(frozen=True, slots=True)
class GrantNegotiationResult:
    grant_id: str
    status: str
    access_tokens: tuple[Mapping[str, object], ...] = ()
    continuation: Mapping[str, object] | None = None
    interaction: Mapping[str, object] | None = None
    subject: Mapping[str, object] | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)


class GrantNegotiationPort(Protocol):
    async def request_grant(
        self, request: GrantNegotiationRequest, /
    ) -> GrantNegotiationResult: ...

    async def continue_grant(
        self, request: GrantContinuationRequest, /
    ) -> GrantNegotiationResult: ...

    async def rotate_access_token(
        self, request: GrantContinuationRequest, /
    ) -> GrantNegotiationResult: ...


__all__ = [
    "GrantAccessRequest",
    "GrantContinuationRequest",
    "GrantNegotiationPort",
    "GrantNegotiationRequest",
    "GrantNegotiationResult",
]
