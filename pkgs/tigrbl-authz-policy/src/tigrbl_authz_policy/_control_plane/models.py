from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping
from uuid import uuid4

PUBLIC_CLIENT_FIELDS: tuple[str, ...] = ("name", "client_id", "redirect_uris", "type")
ADMIN_CLIENT_FIELDS: tuple[str, ...] = (
    "id",
    "tenant_id",
    "name",
    "client_id",
    "client_secret",
    "redirect_uris",
    "type",
    "created_at",
    "enabled",
    "policy_tags",
)
DELEGATED_VISIBLE_CLIENT_FIELDS: tuple[str, ...] = (
    "id",
    "tenant_id",
    "name",
    "client_id",
    "redirect_uris",
    "type",
    "created_at",
    "enabled",
)
DELEGATED_MUTABLE_CLIENT_FIELDS: tuple[str, ...] = (
    "name",
    "redirect_uris",
    "enabled",
    "type",
)


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


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason: str
    matched: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Role:
    name: str
    permissions: tuple[str, ...]
    tenant_id: str | None = None
    denied_permissions: tuple[str, ...] = ()
    inherited_roles: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DynamicCondition:
    field: str
    operator: str
    expected: Any

    def evaluate(self, attributes: Mapping[str, Any]) -> bool:
        actual = attributes.get(self.field)
        if self.operator == "eq":
            return actual == self.expected
        if self.operator == "neq":
            return actual != self.expected
        if self.operator == "in":
            return actual in self.expected
        if self.operator == "contains":
            return self.expected in actual if actual is not None else False
        if self.operator == "gte":
            return actual is not None and actual >= self.expected
        if self.operator == "lte":
            return actual is not None and actual <= self.expected
        if self.operator == "prefix":
            return isinstance(actual, str) and actual.startswith(str(self.expected))
        raise ValueError(f"unsupported dynamic condition operator {self.operator!r}")


@dataclass(frozen=True, slots=True)
class AttributePolicy:
    name: str
    permission: str
    required_attributes: Mapping[str, Any]
    tenant_id: str | None = None
    dynamic_conditions: tuple[DynamicCondition, ...] = ()
    effect: str = "allow"
    client_id: str | None = None


@dataclass(frozen=True, slots=True)
class PolicyAuditEvent:
    event_id: str
    subject: str
    tenant_id: str | None
    permission: str
    allowed: bool
    reason: str
    matched: tuple[str, ...]
    actor_type: str
    recorded_at: str
    client_id: str | None = None


@dataclass(frozen=True, slots=True)
class ServiceIdentity:
    service_id: str
    tenant_id: str
    name: str
    scopes: tuple[str, ...]
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class ServiceCredential:
    credential_id: str
    service_id: str
    label: str
    raw_key: str
    created_at: str
    revoked: bool = False
    expires_at: str | None = None


@dataclass(frozen=True, slots=True)
class ServiceIdentityAuthentication:
    service: ServiceIdentity
    credential_id: str
    granted_permissions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DelegatedAdminScope:
    subject: str
    tenant_ids: tuple[str, ...]
    permissions: tuple[str, ...]
    visible_client_fields: tuple[str, ...] = DELEGATED_VISIBLE_CLIENT_FIELDS
    mutable_client_fields: tuple[str, ...] = DELEGATED_MUTABLE_CLIENT_FIELDS
    service_identity_permissions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AdminPolicyBoundaryFeature:
    feature_id: str
    category: str
    runtime_objects: tuple[str, ...]
    guarded_planes: tuple[str, ...]


ADMIN_POLICY_BOUNDARY_FEATURES: tuple[AdminPolicyBoundaryFeature, ...] = (
    AdminPolicyBoundaryFeature("feat:f03-service-identities", "service-identity", ("ServiceIdentityRegistry", "ServiceIdentityAuthentication"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f13-rbac", "rbac", ("RBACAdministration", "Role"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f14-abac", "abac", ("ABACAdministration", "AttributePolicy"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f16-policy-engine", "policy-engine", ("PolicyEngine", "PolicyDecision"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f19-policy-simulation", "simulation", ("simulate_policy",), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f20-policy-audit", "audit", ("PolicyAuditEvent", "PolicyEngine.audit_events"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f24-fine-grained-permissions", "permissions", ("RBACAdministration.effective_permissions", "DynamicCondition"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f25-dynamic-conditions", "conditions", ("DynamicCondition", "ABACAdministration"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f42-compliance-reporting", "compliance", ("build_compliance_report", "PolicyEngine.compliance_report"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:f45-delegated-admin", "delegation", ("DelegatedAdministration", "DelegatedAdminScope"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:tenant-isolation-cross-plane", "tenant-isolation", ("filter_visible_tenants", "DelegatedAdministration.visible_tenant_ids"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:tenant-visibility-rules", "tenant-visibility", ("filter_visible_tenants",), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:client-policy-cross-plane", "client-policy", ("expose_client_record", "assert_client_mutation_authority"), ("admin", "public", "policy")),
    AdminPolicyBoundaryFeature("feat:client-mutation-authority-rules", "client-mutation", ("assert_client_mutation_authority", "DelegatedAdministration.authorize"), ("admin", "policy")),
    AdminPolicyBoundaryFeature("feat:public-vs-admin-client-exposure", "client-exposure", ("PUBLIC_CLIENT_FIELDS", "ADMIN_CLIENT_FIELDS"), ("admin", "public")),
)


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


PHASE3_ADMIN_POLICY_FEATURES = ADMIN_POLICY_BOUNDARY_FEATURES
phase3_admin_policy_boundary_manifest = admin_policy_boundary_manifest
phase3_admin_policy_boundary_integrity = admin_policy_boundary_integrity


