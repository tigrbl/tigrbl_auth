from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .authority_graph import AuthorityScope


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


@dataclass(frozen=True, slots=True)
class DelegationGrant:
    delegator: str
    delegate: str
    tenant_ids: tuple[str, ...]
    actions: tuple[str, ...]
    resources: tuple[str, ...] = ("*",)
    realm: str = ""
    policy_version: str = ""
    provenance_id: str = ""
    revoked: bool = False
    expires_at: str | None = None

    def __post_init__(self) -> None:
        if not self.delegator or not self.delegate:
            raise ValueError("delegator and delegate are required")
        if not self.tenant_ids or not self.actions:
            raise ValueError("tenant_ids and actions are required")
        object.__setattr__(self, "tenant_ids", tuple(sorted(set(self.tenant_ids))))
        object.__setattr__(self, "actions", tuple(sorted(set(self.actions))))
        object.__setattr__(self, "resources", tuple(sorted(set(self.resources or ("*",)))))

    def scopes(self) -> tuple[AuthorityScope, ...]:
        return tuple(
            AuthorityScope(tenant_id=tenant_id, realm=self.realm, action=action, resource=resource)
            for tenant_id in self.tenant_ids
            for action in self.actions
            for resource in self.resources
        )


@dataclass(frozen=True, slots=True)
class DelegationAttenuationProof:
    grant: DelegationGrant
    passed: bool
    delegated_scopes: tuple[AuthorityScope, ...]
    uncovered_scopes: tuple[AuthorityScope, ...]
    source_scope_count: int
    provenance_id: str = ""
    failures: tuple[str, ...] = ()


def prove_delegation_attenuation(
    *,
    source_scopes: Iterable[AuthorityScope],
    grant: DelegationGrant,
    known_provenance_ids: Iterable[str] | None = None,
    allowed_policy_versions: Iterable[str] | None = None,
    evaluated_at: str | None = None,
) -> DelegationAttenuationProof:
    source = tuple(source_scopes)
    delegated = grant.scopes()
    uncovered = tuple(scope for scope in delegated if not any(source_scope.covers(scope) for source_scope in source))
    failures = [
        f"delegated scope {scope.action!r} on {scope.resource!r} is not covered in tenant {scope.tenant_id!r}"
        for scope in uncovered
    ]
    if grant.revoked:
        failures.append("delegation grant is revoked")
    if grant.expires_at is not None and evaluated_at is not None and _parse_time(grant.expires_at) <= _parse_time(evaluated_at):
        failures.append("delegation grant is expired")
    if known_provenance_ids is not None:
        known = set(known_provenance_ids)
        if not grant.provenance_id:
            failures.append("delegation provenance is required")
        elif grant.provenance_id not in known:
            failures.append(f"unknown delegation provenance {grant.provenance_id!r}")
    if allowed_policy_versions is not None and grant.policy_version not in set(allowed_policy_versions):
        failures.append(f"delegation policy version {grant.policy_version!r} is not allowed")
    return DelegationAttenuationProof(
        grant=grant,
        passed=not failures,
        delegated_scopes=delegated,
        uncovered_scopes=uncovered,
        source_scope_count=len(source),
        provenance_id=grant.provenance_id,
        failures=tuple(failures),
    )


__all__ = [
    "DelegationAttenuationProof",
    "DelegationGrant",
    "prove_delegation_attenuation",
]
