from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

from .graph import AuthorityScope


class AuthorityMutationKind(str, Enum):
    GRANT = "grant"
    REVOKE = "revoke"
    REPLACE = "replace"


@dataclass(frozen=True, slots=True)
class AuthorityClosure:
    subject: str
    scopes: tuple[AuthorityScope, ...]
    provenance: Mapping[tuple[str, str, str, str], tuple[str, ...]] = field(default_factory=dict)

    @property
    def keys(self) -> frozenset[tuple[str, str, str, str]]:
        return frozenset(scope.key for scope in self.scopes)


@dataclass(frozen=True, slots=True)
class AuthorityMonotonicityReport:
    passed: bool
    mutation_kind: AuthorityMutationKind
    added: tuple[AuthorityScope, ...]
    removed: tuple[AuthorityScope, ...]
    failures: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LeastAuthorityDiff:
    passed: bool
    required: tuple[AuthorityScope, ...]
    effective: tuple[AuthorityScope, ...]
    missing: tuple[AuthorityScope, ...]
    excess: tuple[AuthorityScope, ...]
    excess_provenance: Mapping[tuple[str, str, str, str], tuple[str, ...]] = field(default_factory=dict)


__all__ = [
    "AuthorityClosure",
    "AuthorityMutationKind",
    "AuthorityMonotonicityReport",
    "LeastAuthorityDiff",
]
