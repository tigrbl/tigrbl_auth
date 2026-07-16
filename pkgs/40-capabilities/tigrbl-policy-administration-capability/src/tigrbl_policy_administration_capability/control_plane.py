"""Authorization control-plane public surface."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from tigrbl_identity_core.normalization import (
    pick_fields as _pick_fields,
)
from tigrbl_identity_contracts.audit.policy import PolicyAuditEvent as _PolicyAuditEvent
from tigrbl_identity_contracts.delegation import (
    PUBLIC_CLIENT_FIELDS,
)
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from .abac import (
    ABACAdministrator,
    AttributePolicy,
    DynamicCondition,
)
from .policy_engine import PolicyEngine
from .delegated_admin import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    DelegatedAdministrator,
    DelegatedAdminScope,
)
from tigrbl_access_governance_capability.service_identity_registry import (
    ServiceCredential,
    ServiceIdentity,
    ServiceIdentityAuthentication,
    ServiceIdentityRegistry,
)
from .rbac import RBACAdministrator, Role


async def simulate_policy(
    *,
    rbac: RBACAdministrator,
    abac: ABACAdministrator,
    subject: str,
    permission: str,
    attributes: Mapping[str, Any],
    tenant_id: str | None = None,
    client_id: str | None = None,
) -> PolicyDecision:
    tenant = tenant_id or str(attributes.get("tenant_id") or "")
    engine = PolicyEngine(
        rbac=rbac, abac=abac, delegated_admin=DelegatedAdministrator(rbac.db)
    )
    if tenant:
        return await engine.evaluate(
            subject=subject,
            permission=permission,
            tenant_id=tenant,
            attributes=attributes,
            client_id=client_id,
        )
    rbac_decision = await rbac.decide(subject, permission, tenant_id)
    abac_decision = await abac.decide(
        permission=permission,
        attributes=attributes,
        tenant_id=tenant_id,
        client_id=client_id,
    )
    if rbac_decision.allowed and abac_decision.allowed:
        return PolicyDecision(
            True,
            "permission granted by RBAC assignment and ABAC attributes",
            rbac_decision.matched + abac_decision.matched,
        )
    reasons = [rbac_decision.reason, abac_decision.reason]
    return PolicyDecision(
        False, "; ".join(reasons), rbac_decision.matched + abac_decision.matched
    )


async def filter_visible_tenants(
    tenants: Iterable[Mapping[str, Any]],
    *,
    subject: str,
    delegated_admin: DelegatedAdministrator | None = None,
) -> list[dict[str, Any]]:
    tenants_list = [dict(tenant) for tenant in tenants]
    if delegated_admin is None:
        return tenants_list
    visible_ids = set(
        await delegated_admin.visible_tenant_ids(
            subject, (str(tenant.get("id")) for tenant in tenants_list)
        )
    )
    return [tenant for tenant in tenants_list if str(tenant.get("id")) in visible_ids]


async def expose_client_record(
    client: Mapping[str, Any],
    *,
    plane: str,
    subject: str | None = None,
    delegated_admin: DelegatedAdministrator | None = None,
) -> dict[str, Any]:
    if plane == "public":
        return _pick_fields(client, PUBLIC_CLIENT_FIELDS)
    if plane != "admin":
        raise ValueError(f"unsupported exposure plane {plane!r}")
    if (
        delegated_admin is not None
        and subject is not None
        and await delegated_admin.scope_for(subject) is not None
    ):
        return _pick_fields(
            client, await delegated_admin.visible_client_fields_for(subject)
        )
    return _pick_fields(client, ADMIN_CLIENT_FIELDS)


async def assert_client_mutation_authority(
    *,
    subject: str,
    tenant_id: str,
    patch: Mapping[str, Any],
    delegated_admin: DelegatedAdministrator | None = None,
) -> None:
    patch_fields = tuple(sorted(set(patch)))
    if "tenant_id" in patch and patch["tenant_id"] != tenant_id:
        raise PermissionError("tenant mutation is not allowed")
    if delegated_admin is None:
        return
    decision = await delegated_admin.authorize(
        subject,
        tenant_id=tenant_id,
        permission="client.update",
        patch_fields=patch_fields,
    )
    if not decision.allowed:
        raise PermissionError(decision.reason)


async def build_compliance_report(
    *,
    service_registry: ServiceIdentityRegistry,
    rbac: RBACAdministrator,
    abac: ABACAdministrator,
    delegated_admin: DelegatedAdministrator,
    audit_events: Iterable[_PolicyAuditEvent],
    tenant_ids: Iterable[str],
    clients: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    tenant_ids_tuple = tuple(sorted(set(str(tenant_id) for tenant_id in tenant_ids)))
    clients_list = [dict(client) for client in clients]
    audit_list = list(audit_events)
    delegated_summary = await delegated_admin.summary()
    rbac_summary = await rbac.summary()
    abac_summary = await abac.summary()
    return {
        "tenant_isolation": {
            "enforced": True,
            "tenants": list(tenant_ids_tuple),
            "delegated_tenant_map": delegated_summary["tenant_map"],
        },
        "service_identities": service_registry.summary(),
        "policy_engine": {
            "role_count": rbac_summary["role_count"],
            "policy_count": abac_summary["policy_count"],
            "audit_event_count": len(audit_list),
        },
        "delegated_admin": delegated_summary,
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
            for event in sorted(
                audit_list, key=lambda event: (event.recorded_at, event.event_id)
            )[-10:]
        ],
    }


__all__ = [
    "ABACAdministrator",
    "ADMIN_CLIENT_FIELDS",
    "AttributePolicy",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "DelegatedAdministrator",
    "DynamicCondition",
    "PUBLIC_CLIENT_FIELDS",
    "PolicyDecision",
    "PolicyEngine",
    "RBACAdministrator",
    "Role",
    "ServiceCredential",
    "ServiceIdentity",
    "ServiceIdentityAuthentication",
    "ServiceIdentityRegistry",
    "assert_client_mutation_authority",
    "build_compliance_report",
    "expose_client_record",
    "filter_visible_tenants",
    "simulate_policy",
]
