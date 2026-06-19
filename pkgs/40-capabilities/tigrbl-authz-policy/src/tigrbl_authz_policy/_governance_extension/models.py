from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from tigrbl_control_plane_contracts.governance import *


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _utc_now_iso() -> str:
    return _utc_now().isoformat()


def _semver_key(version: str) -> tuple[int, int, int]:
    text = version.strip().lstrip("v")
    head = text.split("-", 1)[0]
    parts = [part for part in head.split(".") if part]
    numbers: list[int] = []
    for part in parts[:3]:
        digits = "".join(ch for ch in part if ch.isdigit())
        numbers.append(int(digits or "0"))
    while len(numbers) < 3:
        numbers.append(0)
    return numbers[0], numbers[1], numbers[2]


def _version_in_range(version: str, compatible_runtime_range: tuple[str, str]) -> bool:
    lower, upper = compatible_runtime_range
    version_key = _semver_key(version)
    return _semver_key(lower) <= version_key <= _semver_key(upper)


def provisioning_governance_ecosystem_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature.feature_id: {
            "category": feature.category,
            "runtime_objects": list(feature.runtime_objects),
            "guarded_capabilities": list(feature.guarded_capabilities),
        }
        for feature in PROVISIONING_GOVERNANCE_ECOSYSTEM_FEATURES
    }


def provisioning_governance_ecosystem_boundary_integrity() -> dict[str, Any]:
    manifest = provisioning_governance_ecosystem_boundary_manifest()
    categories = {row["category"] for row in manifest.values()}
    runtime_objects = {
        runtime_object
        for row in manifest.values()
        for runtime_object in row["runtime_objects"]
    }
    failures: list[str] = []
    if len(manifest) != 5:
        failures.append("phase 5 governance extension boundary must track exactly 5 feature rows")
    for required in (
        "sdk-ecosystem",
        "plugins",
        "scim-provisioning",
        "access-review",
        "entitlement-management",
    ):
        if required not in categories:
            failures.append(f"missing category {required}")
    for required_object in (
        "SDKEcosystemCatalog",
        "PluginRuntimeRegistry",
        "ScimProvisioningPlane",
        "EntitlementManager",
        "AccessReviewWorkflow",
    ):
        if required_object not in runtime_objects:
            failures.append(f"missing runtime object {required_object}")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "categories": sorted(categories),
        "failures": failures,
    }


phase5_governance_extension_boundary_manifest = (
    provisioning_governance_ecosystem_boundary_manifest
)
phase5_governance_extension_boundary_integrity = (
    provisioning_governance_ecosystem_boundary_integrity
)
