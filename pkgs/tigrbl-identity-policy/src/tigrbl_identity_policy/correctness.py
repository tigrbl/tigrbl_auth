from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping

from .authority_graph import AuthorityDerivationGraph
from .invariants import InvariantEvaluation, InvariantRegistry


@dataclass(frozen=True, slots=True)
class SafetyPropertyResult:
    passed: bool
    evaluations: tuple[InvariantEvaluation, ...]
    failures: tuple[str, ...]


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


@dataclass(frozen=True, slots=True)
class ReferenceCatalog:
    subjects: tuple[str, ...] = ()
    tenants: tuple[str, ...] = ()
    realms: tuple[str, ...] = ()
    policies: tuple[str, ...] = ()
    delegations: tuple[str, ...] = ()
    trust_domains: tuple[str, ...] = ()
    authority_nodes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("subjects", "tenants", "realms", "policies", "delegations", "trust_domains", "authority_nodes"):
            object.__setattr__(self, field_name, tuple(sorted(set(getattr(self, field_name)))))


@dataclass(frozen=True, slots=True)
class AuthorizationReference:
    ref_id: str
    ref_type: str
    target_id: str
    source_id: str = ""

    def __post_init__(self) -> None:
        if not self.ref_id or not self.ref_type or not self.target_id:
            raise ValueError("ref_id, ref_type, and target_id are required")


@dataclass(frozen=True, slots=True)
class IntegrityReport:
    passed: bool
    failures: tuple[str, ...]
    checked_count: int


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
    }
    rows = tuple(references)
    failures = tuple(
        f"{row.ref_id} references unknown {row.ref_type} {row.target_id!r}"
        for row in rows
        if row.ref_type not in known or row.target_id not in known[row.ref_type]
    )
    return IntegrityReport(passed=not failures, failures=failures, checked_count=len(rows))


@dataclass(frozen=True, slots=True)
class TrustEdge:
    edge_id: str
    issuer: str
    subject: str
    tenant_id: str
    trust_domain: str
    revoked: bool = False

    def __post_init__(self) -> None:
        if not self.edge_id or not self.issuer or not self.subject or not self.tenant_id or not self.trust_domain:
            raise ValueError("edge_id, issuer, subject, tenant_id, and trust_domain are required")


def validate_trust_graph_integrity(
    *,
    catalog: ReferenceCatalog,
    edges: Iterable[TrustEdge],
    allow_cycles: bool = False,
) -> IntegrityReport:
    rows = tuple(edges)
    subjects = set(catalog.subjects)
    tenants = set(catalog.tenants)
    domains = set(catalog.trust_domains)
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


@dataclass(frozen=True, slots=True)
class TenantRealmIsolationReport:
    passed: bool
    subject: str
    failures: tuple[str, ...]
    checked_path_count: int
    expected_tenant_id: str = ""
    expected_realm: str = ""


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
