from __future__ import annotations

from dataclasses import dataclass


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


PHASE3_ADMIN_POLICY_FEATURES = ADMIN_POLICY_BOUNDARY_FEATURES


__all__ = [
    "ADMIN_CLIENT_FIELDS",
    "ADMIN_POLICY_BOUNDARY_FEATURES",
    "AdminPolicyBoundaryFeature",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "PHASE3_ADMIN_POLICY_FEATURES",
    "PUBLIC_CLIENT_FIELDS",
    "ServiceCredential",
    "ServiceIdentity",
    "ServiceIdentityAuthentication",
]
