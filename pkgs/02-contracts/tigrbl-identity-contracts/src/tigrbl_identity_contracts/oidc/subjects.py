"""OIDC subject identifier contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib import import_module
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
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


def __getattr__(name: str) -> object:
    if name in {"SubjectAliasCreateRequest", "SubjectAliasReadResponse"}:
        return getattr(import_module("..schemas", __package__), name)
    raise AttributeError(name)


__all__ = [
    "SubjectAliasCreateRequest",
    "SubjectAliasReadResponse",
    "SubjectIdentifierKind",
    "SubjectIdentifierRequest",
    "SubjectIdentifierResult",
    "SubjectIdentifierStrategyPort",
]
