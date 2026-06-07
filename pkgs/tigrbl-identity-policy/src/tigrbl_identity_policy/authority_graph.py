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


class AuthorityDerivationGraph:
    def __init__(
        self,
        *,
        nodes: Iterable[AuthorityNode] = (),
        edges: Iterable[AuthorityEdge] = (),
    ) -> None:
        self._nodes: dict[str, AuthorityNode] = {}
        self._edges: dict[str, AuthorityEdge] = {}
        for node in nodes:
            self.add_node(node)
        for edge in edges:
            self.add_edge(edge)

    @property
    def nodes(self) -> Mapping[str, AuthorityNode]:
        return dict(self._nodes)

    @property
    def edges(self) -> Mapping[str, AuthorityEdge]:
        return dict(self._edges)

    def add_node(self, node: AuthorityNode) -> AuthorityNode:
        if node.node_id in self._nodes:
            raise ValueError(f"duplicate authority node {node.node_id!r}")
        self._nodes[node.node_id] = node
        return node

    def add_edge(self, edge: AuthorityEdge) -> AuthorityEdge:
        if edge.edge_id in self._edges:
            raise ValueError(f"duplicate authority edge {edge.edge_id!r}")
        if edge.source not in self._nodes:
            raise KeyError(f"unknown authority edge source {edge.source!r}")
        if edge.target not in self._nodes:
            raise KeyError(f"unknown authority edge target {edge.target!r}")
        self._edges[edge.edge_id] = edge
        return edge

    def outgoing(self, node_id: str) -> tuple[AuthorityEdge, ...]:
        return tuple(
            sorted(
                (edge for edge in self._edges.values() if edge.source == node_id and edge.active),
                key=lambda edge: edge.edge_id,
            )
        )

    def derive_paths(self, subject: str) -> tuple[AuthorityPath, ...]:
        if subject not in self._nodes:
            raise KeyError(f"unknown authority subject {subject!r}")
        paths: list[AuthorityPath] = []
        stack: list[tuple[str, tuple[str, ...], tuple[AuthorityScope, ...], tuple[str, ...]]] = [(subject, (), (), (subject,))]
        while stack:
            node_id, edge_ids, inherited_scopes, node_path = stack.pop()
            for edge in reversed(self.outgoing(node_id)):
                edge_scopes = edge.scopes if not inherited_scopes else tuple(
                    scope for scope in edge.scopes if any(parent.covers(scope) for parent in inherited_scopes)
                )
                if not edge_scopes:
                    continue
                next_edge_ids = edge_ids + (edge.edge_id,)
                path = AuthorityPath(subject=subject, target=edge.target, edge_ids=next_edge_ids, scopes=edge_scopes)
                paths.append(path)
                if edge.target not in node_path:
                    stack.append((edge.target, next_edge_ids, edge_scopes, node_path + (edge.target,)))
        return tuple(sorted(paths, key=lambda path: (path.target, path.edge_ids)))

    def effective_scopes(self, subject: str) -> tuple[AuthorityScope, ...]:
        scopes = {scope.key: scope for path in self.derive_paths(subject) for scope in path.scopes}
        return tuple(scopes[key] for key in sorted(scopes))

    def prove_reachability(self, subject: str, requested: AuthorityScope) -> AuthorityReachabilityProof:
        paths = tuple(
            path
            for path in self.derive_paths(subject)
            if any(scope.covers(requested) for scope in path.scopes)
        )
        failures = () if paths else (f"{subject!r} cannot reach {requested.action!r} in tenant {requested.tenant_id!r}",)
        return AuthorityReachabilityProof(subject=subject, requested=requested, reachable=bool(paths), paths=paths, failures=failures)


__all__ = [
    "AuthorityDerivationGraph",
    "AuthorityEdge",
    "AuthorityNode",
    "AuthorityPath",
    "AuthorityReachabilityProof",
    "AuthorityScope",
    "authority_matches",
]
