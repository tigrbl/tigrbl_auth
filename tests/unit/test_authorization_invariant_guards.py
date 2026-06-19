from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
root_value = str(ROOT)
if root_value not in sys.path:
    sys.path.insert(0, root_value)
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.append(value)

from tigrbl_auth.services.policy_invariants import (
    AuthorizationInvariant as FacadeAuthorizationInvariant,
    InvariantRegistry as FacadeInvariantRegistry,
)
from tigrbl_authz_policy import (
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantRegistry,
    InvariantSeverity,
    VerificationMethod,
    default_authorization_invariant_registry,
)


def test_authorization_invariant_registry_t0_exports_public_surfaces() -> None:
    assert FacadeAuthorizationInvariant is AuthorizationInvariant
    assert FacadeInvariantRegistry is InvariantRegistry
    assert VerificationMethod.GRAPH.value == "graph"
    assert InvariantSeverity.CRITICAL.value == "critical"


def test_authorization_invariant_registry_t1_registers_lists_and_evaluates() -> None:
    invariant = AuthorizationInvariant(
        invariant_id="authz.scope.non_persistence",
        title="Removed authority cannot reappear",
        property_family="safety",
        statement="Removed authority must not reappear without a later explicit grant.",
        verification_method=VerificationMethod.REPLAY,
        severity=InvariantSeverity.CRITICAL,
        feature_ids=("feat:authorization-invariant-guard-registry",),
        spec_ids=("spc:1205",),
        tags=("revocation", "authority"),
    )
    registry = InvariantRegistry((invariant,))

    assert registry.get("authz.scope.non_persistence") is invariant
    assert registry.list(property_family="safety", tags=("authority",)) == (invariant,)
    assert registry.list(enabled_only=True) == (invariant,)

    evaluation = registry.evaluate(
        "authz.scope.non_persistence",
        lambda item: InvariantEvaluation(
            invariant_id=item.invariant_id,
            passed=True,
            message="replay accepted",
            evaluated_at="2026-06-07T00:00:00+00:00",
            evidence={"trace": "decision-key"},
        ),
    )

    assert evaluation.passed is True
    assert evaluation.evidence["trace"] == "decision-key"
    assert registry.violations((evaluation,)) == ()


def test_authorization_invariant_registry_t1_default_registry_tracks_seed_invariants() -> None:
    registry = default_authorization_invariant_registry()
    invariant_ids = tuple(item.invariant_id for item in registry.list(enabled_only=True))

    assert invariant_ids == ("authz.non_escalation", "authz.tenant_isolation")
    assert registry.get("authz.non_escalation").spec_ids == ("spc:1205", "spc:1206", "spc:1207")
    assert registry.get("authz.tenant_isolation").severity is InvariantSeverity.CRITICAL


def test_authorization_invariant_registry_t2_fails_closed_for_bad_definitions() -> None:
    registry = InvariantRegistry()
    invariant = AuthorizationInvariant(
        invariant_id="authz.tenant.no_leakage",
        title="Tenant authority cannot leak",
        property_family="isolation",
        statement="Authority derived in one tenant cannot leak to another.",
        verification_method="runtime",
        tags=("tenant", "tenant"),
    )
    registry.register(invariant)

    with pytest.raises(ValueError, match="duplicate invariant"):
        registry.register(invariant)
    with pytest.raises(ValueError, match="statement is required"):
        AuthorizationInvariant(
            invariant_id="authz.bad",
            title="Bad",
            property_family="safety",
            statement="",
            verification_method=VerificationMethod.STATIC,
        )
    with pytest.raises(KeyError, match="unknown invariant"):
        registry.get("authz.missing")


def test_authorization_invariant_registry_t2_reports_violations_and_rejects_mismatched_evaluation() -> None:
    invariant = AuthorizationInvariant(
        invariant_id="authz.delegation.attenuated",
        title="Delegation is attenuated",
        property_family="safety",
        statement="Delegated authority must be bounded by source authority.",
        verification_method=VerificationMethod.GRAPH,
    )
    registry = InvariantRegistry((invariant,))

    failed = registry.evaluate("authz.delegation.attenuated", lambda _item: False)
    violations = registry.violations((failed,))

    assert failed.passed is False
    assert violations[0].invariant_id == "authz.delegation.attenuated"
    assert violations[0].severity is InvariantSeverity.ERROR

    with pytest.raises(ValueError, match="evaluation invariant_id mismatch"):
        registry.evaluate(
            "authz.delegation.attenuated",
            lambda _item: InvariantEvaluation(
                invariant_id="authz.other",
                passed=True,
                message="wrong id",
                evaluated_at="2026-06-07T00:00:00+00:00",
            ),
        )
