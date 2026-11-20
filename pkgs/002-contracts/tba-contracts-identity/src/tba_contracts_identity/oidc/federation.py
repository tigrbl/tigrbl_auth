"""OIDC Federation contract ports."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class FederationEntityStatementRequest:
    entity_id: str
    audience: str | None = None
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class FederationEntityStatementResult:
    entity_id: str
    statement: str | Mapping[str, Any]


class OidcFederationPort(Protocol):
    async def entity_statement(
        self,
        request: FederationEntityStatementRequest,
        /,
    ) -> FederationEntityStatementResult: ...


__all__ = [
    "FederationEntityStatementRequest",
    "FederationEntityStatementResult",
    "OidcFederationPort",
]
