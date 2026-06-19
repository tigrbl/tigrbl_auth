from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


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


PROVISIONING_GOVERNANCE_ECOSYSTEM_FEATURES: tuple[GovernanceExtensionBoundaryFeature, ...] = (
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


PHASE5_GOVERNANCE_EXTENSION_FEATURES = PROVISIONING_GOVERNANCE_ECOSYSTEM_FEATURES


__all__ = [
    "AccessReviewCampaign",
    "AccessReviewDecision",
    "AccessReviewItem",
    "EntitlementAssignment",
    "EntitlementDefinition",
    "GovernanceExtensionBoundaryFeature",
    "PHASE5_GOVERNANCE_EXTENSION_FEATURES",
    "PROVISIONING_GOVERNANCE_ECOSYSTEM_FEATURES",
    "PluginDescriptor",
    "PluginLifecycleEvent",
    "SDKPackage",
    "ScimGroup",
    "ScimPatchOperation",
    "ScimSchema",
    "ScimUser",
]
