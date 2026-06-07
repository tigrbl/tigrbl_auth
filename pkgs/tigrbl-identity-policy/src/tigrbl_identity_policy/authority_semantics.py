from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

from .authority_graph import AuthorityDerivationGraph, AuthorityScope


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


def compute_authority_closure(graph: AuthorityDerivationGraph, subject: str) -> AuthorityClosure:
    paths = graph.derive_paths(subject)
    scopes: dict[tuple[str, str, str, str], AuthorityScope] = {}
    provenance: dict[tuple[str, str, str, str], set[str]] = {}
    for path in paths:
        for scope in path.scopes:
            scopes[scope.key] = scope
            provenance.setdefault(scope.key, set()).update(path.edge_ids)
    return AuthorityClosure(
        subject=subject,
        scopes=tuple(scopes[key] for key in sorted(scopes)),
        provenance={key: tuple(sorted(edge_ids)) for key, edge_ids in provenance.items()},
    )


def compare_authority_monotonicity(
    before: AuthorityClosure,
    after: AuthorityClosure,
    *,
    mutation_kind: AuthorityMutationKind,
) -> AuthorityMonotonicityReport:
    mutation_kind = AuthorityMutationKind(mutation_kind)
    before_by_key = {scope.key: scope for scope in before.scopes}
    after_by_key = {scope.key: scope for scope in after.scopes}
    added_keys = set(after_by_key) - set(before_by_key)
    removed_keys = set(before_by_key) - set(after_by_key)
    failures: list[str] = []
    if mutation_kind == AuthorityMutationKind.GRANT and removed_keys:
        failures.append("grant mutation removed existing authority")
    if mutation_kind == AuthorityMutationKind.REVOKE and added_keys:
        failures.append("revoke mutation added authority")
    if mutation_kind == AuthorityMutationKind.REPLACE and not (added_keys or removed_keys):
        failures.append("replace mutation did not change authority")
    return AuthorityMonotonicityReport(
        passed=not failures,
        mutation_kind=mutation_kind,
        added=tuple(after_by_key[key] for key in sorted(added_keys)),
        removed=tuple(before_by_key[key] for key in sorted(removed_keys)),
        failures=tuple(failures),
    )


def diff_least_authority(
    *,
    required: tuple[AuthorityScope, ...],
    effective: AuthorityClosure,
) -> LeastAuthorityDiff:
    required_keys = {scope.key: scope for scope in required}
    effective_keys = {scope.key: scope for scope in effective.scopes}
    missing: dict[tuple[str, str, str, str], AuthorityScope] = {}
    excess: dict[tuple[str, str, str, str], AuthorityScope] = {}
    for key, required_scope in required_keys.items():
        if not any(scope.covers(required_scope) for scope in effective.scopes):
            missing[key] = required_scope
    for key, effective_scope in effective_keys.items():
        if not any(required_scope.covers(effective_scope) for required_scope in required):
            excess[key] = effective_scope
    return LeastAuthorityDiff(
        passed=not missing and not excess,
        required=tuple(required_keys[key] for key in sorted(required_keys)),
        effective=effective.scopes,
        missing=tuple(missing[key] for key in sorted(missing)),
        excess=tuple(excess[key] for key in sorted(excess)),
        excess_provenance={key: effective.provenance.get(key, ()) for key in sorted(excess)},
    )


__all__ = [
    "AuthorityClosure",
    "AuthorityMutationKind",
    "AuthorityMonotonicityReport",
    "LeastAuthorityDiff",
    "compare_authority_monotonicity",
    "compute_authority_closure",
    "diff_least_authority",
]
