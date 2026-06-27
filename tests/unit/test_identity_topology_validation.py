from __future__ import annotations

from types import SimpleNamespace

from tigrbl_identity_contracts.topology import IDENTITY_TOPOLOGY_SCENARIOS
from tigrbl_identity_storage_runtime.topology_validation import (
    IdentityTopologySnapshot,
    validate_identity_topology_snapshot,
)


def _record(**values):
    return SimpleNamespace(**values)


def _scenario_snapshot(scenario_id: int) -> IdentityTopologySnapshot:
    scenario = IDENTITY_TOPOLOGY_SCENARIOS[scenario_id - 1]
    realm_count = 1 if scenario.realm == "single" else 2
    tenant_count = 1 if scenario.tenant == "single" else 2
    identity_count = 1 if scenario.identities == "single" else 2

    realms = tuple(_record(id=f"realm-{index}") for index in range(realm_count))
    tenants = tuple(
        _record(id=f"tenant-{index}", realm_id=realms[index % realm_count].id)
        for index in range(tenant_count)
    )
    principals = tuple(
        _record(
            id=f"principal-{index}",
            subject=f"subject:{index}",
            tenant_id=tenants[index % tenant_count].id,
            realm_id=tenants[index % tenant_count].realm_id,
        )
        for index in range(identity_count)
    )

    memberships = []
    if scenario.tenant == "multi" and scenario.identities == "single":
        memberships.extend(
            _record(tenant_id=tenant.id, principal_id=principals[0].id, status="active")
            for tenant in tenants
        )
    else:
        memberships.extend(
            _record(
                tenant_id=tenants[index % tenant_count].id,
                principal_id=principal.id,
                status="active",
            )
            for index, principal in enumerate(principals)
        )

    return IdentityTopologySnapshot(
        realms=realms,
        tenants=tenants,
        principals=principals,
        tenant_memberships=tuple(memberships),
    )


def test_identity_topology_validator_accepts_all_declared_scenarios() -> None:
    for scenario in IDENTITY_TOPOLOGY_SCENARIOS:
        report = validate_identity_topology_snapshot(_scenario_snapshot(scenario.id), scenario.id)
        assert report.passed, (scenario.id, report.failures)
        assert report.observed.realm == scenario.realm
        assert report.observed.tenant == scenario.tenant
        assert report.observed.identities == scenario.identities


def test_identity_topology_validator_rejects_wrong_cardinality() -> None:
    report = validate_identity_topology_snapshot(_scenario_snapshot(2), 1)

    assert not report.passed
    assert "identities cardinality expected single, observed multi (2)" in report.failures


def test_identity_topology_validator_rejects_unknown_references() -> None:
    snapshot = IdentityTopologySnapshot(
        realms=(_record(id="realm-a"),),
        tenants=(_record(id="tenant-a", realm_id="realm-missing"),),
        principals=(_record(id="principal-a", tenant_id="tenant-missing", realm_id="realm-missing"),),
    )

    report = validate_identity_topology_snapshot(snapshot, 1)

    assert not report.passed
    assert "tenants reference unknown realms: ['realm-missing']" in report.failures
    assert "identities reference unknown tenants: ['tenant-missing']" in report.failures
    assert "identities reference unknown realms: ['realm-missing']" in report.failures


def test_identity_topology_validator_rejects_ambiguous_multi_realm_tenant() -> None:
    snapshot = IdentityTopologySnapshot(
        realms=(_record(id="realm-a"), _record(id="realm-b")),
        tenants=(_record(id="tenant-a", realm_id=None),),
        principals=(_record(id="principal-a", tenant_id="tenant-a"),),
    )

    report = validate_identity_topology_snapshot(snapshot, 5)

    assert not report.passed
    assert "multi-realm topology has tenants without realm_id: ['tenant-a']" in report.failures


def test_identity_topology_validator_rejects_multi_tenant_without_identity_bindings() -> None:
    snapshot = IdentityTopologySnapshot(
        realms=(_record(id="realm-a"),),
        tenants=(
            _record(id="tenant-a", realm_id="realm-a"),
            _record(id="tenant-b", realm_id="realm-a"),
        ),
        principals=(_record(id="principal-a", tenant_id="tenant-a", realm_id="realm-a"),),
    )

    report = validate_identity_topology_snapshot(snapshot, 3)

    assert not report.passed
    assert "multi-tenant topology must bind identities to at least two tenants" in report.failures
