from __future__ import annotations

from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.audit.policy import PolicyAuditEvent as _PolicyAuditEvent
from tigrbl_identity_contracts.delegation import ADMIN_CLIENT_FIELDS, PUBLIC_CLIENT_FIELDS
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_authz_policy_abac_administrator import ABACAdministrator
from tigrbl_authz_policy_delegated_administrator import DelegatedAdministrator
from tigrbl_authz_policy_rbac_administrator import RBACAdministrator
from tigrbl_authz_policy_service_identity_registry import (
    ServiceIdentityAuthentication,
    ServiceIdentityRegistry,
)


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
        return await self._build_compliance_report(
            service_registry=service_registry,
            tenant_ids=tenant_ids,
            clients=clients,
        )

    async def _build_compliance_report(
        self,
        *,
        service_registry: ServiceIdentityRegistry,
        tenant_ids: Iterable[str],
        clients: Iterable[Mapping[str, Any]],
    ) -> dict[str, Any]:
        tenant_ids_tuple = tuple(sorted(set(str(tenant_id) for tenant_id in tenant_ids)))
        clients_list = [dict(client) for client in clients]
        audit_list = list(self.audit_events)
        delegated_summary = await self.delegated_admin.summary()
        rbac_summary = await self.rbac.summary()
        abac_summary = await self.abac.summary()
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


__all__ = ["PolicyEngine"]
