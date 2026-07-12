from dataclasses import dataclass
from typing import Protocol, Sequence

from .entities import PolicyEntity


@dataclass(frozen=True, slots=True)
class PolicySearchRequest:
    subject: PolicyEntity
    action: str | None = None
    resource_type: str | None = None


@dataclass(frozen=True, slots=True)
class PolicySearchResult:
    entities: Sequence[PolicyEntity]
    cursor: str | None = None


class PolicySearchPort(Protocol):
    def search(self, request: PolicySearchRequest, /) -> PolicySearchResult: ...


__all__ = ["PolicySearchPort", "PolicySearchRequest", "PolicySearchResult"]
