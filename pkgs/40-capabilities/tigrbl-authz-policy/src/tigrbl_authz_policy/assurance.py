"""Authorization assurance, replay, correctness, and liveness helpers."""

from __future__ import annotations

from typing import Iterable, Mapping

from tigrbl_identity_core.json_canonicalization import canonical_hash, canonical_json
from tigrbl_authz_policy_invariant_registry import (
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantRegistry,
    InvariantSeverity,
    InvariantViolation,
    VerificationMethod,
    default_authorization_invariant_registry,
)
from tigrbl_identity_contracts.correctness import (
    AuthorizationReference,
    ControlPlaneCorrectnessReport,
    CorrectnessProofSection,
    IntegrityReport,
    ReferenceCatalog,
    SafetyPropertyResult,
    TenantRealmIsolationReport,
    TrustEdge,
)
from tigrbl_identity_contracts.liveness import (
    ConvergenceEvent,
    ConvergenceState,
    LivenessConvergenceReport,
)
from tigrbl_identity_contracts.replay import (
    DecisionStabilityChange,
    DecisionStabilityReport,
    PolicyDeterminismReport,
    PolicyEvaluator,
    PolicyReplayCase,
    PolicyReplayResult,
)

from tigrbl_authz_policy_authority_derivation_graph import AuthorityDerivationGraph


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


def build_control_plane_correctness_report(
    *,
    report_id: str,
    sections: Iterable[CorrectnessProofSection],
    required_section_ids: Iterable[str] = (),
) -> ControlPlaneCorrectnessReport:
    rows = tuple(sorted(sections, key=lambda section: section.section_id))
    present_section_ids = {section.section_id for section in rows}
    missing_sections = tuple(sorted(set(required_section_ids) - present_section_ids))
    failures = tuple(
        [
            *(f"missing required proof section: {section_id}" for section_id in missing_sections),
            *(("report has no proof sections",) if not rows else ()),
            *(
                failure
                for section in rows
                for failure in (
                    (f"{section.section_id}: {item}" for item in section.failures)
                    if not section.passed
                    else ()
                )
            ),
        ]
    )
    return ControlPlaneCorrectnessReport(
        report_id=report_id,
        passed=not failures,
        sections=rows,
        failures=failures,
    )


def replay_policy_determinism(
    *,
    policy_version: str,
    cases: tuple[PolicyReplayCase, ...],
    evaluator: PolicyEvaluator,
    runs: int = 2,
    schema_version: str = "",
) -> PolicyDeterminismReport:
    if runs < 2:
        raise ValueError("runs must be at least 2")
    results: list[PolicyReplayResult] = []
    failures: list[str] = []
    for case in cases:
        decisions = tuple(dict(evaluator(case.request)) for _ in range(runs))
        decision_hashes = tuple(canonical_hash(decision) for decision in decisions)
        stable = len(set(decision_hashes)) == 1
        if not stable:
            failures.append(f"case {case.case_id!r} produced non-deterministic decisions")
        results.append(
            PolicyReplayResult(
                case_id=case.case_id,
                request_hash=canonical_hash(case.request),
                decision_hashes=decision_hashes,
                stable=stable,
                decisions=decisions,
            )
        )
    return PolicyDeterminismReport(
        passed=not failures,
        policy_version=policy_version,
        schema_version=schema_version,
        results=tuple(results),
        failures=tuple(failures),
    )


def compare_policy_version_decisions(
    *,
    baseline_version: str,
    candidate_version: str,
    cases: tuple[PolicyReplayCase, ...],
    baseline_evaluator: PolicyEvaluator,
    candidate_evaluator: PolicyEvaluator,
    allowed_change_reasons: Mapping[str, str] = {},
    baseline_schema_version: str = "",
    candidate_schema_version: str = "",
) -> DecisionStabilityReport:
    changes: list[DecisionStabilityChange] = []
    failures: list[str] = []
    for case in cases:
        baseline_hash = canonical_hash(baseline_evaluator(case.request))
        candidate_hash = canonical_hash(candidate_evaluator(case.request))
        if baseline_hash == candidate_hash:
            continue
        reason = allowed_change_reasons.get(case.case_id, "")
        attributed = bool(reason and baseline_version != candidate_version)
        if not attributed:
            failures.append(f"case {case.case_id!r} changed without policy-version attribution")
        changes.append(
            DecisionStabilityChange(
                case_id=case.case_id,
                baseline_hash=baseline_hash,
                candidate_hash=candidate_hash,
                attributed=attributed,
                reason=reason,
            )
        )
    return DecisionStabilityReport(
        passed=not failures,
        baseline_version=baseline_version,
        candidate_version=candidate_version,
        baseline_schema_version=baseline_schema_version,
        candidate_schema_version=candidate_schema_version,
        changes=tuple(changes),
        failures=tuple(failures),
    )


def evaluate_liveness_convergence(events: tuple[ConvergenceEvent, ...]) -> LivenessConvergenceReport:
    by_id = {event.event_id: event for event in events}
    rows = tuple(by_id[event_id] for event_id in sorted(by_id))
    converged = tuple(event for event in rows if event.state is ConvergenceState.CONVERGED)
    pending = tuple(event for event in rows if event.state is ConvergenceState.PENDING)
    late = tuple(event for event in rows if event.state is ConvergenceState.LATE)
    failures = tuple(
        [*(f"mutation {event.mutation_id!r} is pending convergence" for event in pending)]
        + [*(f"mutation {event.mutation_id!r} converged after its expected window" for event in late)]
    )
    return LivenessConvergenceReport(
        passed=not failures,
        converged=converged,
        pending=pending,
        late=late,
        failures=failures,
    )


__all__ = [
    "AuthorizationInvariant",
    "AuthorizationReference",
    "AuthorizationSafetyPropertyEvaluator",
    "ControlPlaneCorrectnessReport",
    "ConvergenceEvent",
    "ConvergenceState",
    "CorrectnessProofSection",
    "DecisionStabilityChange",
    "DecisionStabilityReport",
    "IntegrityReport",
    "InvariantEvaluation",
    "InvariantRegistry",
    "InvariantSeverity",
    "InvariantViolation",
    "LivenessConvergenceReport",
    "PolicyDeterminismReport",
    "PolicyReplayCase",
    "PolicyReplayResult",
    "ReferenceCatalog",
    "SafetyPropertyResult",
    "TenantRealmIsolationReport",
    "TrustEdge",
    "VerificationMethod",
    "build_control_plane_correctness_report",
    "canonical_hash",
    "canonical_json",
    "compare_policy_version_decisions",
    "default_authorization_invariant_registry",
    "evaluate_liveness_convergence",
    "replay_policy_determinism",
    "validate_authorization_referential_integrity",
    "validate_tenant_realm_isolation",
    "validate_trust_graph_integrity",
]
