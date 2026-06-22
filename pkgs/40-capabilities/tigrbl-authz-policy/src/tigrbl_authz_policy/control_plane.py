"""Authorization control-plane public surface."""

from __future__ import annotations

from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.normalization import (
    pick_fields as _pick_fields,
)
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.audit.policy import PolicyAuditEvent as _PolicyAuditEvent
from tigrbl_identity_contracts.delegation import (
    PUBLIC_CLIENT_FIELDS,
)
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_authz_policy_abac_administrator import (
    ABACAdministrator,
    AttributePolicy,
    DynamicCondition,
)
from tigrbl_authz_policy_delegated_administrator import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    DelegatedAdministrator,
    DelegatedAdminScope,
)
from tigrbl_authz_policy_service_identity_registry import (
    ServiceCredential,
    ServiceIdentity,
    ServiceIdentityAuthentication,
    ServiceIdentityRegistry,
)
from tigrbl_authz_policy_rbac_administrator import RBACAdministrator, Role


class PolicyEngine:
    def __init__(
        self,
        *,
        db: Any | None = None,
        rbac: RBACAdministrator | None = None,
        abac: ABACAdministrator | None = None,
        delegated_admin: DelegatedAdministrator | None = None,
    ) -> None:
        if db is None and (rbac is None or abac is None or delegated_admin is None):
            raise ValueError("db is required when PolicyEngine constructs storage-backed administrators")
        self.db = db
        self.rbac = rbac or RBACAdministrator(db)
        self.abac = abac or ABACAdministrator(db)
        self.delegated_admin = delegated_admin or DelegatedAdministrator(db)
        self._audit_events: list[_PolicyAuditEvent] = []

    @property
    def audit_events(self) -> tuple[_PolicyAuditEvent, ...]:
        return tuple(self._audit_events)

    async def evaluate(
        self,
        *,
        subject: str,
        permission: str,
        tenant_id: str,
        attributes: Mapping[str, Any],
        actor_type: str = "user",
        client_id: str | None = None,
        service_auth: ServiceIdentityAuthentication | None = None,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision:
        delegated = await self.delegated_admin.authorize(
            subject,
            tenant_id=tenant_id,
            permission=permission,
            patch_fields=patch_fields,
        )
        if not delegated.allowed:
            decision = delegated
            self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type=actor_type, client_id=client_id)
            return decision

        if service_auth is not None:
            if service_auth.service.tenant_id != tenant_id:
                decision = PolicyDecision(False, "permission denied by service identity tenant mismatch", (service_auth.service.name,))
                self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type="service", client_id=client_id)
                return decision
            if not any(_permission_matches(grant, permission) for grant in service_auth.granted_permissions):
                decision = PolicyDecision(False, "permission denied by service identity scopes", (service_auth.service.name,))
                self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type="service", client_id=client_id)
                return decision
            rbac_decision = PolicyDecision(True, "permission granted by service identity scope", (service_auth.service.name,))
        else:
            rbac_decision = await self.rbac.decide(subject, permission, tenant_id)

        abac_decision = await self.abac.decide(
            permission=permission,
            attributes=attributes,
            tenant_id=tenant_id,
            client_id=client_id,
        )
        requires_abac = await self.abac.has_relevant_policy(permission, tenant_id, client_id)

        if rbac_decision.allowed and (abac_decision.allowed or not requires_abac):
            matched = rbac_decision.matched + (() if not requires_abac else abac_decision.matched)
            reason = rbac_decision.reason if not requires_abac else "permission granted by RBAC assignment and ABAC attributes"
            decision = PolicyDecision(True, reason, matched)
        elif not rbac_decision.allowed:
            matched = rbac_decision.matched + abac_decision.matched
            decision = PolicyDecision(False, rbac_decision.reason, matched)
        else:
            matched = rbac_decision.matched + abac_decision.matched
            decision = PolicyDecision(False, abac_decision.reason, matched)

        self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type=actor_type, client_id=client_id)
        return decision

    async def compliance_report(
        self,
        *,
        service_registry: ServiceIdentityRegistry,
        tenants: Iterable[Mapping[str, Any]],
        clients: Iterable[Mapping[str, Any]],
    ) -> dict[str, Any]:
        tenant_ids = [str(tenant["id"]) for tenant in tenants if "id" in tenant]
        return await build_compliance_report(
            service_registry=service_registry,
            rbac=self.rbac,
            abac=self.abac,
            delegated_admin=self.delegated_admin,
            audit_events=self.audit_events,
            tenant_ids=tenant_ids,
            clients=clients,
        )

    def _record_audit(
        self,
        decision: PolicyDecision,
        *,
        subject: str,
        tenant_id: str,
        permission: str,
        actor_type: str,
        client_id: str | None,
    ) -> None:
        self._audit_events.append(
            _PolicyAuditEvent(
                event_id=f"policy-audit-{uuid4().hex}",
                subject=subject,
                tenant_id=tenant_id,
                permission=permission,
                allowed=decision.allowed,
                reason=decision.reason,
                matched=decision.matched,
                actor_type=actor_type,
                recorded_at=utc_now_iso(),
                client_id=client_id,
            )
        )


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
    engine = PolicyEngine(rbac=rbac, abac=abac, delegated_admin=DelegatedAdministrator(rbac.db))
    if tenant:
        return await engine.evaluate(
            subject=subject,
            permission=permission,
            tenant_id=tenant,
            attributes=attributes,
            client_id=client_id,
        )
    rbac_decision = await rbac.decide(subject, permission, tenant_id)
    abac_decision = await abac.decide(permission=permission, attributes=attributes, tenant_id=tenant_id, client_id=client_id)
    if rbac_decision.allowed and abac_decision.allowed:
        return PolicyDecision(
            True,
            "permission granted by RBAC assignment and ABAC attributes",
            rbac_decision.matched + abac_decision.matched,
        )
    reasons = [rbac_decision.reason, abac_decision.reason]
    return PolicyDecision(False, "; ".join(reasons), rbac_decision.matched + abac_decision.matched)


async def filter_visible_tenants(
    tenants: Iterable[Mapping[str, Any]],
    *,
    subject: str,
    delegated_admin: DelegatedAdministrator | None = None,
) -> list[dict[str, Any]]:
    tenants_list = [dict(tenant) for tenant in tenants]
    if delegated_admin is None:
        return tenants_list
    visible_ids = set(await delegated_admin.visible_tenant_ids(subject, (str(tenant.get("id")) for tenant in tenants_list)))
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
    if delegated_admin is not None and subject is not None and await delegated_admin.scope_for(subject) is not None:
        return _pick_fields(client, await delegated_admin.visible_client_fields_for(subject))
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
            for event in sorted(audit_list, key=lambda event: (event.recorded_at, event.event_id))[-10:]
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
