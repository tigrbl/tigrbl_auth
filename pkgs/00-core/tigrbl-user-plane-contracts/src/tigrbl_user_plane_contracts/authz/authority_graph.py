from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


def _stable_tuple(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if str(value)}))


def authority_matches(grant: str, requested: str) -> bool:
    if grant == "*" or grant == requested:
        return True
    if grant.endswith(".*"):
        prefix = grant[:-2]
        return requested == prefix or requested.startswith(f"{prefix}.")
    return False


@dataclass(frozen=True, slots=True)
class AuthorityScope:
    tenant_id: str
    action: str
    resource: str = "*"
    realm: str = ""

    def __post_init__(self) -> None:
        if not self.tenant_id:
            raise ValueError("tenant_id is required")
        if not self.action:
            raise ValueError("action is required")
        object.__setattr__(self, "resource", self.resource or "*")

    def covers(self, requested: "AuthorityScope") -> bool:
        realm_ok = not self.realm or not requested.realm or self.realm == requested.realm
        return (
            self.tenant_id == requested.tenant_id
            and realm_ok
            and authority_matches(self.action, requested.action)
            and authority_matches(self.resource, requested.resource)
        )

    @property
    def key(self) -> tuple[str, str, str, str]:
        return (self.tenant_id, self.realm, self.action, self.resource)


@dataclass(frozen=True, slots=True)
class AuthorityNode:
    node_id: str
    kind: str
    tenant_id: str = ""
    realm: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("node_id is required")
        if not self.kind:
            raise ValueError("kind is required")
        object.__setattr__(self, "attributes", dict(self.attributes))


@dataclass(frozen=True, slots=True)
class AuthorityEdge:
    edge_id: str
    source: str
    target: str
    edge_type: str
    scopes: tuple[AuthorityScope, ...]
    policy_version: str = ""
    provenance_id: str = ""
    constraints: tuple[str, ...] = ()
    active: bool = True

    def __post_init__(self) -> None:
        if not self.edge_id:
            raise ValueError("edge_id is required")
        if not self.source or not self.target:
            raise ValueError("source and target are required")
        if not self.edge_type:
            raise ValueError("edge_type is required")
        if not self.scopes:
            raise ValueError("at least one authority scope is required")
        object.__setattr__(self, "scopes", tuple(sorted(self.scopes, key=lambda item: item.key)))
        object.__setattr__(self, "constraints", _stable_tuple(self.constraints))


@dataclass(frozen=True, slots=True)
class AuthorityPath:
    subject: str
    target: str
    edge_ids: tuple[str, ...]
    scopes: tuple[AuthorityScope, ...]


@dataclass(frozen=True, slots=True)
class AuthorityReachabilityProof:
    subject: str
    requested: AuthorityScope
    reachable: bool
    paths: tuple[AuthorityPath, ...]
    failures: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AuthorityGraphIntegrityReport:
    passed: bool
    failures: tuple[str, ...]
    checked_edge_count: int


__all__ = [
    "AuthorityEdge",
    "AuthorityGraphIntegrityReport",
    "AuthorityNode",
    "AuthorityPath",
    "AuthorityReachabilityProof",
    "AuthorityScope",
    "authority_matches",
]
