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
    AuthorizationInvariantTable as FacadeAuthorizationInvariantTable,
)
from tigrbl_identity_contracts.invariants import (
    AuthorizationInvariant as ContractAuthorizationInvariant,
    InvariantEvaluation,
    InvariantSeverity,
    VerificationMethod,
)
from tigrbl_identity_storage.tables import (
    AuthorizationInvariant as StorageAuthorizationInvariant,
    InvariantEvaluation as StorageInvariantEvaluation,
    InvariantViolation as StorageInvariantViolation,
)
from tigrbl_authz_policy import (
    AuthorizationInvariant,
    AuthorizationInvariantTable,
    InvariantEvaluationTable,
    InvariantViolationTable,
)


def test_authorization_invariant_tables_t0_export_public_surfaces() -> None:
    assert AuthorizationInvariant is ContractAuthorizationInvariant
    assert AuthorizationInvariantTable is StorageAuthorizationInvariant
    assert InvariantEvaluationTable is StorageInvariantEvaluation
    assert InvariantViolationTable is StorageInvariantViolation
    assert FacadeAuthorizationInvariantTable is AuthorizationInvariantTable
    assert VerificationMethod.GRAPH.value == "graph"
    assert InvariantSeverity.CRITICAL.value == "critical"


def test_authorization_invariant_contract_t1_normalizes_definition_metadata() -> None:
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
    evaluation = InvariantEvaluation(
        invariant_id=invariant.invariant_id,
        passed=True,
        message="replay accepted",
        evaluated_at="2026-06-07T00:00:00+00:00",
        evidence={"trace": "decision-key"},
    )

    assert invariant.feature_ids == ("feat:authorization-invariant-guard-registry",)
    assert invariant.tags == ("authority", "revocation")
    assert evaluation.evidence["trace"] == "decision-key"


def test_authorization_invariant_contract_t2_fails_closed_for_bad_definitions() -> None:
    valid = AuthorizationInvariant(
        invariant_id="authz.tenant.no_leakage",
        title="Tenant authority cannot leak",
        property_family="isolation",
        statement="Authority derived in one tenant cannot leak to another.",
        verification_method="runtime",
        tags=("tenant", "tenant"),
    )

    assert valid.verification_method is VerificationMethod.RUNTIME
    assert valid.tags == ("tenant",)
    with pytest.raises(ValueError, match="statement is required"):
        AuthorizationInvariant(
            invariant_id="authz.bad",
            title="Bad",
            property_family="safety",
            statement="",
            verification_method=VerificationMethod.STATIC,
        )


def test_authorization_invariant_tables_t2_materialize_table_rows() -> None:
    invariant = AuthorizationInvariantTable(
        invariant_id="authz.delegation.attenuated",
        title="Delegation is attenuated",
        property_family="safety",
        statement="Delegated authority must be bounded by source authority.",
        verification_method=VerificationMethod.GRAPH.value,
    )
    failed = InvariantEvaluationTable(
        invariant_id="authz.delegation.attenuated",
        passed=False,
        message="effective authority exceeded closure",
        evaluated_at="2026-06-07T00:00:00+00:00",
    )
    violation = InvariantViolationTable(
        invariant_id=failed.invariant_id,
        severity=InvariantSeverity.ERROR.value,
        message=failed.message,
    )

    assert invariant.invariant_id == "authz.delegation.attenuated"
    assert failed.passed is False
    assert violation.message == "effective authority exceeded closure"
