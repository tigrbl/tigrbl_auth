from __future__ import annotations

from typing import Iterable

from tigrbl_identity_contracts.authz.correctness import (
    AuthorizationReference,
    IntegrityReport,
    ReferenceCatalog,
    SafetyPropertyResult,
    TenantRealmIsolationReport,
    TrustEdge,
)
from tigrbl_identity_contracts.authz.invariants import InvariantEvaluation

from .authority_graph import AuthorityDerivationGraph
from .invariants import InvariantRegistry


class AuthorizationSafetyPropertyEvaluator:
    def __init__(self, registry: InvariantRegistry) -> None:
        self.registry = registry

    def evaluate(self, evaluations: Iterable[InvariantEvaluation]) -> SafetyPropertyResult:
        rows = tuple(sorted(evaluations, key=lambda item: item.invariant_id))
        violations = self.registry.violations(rows)
        return SafetyPropertyResult(
            passed=not violations,
            evaluations=rows,
            failures=tuple(violation.message for violation in violations),
        )


def validate_authorization_referential_integrity(
    *,
    catalog: ReferenceCatalog,
    references: Iterable[AuthorizationReference],
) -> IntegrityReport:
    known = {
        "subject": set(catalog.subjects),
        "tenant": set(catalog.tenants),
        "realm": set(catalog.realms),
        "policy": set(catalog.policies),
        "delegation": set(catalog.delegations),
        "trust_domain": set(catalog.trust_domains),
        "authority_node": set(catalog.authority_nodes),
        "provenance": set(catalog.provenance_ids),
        "policy_version": set(catalog.policy_versions),
    }
    rows = tuple(references)
    failures: list[str] = []
    by_ref_id: dict[str, set[str]] = {}
    by_target_id: dict[str, set[str]] = {}
    for row in rows:
        by_ref_id.setdefault(row.ref_id, set()).add(row.ref_type)
        by_target_id.setdefault(row.target_id, set()).add(row.ref_type)
        if row.ref_type not in known or row.target_id not in known[row.ref_type]:
            failures.append(f"{row.ref_id} references unknown {row.ref_type} {row.target_id!r}")
    for ref_id, ref_types in by_ref_id.items():
        if len(ref_types) > 1:
            failures.append(f"reference id {ref_id!r} is reused across incompatible types")
    for target_id, ref_types in by_target_id.items():
        if len(ref_types) > 1:
            failures.append(f"target id {target_id!r} is referenced as incompatible types")
    failures_tuple = tuple(sorted(set(failures)))
    return IntegrityReport(passed=not failures_tuple, failures=failures_tuple, checked_count=len(rows))


def validate_trust_graph_integrity(
    *,
    catalog: ReferenceCatalog,
    edges: Iterable[TrustEdge],
    allow_cycles: bool = False,
    allowed_cross_domain_edges: Iterable[tuple[str, str]] = (),
) -> IntegrityReport:
    rows = tuple(edges)
    subjects = set(catalog.subjects)
    tenants = set(catalog.tenants)
    domains = set(catalog.trust_domains)
    allowed_cross_domain = set(allowed_cross_domain_edges)
    failures: list[str] = []
    adjacency: dict[str, set[str]] = {}
    for edge in rows:
        if edge.revoked:
            failures.append(f"trust edge {edge.edge_id!r} is revoked and cannot be active")
        if edge.issuer not in subjects:
            failures.append(f"trust edge {edge.edge_id!r} has unknown issuer {edge.issuer!r}")
        if edge.subject not in subjects:
            failures.append(f"trust edge {edge.edge_id!r} has unknown subject {edge.subject!r}")
        if edge.tenant_id not in tenants:
            failures.append(f"trust edge {edge.edge_id!r} has unknown tenant {edge.tenant_id!r}")
        if edge.trust_domain not in domains:
            failures.append(f"trust edge {edge.edge_id!r} has unknown trust domain {edge.trust_domain!r}")
        if edge.subject_tenant_id and edge.subject_tenant_id != edge.tenant_id:
            failures.append(f"trust edge {edge.edge_id!r} crosses tenant {edge.tenant_id!r}->{edge.subject_tenant_id!r}")
        if edge.subject_trust_domain:
            if edge.subject_trust_domain not in domains:
                failures.append(f"trust edge {edge.edge_id!r} has unknown subject trust domain {edge.subject_trust_domain!r}")
            if edge.subject_trust_domain != edge.trust_domain and (edge.trust_domain, edge.subject_trust_domain) not in allowed_cross_domain:
                failures.append(f"trust edge {edge.edge_id!r} crosses trust domain {edge.trust_domain!r}->{edge.subject_trust_domain!r}")
        adjacency.setdefault(edge.issuer, set()).add(edge.subject)
    if not allow_cycles:
        for start in adjacency:
            stack = [(start, (start,))]
            while stack:
                node, path = stack.pop()
                for nxt in adjacency.get(node, set()):
                    if nxt == start:
                        failures.append(f"trust graph cycle detected at {start!r}")
                    elif nxt not in path:
                        stack.append((nxt, path + (nxt,)))
    return IntegrityReport(passed=not failures, failures=tuple(sorted(set(failures))), checked_count=len(rows))


def validate_tenant_realm_isolation(
    *,
    graph: AuthorityDerivationGraph,
    subject: str,
    expected_tenant_id: str,
    expected_realm: str = "",
) -> TenantRealmIsolationReport:
    paths = graph.derive_paths(subject)
    failures: list[str] = []
    for path in paths:
        for scope in path.scopes:
            if scope.tenant_id != expected_tenant_id:
                failures.append(f"path {'/'.join(path.edge_ids)} crosses tenant {scope.tenant_id!r}")
            if expected_realm and scope.realm and scope.realm != expected_realm:
                failures.append(f"path {'/'.join(path.edge_ids)} crosses realm {scope.realm!r}")
    return TenantRealmIsolationReport(
        passed=not failures,
        subject=subject,
        failures=tuple(sorted(set(failures))),
        checked_path_count=len(paths),
        expected_tenant_id=expected_tenant_id,
        expected_realm=expected_realm,
    )


__all__ = [
    "AuthorizationReference",
    "AuthorizationSafetyPropertyEvaluator",
    "IntegrityReport",
    "ReferenceCatalog",
    "SafetyPropertyResult",
    "TenantRealmIsolationReport",
    "TrustEdge",
    "validate_authorization_referential_integrity",
    "validate_tenant_realm_isolation",
    "validate_trust_graph_integrity",
]
