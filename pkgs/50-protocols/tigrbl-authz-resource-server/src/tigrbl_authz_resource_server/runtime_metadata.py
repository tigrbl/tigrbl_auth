"""Runtime-derived capability and verifier metadata."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Iterable, Mapping

from tigrbl_identity_runtime.deployment import (
    ROUTE_REGISTRY,
    SURFACE_CAPABILITY_REGISTRY,
    ResolvedDeployment,
    resolve_deployment,
)
from tigrbl_identity_contracts.resource_server import CapabilityAttestation
from tigrbl_authz_policy.certification import (
    CapabilityRecord,
    CertificationError,
    runtime_capability_truth,
)


CAPABILITY_ATTESTATION_VERSION = "tigrbl-auth.capability-attestation.v1"


def _evidence_id(capability: str) -> str:
    return f"evd:runtime-capability:{capability}"


def capability_records_for_deployment(
    deployment: ResolvedDeployment,
) -> tuple[CapabilityRecord, ...]:
    records: list[CapabilityRecord] = []
    for name in sorted(SURFACE_CAPABILITY_REGISTRY):
        meta = SURFACE_CAPABILITY_REGISTRY[name]
        paths = tuple(str(path) for path in meta.get("paths", ()) or ())
        enabled = deployment.capability_enabled(name)
        records.append(
            CapabilityRecord(
                name=name,
                enabled=enabled,
                evidence_id=_evidence_id(name) if enabled else None,
                route=paths[0] if paths else None,
            )
        )
    return tuple(records)


def runtime_truth_manifest(
    deployment: ResolvedDeployment | None = None,
    *,
    advertised_capabilities: Iterable[str] | None = None,
) -> dict[str, Any]:
    active_deployment = deployment or resolve_deployment()
    advertised = tuple(
        advertised_capabilities
        if advertised_capabilities is not None
        else active_deployment.active_capabilities
    )
    records = capability_records_for_deployment(active_deployment)
    truth = runtime_capability_truth(records, advertised)
    active_records = {
        record.name: record
        for record in records
        if truth.get(record.name) and active_deployment.capability_enabled(record.name)
    }
    active_routes = [
        {
            "path": path,
            "methods": list(ROUTE_REGISTRY.get(path, {}).get("methods", ())),
            "capability": ROUTE_REGISTRY.get(path, {}).get("capability"),
            "discovery_visible": bool(
                ROUTE_REGISTRY.get(path, {}).get("discovery_visible", False)
            ),
            "contract_visible": bool(
                ROUTE_REGISTRY.get(path, {}).get("contract_visible", False)
            ),
        }
        for path in active_deployment.active_routes
    ]
    return {
        "product_surface": active_deployment.product_surface,
        "profile": active_deployment.profile,
        "issuer": active_deployment.issuer,
        "protected_resource_identifier": active_deployment.protected_resource_identifier,
        "capabilities": {
            name: {
                "enabled": True,
                "evidence_id": record.evidence_id,
                "route": record.route,
            }
            for name, record in active_records.items()
        },
        "routes": active_routes,
        "active_targets": list(active_deployment.active_targets),
    }


def assert_runtime_metadata_truth(
    deployment: ResolvedDeployment,
    *,
    metadata: Mapping[str, Any],
) -> None:
    advertised = metadata.get("tigrbl_auth_capabilities", ())
    if not isinstance(advertised, Iterable) or isinstance(advertised, (str, bytes)):
        raise CertificationError("metadata capabilities must be a list")
    runtime_capability_truth(
        capability_records_for_deployment(deployment),
        tuple(str(item) for item in advertised),
    )



def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_capability_attestation(
    deployment: ResolvedDeployment | None = None,
    *,
    generated_at: str | None = None,
    claim_ids: Iterable[str] = (),
) -> CapabilityAttestation:
    active_deployment = deployment or resolve_deployment()
    truth = runtime_truth_manifest(active_deployment)
    capabilities = tuple(sorted(truth["capabilities"]))
    routes = tuple(sorted(str(row["path"]) for row in truth["routes"]))
    evidence_ids = tuple(
        sorted(
            str(row["evidence_id"])
            for row in truth["capabilities"].values()
            if row.get("evidence_id")
        )
    )
    generated = generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    unsigned = {
        "version": CAPABILITY_ATTESTATION_VERSION,
        "issuer": active_deployment.issuer,
        "product_surface": active_deployment.product_surface,
        "profile": active_deployment.profile,
        "capabilities": list(capabilities),
        "routes": list(routes),
        "evidence_ids": list(evidence_ids),
        "claim_ids": sorted(str(claim_id) for claim_id in claim_ids),
        "generated_at": generated,
    }
    return CapabilityAttestation(
        **unsigned,
        artifact_sha256=_canonical_sha256(unsigned),
    )


def scoped_deployment_for_metadata(
    deployment: ResolvedDeployment,
    *,
    issuer: str,
    protected_resource_identifier: str | None = None,
) -> ResolvedDeployment:
    return replace(
        deployment,
        issuer=issuer.rstrip("/"),
        protected_resource_identifier=(
            protected_resource_identifier
            or deployment.protected_resource_identifier
        ),
    )


__all__ = [
    "CAPABILITY_ATTESTATION_VERSION",
    "CapabilityAttestation",
    "assert_runtime_metadata_truth",
    "build_capability_attestation",
    "capability_records_for_deployment",
    "runtime_truth_manifest",
    "scoped_deployment_for_metadata",
]
