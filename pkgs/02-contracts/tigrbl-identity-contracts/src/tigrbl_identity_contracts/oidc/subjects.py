"""OIDC subject identifier contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from ..schemas import SubjectAliasCreateRequest, SubjectAliasReadResponse


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
    alias: SubjectAliasReadResponse | None = None


class SubjectIdentifierStrategyPort(Protocol):
    def derive(self, request: SubjectIdentifierRequest, /) -> SubjectIdentifierResult: ...


__all__ = [
    "SubjectAliasCreateRequest",
    "SubjectAliasReadResponse",
    "SubjectIdentifierKind",
    "SubjectIdentifierRequest",
    "SubjectIdentifierResult",
    "SubjectIdentifierStrategyPort",
]
