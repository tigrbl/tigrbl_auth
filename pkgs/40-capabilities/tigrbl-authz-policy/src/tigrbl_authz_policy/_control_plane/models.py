from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from tigrbl_identity_contracts.authentication import ServiceIdentityAuthentication
from tigrbl_identity_contracts.authority import Role
from tigrbl_identity_contracts.credentials import ServiceCredential
from tigrbl_identity_contracts.delegation import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    DelegatedAdminScope,
)
from tigrbl_identity_contracts.policy.conditions import DynamicCondition
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_identity_contracts.policy.rules import AttributePolicy
from tigrbl_identity_contracts.principals import ServiceIdentity

ADMIN_POLICY_BOUNDARY_FEATURES: tuple[dict[str, Any], ...] = (
    {"feature_id": "feat:f03-service-identities", "category": "service-identity", "runtime_objects": ("ServiceIdentityRegistry", "ServiceIdentityAuthentication"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f13-rbac", "category": "rbac", "runtime_objects": ("RBACAdministration", "Role"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f14-abac", "category": "abac", "runtime_objects": ("ABACAdministration", "AttributePolicy"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f16-policy-engine", "category": "policy-engine", "runtime_objects": ("PolicyEngine", "PolicyDecision"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f19-policy-simulation", "category": "simulation", "runtime_objects": ("simulate_policy",), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f20-policy-audit", "category": "audit", "runtime_objects": ("PolicyAuditEvent", "PolicyEngine.audit_events"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f24-fine-grained-permissions", "category": "permissions", "runtime_objects": ("RBACAdministration.effective_permissions", "DynamicCondition"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f25-dynamic-conditions", "category": "conditions", "runtime_objects": ("DynamicCondition", "ABACAdministration"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f42-compliance-reporting", "category": "compliance", "runtime_objects": ("build_compliance_report", "PolicyEngine.compliance_report"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:f45-delegated-admin", "category": "delegation", "runtime_objects": ("DelegatedAdministration", "DelegatedAdminScope"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:tenant-isolation-cross-plane", "category": "tenant-isolation", "runtime_objects": ("filter_visible_tenants", "DelegatedAdministration.visible_tenant_ids"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:tenant-visibility-rules", "category": "tenant-visibility", "runtime_objects": ("filter_visible_tenants",), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:client-policy-cross-plane", "category": "client-policy", "runtime_objects": ("expose_client_record", "assert_client_mutation_authority"), "guarded_planes": ("admin", "public", "policy")},
    {"feature_id": "feat:client-mutation-authority-rules", "category": "client-mutation", "runtime_objects": ("assert_client_mutation_authority", "DelegatedAdministration.authorize"), "guarded_planes": ("admin", "policy")},
    {"feature_id": "feat:public-vs-admin-client-exposure", "category": "client-exposure", "runtime_objects": ("PUBLIC_CLIENT_FIELDS", "ADMIN_CLIENT_FIELDS"), "guarded_planes": ("admin", "public")},
)

PHASE3_ADMIN_POLICY_FEATURES = ADMIN_POLICY_BOUNDARY_FEATURES


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
        str(feature["feature_id"]): {
            "category": feature["category"],
            "runtime_objects": list(feature["runtime_objects"]),
            "guarded_planes": list(feature["guarded_planes"]),
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
