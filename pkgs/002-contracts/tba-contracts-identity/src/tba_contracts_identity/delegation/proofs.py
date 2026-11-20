from __future__ import annotations

from dataclasses import dataclass

from ..authority import AuthorityScope


@dataclass(frozen=True, slots=True)
class DelegationGrantSpec:
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
        object.__setattr__(
            self, "resources", tuple(sorted(set(self.resources or ("*",))))
        )

    def scopes(self) -> tuple[AuthorityScope, ...]:
        return tuple(
            AuthorityScope(
                tenant_id=tenant_id, realm=self.realm, action=action, resource=resource
            )
            for tenant_id in self.tenant_ids
            for action in self.actions
            for resource in self.resources
        )


@dataclass(frozen=True, slots=True)
class DelegationAttenuationProof:
    grant: DelegationGrantSpec
    passed: bool
    delegated_scopes: tuple[AuthorityScope, ...]
    uncovered_scopes: tuple[AuthorityScope, ...]
    source_scope_count: int
    provenance_id: str = ""
    failures: tuple[str, ...] = ()


__all__ = [
    "DelegationAttenuationProof",
    "DelegationGrantSpec",
]
