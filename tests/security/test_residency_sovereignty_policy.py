from __future__ import annotations

from tigrbl_authz_policy import (
    ResidencyZone,
    TenantResidencyRecord,
    assert_residency_access,
    evaluate_residency_access,
    residency_policy_manifest,
)


def _record() -> TenantResidencyRecord:
    return TenantResidencyRecord(
        tenant_id="tenant-eu",
        realm="realm-a",
        residency_zone=ResidencyZone(
            zone_id="eu-sovereign",
            jurisdictions=("eu-central", "eu-west"),
            sovereign_controls=("eu-only-processor",),
        ),
        allowed_processing_regions=("eu-central", "eu-west"),
        restricted_transfer_regions=("us-east",),
    )


def test_residency_sovereignty_t0_exports_policy_surface() -> None:
    assert callable(evaluate_residency_access)
    assert callable(assert_residency_access)
    assert callable(residency_policy_manifest)


def test_residency_sovereignty_t1_allows_declared_region_and_reports_manifest() -> None:
    record = _record()

    decision = assert_residency_access(
        record,
        tenant_id="tenant-eu",
        realm="realm-a",
        processing_region="eu-central",
    )
    manifest = residency_policy_manifest((record,))

    assert decision.allowed is True
    assert decision.transfer_required is False
    assert decision.reasons == ("processing region is inside allowed residency boundary",)
    assert manifest["tenants"] == [
        {
            "tenant_id": "tenant-eu",
            "realm": "realm-a",
            "residency_zone": "eu-sovereign",
            "allowed_processing_regions": ["eu-central", "eu-west"],
            "restricted_transfer_regions": ["us-east"],
            "sovereign_controls": ["eu-only-processor"],
        }
    ]
