from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .authority_graph import AuthorityScope


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
) -> DelegationAttenuationProof:
    source = tuple(source_scopes)
    delegated = grant.scopes()
    uncovered = tuple(scope for scope in delegated if not any(source_scope.covers(scope) for source_scope in source))
    failures = tuple(
        f"delegated scope {scope.action!r} on {scope.resource!r} is not covered in tenant {scope.tenant_id!r}"
        for scope in uncovered
    )
    return DelegationAttenuationProof(
        grant=grant,
        passed=not uncovered,
        delegated_scopes=delegated,
        uncovered_scopes=uncovered,
        source_scope_count=len(source),
        provenance_id=grant.provenance_id,
        failures=failures,
    )


__all__ = [
    "DelegationAttenuationProof",
    "DelegationGrant",
    "prove_delegation_attenuation",
]
