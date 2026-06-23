"""Authority graph, role, and closure helpers."""

from __future__ import annotations

from typing import Iterable, Mapping

from tigrbl_identity_contracts.authority import (
    AuthorityClosure,
    AuthorityEdge,
    AuthorityGraphIntegrityReport,
    AuthorityMonotonicityReport,
    AuthorityMutationKind,
    AuthorityNode,
    AuthorityPath,
    AuthorityReachabilityProof,
    AuthorityRole,
    AuthorityScope,
    LeastAuthorityDiff,
    authority_matches,
)


def normalize_authority_roles(values: Iterable[str | AuthorityRole] = ()) -> tuple[str, ...]:
    normalized = {str(value.value if isinstance(value, AuthorityRole) else value).strip() for value in values}
    normalized.discard("")
    return tuple(sorted(normalized))


def has_admin_authority(values: Iterable[str | AuthorityRole] = (), *, principal_kind: str | None = None) -> bool:
    roles = normalize_authority_roles(values)
    return AuthorityRole.ADMIN.value in roles or principal_kind == AuthorityRole.ADMIN.value


def has_owner_authority(values: Iterable[str | AuthorityRole] = ()) -> bool:
    return AuthorityRole.OWNER.value in normalize_authority_roles(values)


def has_superuser_authority(values: Iterable[str | AuthorityRole] = ()) -> bool:
    return AuthorityRole.SUPERUSER.value in normalize_authority_roles(values)


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
        stack: list[tuple[str, tuple[str, ...], tuple[AuthorityScope, ...], tuple[str, ...]]] = [
            (subject, (), (), (subject,))
        ]
        while stack:
            node_id, edge_ids, inherited_scopes, node_path = stack.pop()
            for edge in reversed(self.outgoing(node_id)):
                edge_scopes = (
                    edge.scopes
                    if not inherited_scopes
                    else tuple(
                        scope
                        for scope in edge.scopes
                        if any(parent.covers(scope) for parent in inherited_scopes)
                    )
                )
                if not edge_scopes:
                    continue
                next_edge_ids = edge_ids + (edge.edge_id,)
                path = AuthorityPath(
                    subject=subject,
                    target=edge.target,
                    edge_ids=next_edge_ids,
                    scopes=edge_scopes,
                )
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
        return AuthorityReachabilityProof(
            subject=subject,
            requested=requested,
            reachable=bool(paths),
            paths=paths,
            failures=failures,
        )


def validate_authority_graph_integrity(graph: AuthorityDerivationGraph) -> AuthorityGraphIntegrityReport:
    semantic_versions: dict[tuple[str, str, tuple[tuple[str, str, str, str], ...]], set[str]] = {}
    failures: list[str] = []
    for edge in graph.edges.values():
        semantic_key = (edge.source, edge.target, tuple(scope.key for scope in edge.scopes))
        semantic_versions.setdefault(semantic_key, set()).add(edge.policy_version)
        for scope in edge.scopes:
            source = graph.nodes[edge.source]
            target = graph.nodes[edge.target]
            if source.tenant_id and scope.tenant_id != source.tenant_id:
                failures.append(f"edge {edge.edge_id!r} scope crosses source tenant {source.tenant_id!r}")
            if target.tenant_id and scope.tenant_id != target.tenant_id:
                failures.append(f"edge {edge.edge_id!r} scope crosses target tenant {target.tenant_id!r}")
    for (source, target, _scopes), versions in semantic_versions.items():
        non_empty_versions = {version for version in versions if version}
        if len(non_empty_versions) > 1:
            failures.append(f"conflicting policy versions for edge {source!r}->{target!r}")
    return AuthorityGraphIntegrityReport(
        passed=not failures,
        failures=tuple(sorted(set(failures))),
        checked_edge_count=len(graph.edges),
    )


def compute_authority_closure(graph: AuthorityDerivationGraph, subject: str) -> AuthorityClosure:
    try:
        paths = graph.derive_paths(subject)
    except KeyError:
        paths = ()
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
    "AuthorityDerivationGraph",
    "AuthorityEdge",
    "AuthorityGraphIntegrityReport",
    "AuthorityMonotonicityReport",
    "AuthorityMutationKind",
    "AuthorityNode",
    "AuthorityPath",
    "AuthorityReachabilityProof",
    "AuthorityRole",
    "AuthorityScope",
    "LeastAuthorityDiff",
    "authority_matches",
    "compare_authority_monotonicity",
    "compute_authority_closure",
    "diff_least_authority",
    "has_admin_authority",
    "has_owner_authority",
    "has_superuser_authority",
    "normalize_authority_roles",
    "validate_authority_graph_integrity",
]
