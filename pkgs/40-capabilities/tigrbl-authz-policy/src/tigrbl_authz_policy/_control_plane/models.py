from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from tigrbl_control_plane_contracts.admin import *


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _permission_matches(grant: str, permission: str) -> bool:
    if grant == "*" or grant == permission:
        return True
    if grant.endswith(".*"):
        prefix = grant[:-2]
        return permission == prefix or permission.startswith(f"{prefix}.")
    return False


def _pick_fields(record: Mapping[str, Any], fields: Iterable[str]) -> dict[str, Any]:
    return {field: record[field] for field in fields if field in record}


def admin_policy_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature.feature_id: {
            "category": feature.category,
            "runtime_objects": list(feature.runtime_objects),
            "guarded_planes": list(feature.guarded_planes),
        }
        for feature in ADMIN_POLICY_BOUNDARY_FEATURES
    }


def admin_policy_boundary_integrity() -> dict[str, Any]:
    manifest = admin_policy_boundary_manifest()
    service_keys_present = "feat:f03-service-identities" in manifest
    public_fields = set(PUBLIC_CLIENT_FIELDS)
    admin_fields = set(ADMIN_CLIENT_FIELDS)
    delegated_mutable = set(DELEGATED_MUTABLE_CLIENT_FIELDS)
    failures = []
    if len(manifest) != 15:
        failures.append("phase 3 admin policy boundary must track exactly 15 feature rows")
    if not service_keys_present:
        failures.append("service identity policy row is missing")
    if "client_secret" in public_fields:
        failures.append("public client exposure leaks client_secret")
    if not public_fields < admin_fields:
        failures.append("public client fields must be a strict subset of admin fields")
    if not delegated_mutable <= admin_fields:
        failures.append("delegated mutable client fields must be admin-owned fields")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "categories": sorted({row["category"] for row in manifest.values()}),
        "failures": failures,
    }


phase3_admin_policy_boundary_manifest = admin_policy_boundary_manifest
phase3_admin_policy_boundary_integrity = admin_policy_boundary_integrity
