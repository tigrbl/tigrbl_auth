from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Iterable, Mapping
from uuid import uuid4


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


@dataclass(frozen=True, slots=True)
class SDKPackage:
    sdk_id: str
    package_name: str
    language: str
    version: str
    compatible_runtime_range: tuple[str, str]
    generated_contracts: Mapping[str, str]
    auth_helpers: tuple[str, ...]
    supported_errors: tuple[str, ...]
    release_channel: str = "stable"


@dataclass(frozen=True, slots=True)
class PluginDescriptor:
    plugin_id: str
    name: str
    version: str
    extension_points: tuple[str, ...]
    lifecycle_hooks: tuple[str, ...]
    compatible_sdk_ids: tuple[str, ...]
    isolation_mode: str
    operator_controls: tuple[str, ...]
    fail_behavior: str
    registered_at: str
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class PluginLifecycleEvent:
    event_id: str
    plugin_id: str
    hook_name: str
    outcome: str
    message: str
    recorded_at: str


@dataclass(frozen=True, slots=True)
class ScimSchema:
    schema_id: str
    resource_kind: str
    required_fields: tuple[str, ...]
    registered_at: str


@dataclass(frozen=True, slots=True)
class ScimUser:
    user_id: str
    tenant_id: str
    user_name: str
    attributes: Mapping[str, Any]
    created_at: str
    active: bool = True


@dataclass(frozen=True, slots=True)
class ScimGroup:
    group_id: str
    tenant_id: str
    display_name: str
    members: tuple[str, ...]
    created_at: str


@dataclass(frozen=True, slots=True)
class ScimPatchOperation:
    op: str
    path: str
    value: Any


@dataclass(frozen=True, slots=True)
class EntitlementDefinition:
    entitlement_id: str
    tenant_id: str
    name: str
    owner: str
    description: str
    created_at: str


@dataclass(frozen=True, slots=True)
class EntitlementAssignment:
    assignment_id: str
    entitlement_id: str
    tenant_id: str
    subject_id: str
    justification: str
    assigned_by: str
    created_at: str
    expires_at: str | None = None
    active: bool = True
    revoked_reason: str | None = None


@dataclass(frozen=True, slots=True)
class AccessReviewItem:
    item_id: str
    assignment_id: str
    subject_id: str
    entitlement_id: str
    reviewer_id: str
    status: str
    due_at: str
    escalation_count: int = 0


@dataclass(frozen=True, slots=True)
class AccessReviewDecision:
    decision_id: str
    item_id: str
    reviewer_id: str
    decision: str
    reason: str
    recorded_at: str


@dataclass(frozen=True, slots=True)
class AccessReviewCampaign:
    campaign_id: str
    tenant_id: str
    name: str
    reviewer_ids: tuple[str, ...]
    item_ids: tuple[str, ...]
    created_at: str
    due_at: str
    closed_at: str | None = None
    status: str = "open"


@dataclass(frozen=True, slots=True)
class GovernanceExtensionBoundaryFeature:
    feature_id: str
    category: str
    runtime_objects: tuple[str, ...]
    guarded_capabilities: tuple[str, ...]


PHASE5_GOVERNANCE_EXTENSION_FEATURES: tuple[GovernanceExtensionBoundaryFeature, ...] = (
    GovernanceExtensionBoundaryFeature(
        "feat:f39-sdk-ecosystem",
        "sdk-ecosystem",
        ("SDKEcosystemCatalog", "SDKPackage"),
        ("runtime-compatibility", "contract-alignment", "auth-helper-inventory"),
    ),
    GovernanceExtensionBoundaryFeature(
        "feat:f40-extensibility-plugins",
        "plugins",
        ("PluginRuntimeRegistry", "PluginDescriptor", "PluginLifecycleEvent"),
        ("isolated-hook-execution", "operator-disable", "lifecycle-audit"),
    ),
    GovernanceExtensionBoundaryFeature(
        "feat:f33-scim-provisioning",
        "scim-provisioning",
        ("ScimProvisioningPlane", "ScimSchema", "ScimUser", "ScimGroup"),
        ("schema-required-fields", "tenant-scope", "patch-validation"),
    ),
    GovernanceExtensionBoundaryFeature(
        "feat:f43-access-review-workflows",
        "access-review",
        ("AccessReviewWorkflow", "AccessReviewCampaign", "AccessReviewDecision"),
        ("reviewer-authorization", "overdue-escalation", "pending-close-guard"),
    ),
    GovernanceExtensionBoundaryFeature(
        "feat:f44-entitlement-management",
        "entitlement-management",
        ("EntitlementManager", "EntitlementDefinition", "EntitlementAssignment"),
        ("assignment-inventory", "expiry", "revocation"),
    ),
)


def phase5_governance_extension_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature.feature_id: {
            "category": feature.category,
            "runtime_objects": list(feature.runtime_objects),
            "guarded_capabilities": list(feature.guarded_capabilities),
        }
        for feature in PHASE5_GOVERNANCE_EXTENSION_FEATURES
    }


def phase5_governance_extension_boundary_integrity() -> dict[str, Any]:
    manifest = phase5_governance_extension_boundary_manifest()
    categories = {row["category"] for row in manifest.values()}
    runtime_objects = {
        runtime_object
        for row in manifest.values()
        for runtime_object in row["runtime_objects"]
    }
    failures: list[str] = []
    if len(manifest) != 5:
        failures.append("phase 5 governance extension boundary must track exactly 5 feature rows")
    for required in ("sdk-ecosystem", "plugins", "scim-provisioning", "access-review", "entitlement-management"):
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


