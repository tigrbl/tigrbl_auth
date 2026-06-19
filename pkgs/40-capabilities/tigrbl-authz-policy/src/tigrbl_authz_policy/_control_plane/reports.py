from __future__ import annotations

from typing import Any, Iterable, Mapping

from .models import *
from .administration import *
from .policy_engine import *

def build_compliance_report(
    *,
    service_registry: ServiceIdentityRegistry,
    rbac: RBACAdministration,
    abac: ABACAdministration,
    delegated_admin: DelegatedAdministration,
    audit_events: Iterable[PolicyAuditEvent],
    tenant_ids: Iterable[str],
    clients: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    tenant_ids_tuple = tuple(sorted(set(str(tenant_id) for tenant_id in tenant_ids)))
    clients_list = [dict(client) for client in clients]
    audit_list = list(audit_events)
    return {
        "tenant_isolation": {
            "enforced": True,
            "tenants": list(tenant_ids_tuple),
            "delegated_tenant_map": delegated_admin.summary()["tenant_map"],
        },
        "service_identities": service_registry.summary(),
        "policy_engine": {
            "role_count": len(rbac.roles),
            "policy_count": len(abac.policies),
            "audit_event_count": len(audit_list),
        },
        "delegated_admin": delegated_admin.summary(),
        "client_exposure": {
            "public_fields": list(PUBLIC_CLIENT_FIELDS),
            "admin_fields": list(ADMIN_CLIENT_FIELDS),
            "client_count": len(clients_list),
        },
        "recent_audit": [
            {
                "subject": event.subject,
                "tenant_id": event.tenant_id,
                "permission": event.permission,
                "allowed": event.allowed,
                "reason": event.reason,
            }
            for event in sorted(audit_list, key=lambda event: (event.recorded_at, event.event_id))[-10:]
        ],
    }


__all__ = [
    "ABACAdministration",
    "ADMIN_POLICY_BOUNDARY_FEATURES",
    "ADMIN_CLIENT_FIELDS",
    "AdminPolicyBoundaryFeature",
    "AttributePolicy",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "DelegatedAdministration",
    "DynamicCondition",
    "PUBLIC_CLIENT_FIELDS",
    "PolicyAuditEvent",
    "PolicyDecision",
    "PolicyEngine",
    "PHASE3_ADMIN_POLICY_FEATURES",
    "RBACAdministration",
    "Role",
    "ServiceCredential",
    "ServiceIdentity",
    "ServiceIdentityAuthentication",
    "ServiceIdentityRegistry",
    "assert_client_mutation_authority",
    "build_compliance_report",
    "admin_policy_boundary_integrity",
    "admin_policy_boundary_manifest",
    "expose_client_record",
    "filter_visible_tenants",
    "phase3_admin_policy_boundary_integrity",
    "phase3_admin_policy_boundary_manifest",
    "simulate_policy",
]
