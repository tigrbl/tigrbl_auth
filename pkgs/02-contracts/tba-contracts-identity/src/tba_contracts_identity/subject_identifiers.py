"""Protocol-neutral public, pairwise, transient, and opaque identifier contracts."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class SubjectIdentifierKind(str, Enum):
    PUBLIC = "public"
    PAIRWISE = "pairwise"
    TRANSIENT = "transient"
    OPAQUE = "opaque"


@dataclass(frozen=True, slots=True)
class SubjectIdentifierRequest:
    subject: str
    issuer: str
    kind: SubjectIdentifierKind = SubjectIdentifierKind.PUBLIC
    sector_identifier: str | None = None
    salt: str | None = None


@dataclass(frozen=True, slots=True)
class SubjectIdentifierResult:
    subject_identifier: str
    kind: SubjectIdentifierKind
    alias: Any | None = None


class SubjectIdentifierStrategyPort(Protocol):
    def derive(
        self, request: SubjectIdentifierRequest, /
    ) -> SubjectIdentifierResult: ...


__all__ = [
    "SubjectIdentifierKind",
    "SubjectIdentifierRequest",
    "SubjectIdentifierResult",
    "SubjectIdentifierStrategyPort",
]
