import pytest

from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.security.certification import (
    CapabilityRecord,
    CertificationError,
    runtime_capability_truth,
)
from tigrbl_auth.security.runtime_metadata import (
    build_capability_attestation,
    runtime_truth_manifest,
)


def test_runtime_capability_truth_t0_contract_exports_runtime_check() -> None:
    assert callable(runtime_capability_truth)


def test_runtime_capability_truth_t1_accepts_evidence_backed_advertising() -> None:
    truth = runtime_capability_truth(
        (
            CapabilityRecord("jwks", True, "evd:jwks"),
            CapabilityRecord("admin", False),
        ),
        advertised={"jwks"},
    )

    assert truth == {"jwks": True, "admin": False}


def test_runtime_capability_truth_t2_rejects_disabled_or_unknown_advertising() -> None:
    configured = (CapabilityRecord("jwks", False, "evd:jwks"),)

    with pytest.raises(CertificationError, match="disabled capability"):
        runtime_capability_truth(configured, advertised={"jwks"})

    with pytest.raises(CertificationError, match="unknown"):
        runtime_capability_truth(configured, advertised={"token"})


def test_runtime_derived_metadata_t1_projects_enabled_resource_validation_surface() -> None:
    deployment = resolve_deployment(
        profile="production",
        product_surface="resource-validation-app",
    )

    manifest = runtime_truth_manifest(deployment)

    assert manifest["product_surface"] == "resource-validation-app"
    assert "introspection" in manifest["capabilities"]
    assert "jwks" in manifest["capabilities"]
    assert "token" not in manifest["capabilities"]
    assert "/introspect" in {row["path"] for row in manifest["routes"]}
    assert all(row["evidence_id"] for row in manifest["capabilities"].values())


def test_capability_attestation_t2_is_deterministic_and_evidence_backed() -> None:
    deployment = resolve_deployment(
        profile="production",
        product_surface="resource-validation-app",
    )

    first = build_capability_attestation(
        deployment,
        generated_at="2026-06-01T00:00:00+00:00",
        claim_ids=("clm:runtime-capability-truth.t2",),
    )
    second = build_capability_attestation(
        deployment,
        generated_at="2026-06-01T00:00:00+00:00",
        claim_ids=("clm:runtime-capability-truth.t2",),
    )

    assert first.artifact_sha256 == second.artifact_sha256
    assert first.evidence_ids
    assert all(item.startswith("evd:runtime-capability:") for item in first.evidence_ids)
