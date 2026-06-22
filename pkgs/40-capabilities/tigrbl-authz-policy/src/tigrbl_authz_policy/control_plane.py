"""Authorization control-plane public surface."""

from __future__ import annotations

from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.normalization import (
    pick_fields as _pick_fields,
    row_active as _row_active,
    row_value as _row_value,
    str_tuple as _str_tuple,
)
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.audit.policy import PolicyAuditEvent as _PolicyAuditEvent
from tigrbl_identity_contracts.delegation import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    DelegatedAdminScope,
)
from tigrbl_identity_contracts.policy.conditions import DynamicCondition
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_authz_policy_service_identity_registry import (
    ServiceCredential,
    ServiceIdentity,
    ServiceIdentityAuthentication,
    ServiceIdentityRegistry,
)
from tigrbl_authz_policy_rbac_administrator import RBACAdministrator, Role
from tigrbl_identity_storage.tables.attribute_policy import AttributePolicy as _StoredAttributePolicy
from tigrbl_identity_storage.tables.delegated_admin_scope import DelegatedAdminScope as _StoredDelegatedAdminScope
from tigrbl_authz_policy_concrete import AttributePolicy


def _condition_contract(row: Any) -> DynamicCondition:
    return DynamicCondition(
        field=str(_row_value(row, "field_name") or ""),
        operator=str(_row_value(row, "operator") or ""),
        expected=_row_value(row, "expected"),
    )


def _attribute_policy_contract(row: Any, conditions: Iterable[Any] = ()) -> AttributePolicy:
    return AttributePolicy(
        name=str(_row_value(row, "name") or ""),
        permission=str(_row_value(row, "permission") or ""),
        tenant_id=_row_value(row, "tenant_id"),
        client_id=_row_value(row, "client_id"),
        effect=str(_row_value(row, "effect", "allow") or "allow"),
        required_attributes=dict(_row_value(row, "required_attributes", {}) or {}),
        dynamic_conditions=tuple(_condition_contract(condition) for condition in conditions),
    )


def _delegated_scope_contract(row: Any) -> DelegatedAdminScope:
    visible = _str_tuple(_row_value(row, "visible_client_fields")) or DELEGATED_VISIBLE_CLIENT_FIELDS
    mutable = _str_tuple(_row_value(row, "mutable_client_fields")) or DELEGATED_MUTABLE_CLIENT_FIELDS
    return DelegatedAdminScope(
        subject=str(_row_value(row, "subject") or ""),
        tenant_ids=_str_tuple(_row_value(row, "tenant_ids")),
        permissions=_str_tuple(_row_value(row, "permissions")),
        visible_client_fields=visible,
        mutable_client_fields=mutable,
        service_identity_permissions=_str_tuple(_row_value(row, "service_identity_permissions")),
    )


class ABACAdministrator:
    def __init__(self, db: Any) -> None:
        self.db = db

    async def upsert_policy(
        self,
        name: str,
        *,
        permission: str,
        required_attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        dynamic_conditions: Iterable[DynamicCondition] = (),
        effect: str = "allow",
        client_id: str | None = None,
    ) -> AttributePolicy:
        if not name or not permission or not required_attributes:
            raise ValueError("policy name, permission, and attributes are required")
        row, conditions = await _StoredAttributePolicy.upsert_with_conditions(
            self.db,
            name=name,
            tenant_id=tenant_id,
            client_id=client_id,
            permission=permission,
            effect=effect,
            required_attributes=dict(required_attributes),
            dynamic_conditions=(
                {"field_name": condition.field, "operator": condition.operator, "expected": condition.expected}
                for condition in dynamic_conditions
            ),
        )
        return _attribute_policy_contract(row, conditions)

    async def has_relevant_policy(
        self,
        permission: str,
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> bool:
        return bool(await self._matching_policies(permission, tenant_id=tenant_id, client_id=client_id))

    async def decide(
        self,
        *,
        permission: str,
        attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> PolicyDecision:
        allow_matches: list[str] = []
        deny_matches: list[str] = []
        for policy in await self._matching_policies(permission, tenant_id=tenant_id, client_id=client_id):
            if not all(attributes.get(key) == value for key, value in policy.required_attributes.items()):
                continue
            if not all(condition.evaluate(attributes) for condition in policy.dynamic_conditions):
                continue
            if policy.effect == "deny":
                deny_matches.append(policy.name)
            else:
                allow_matches.append(policy.name)
        if deny_matches:
            return PolicyDecision(False, "permission denied by ABAC attributes", tuple(sorted(deny_matches)))
        if allow_matches:
            return PolicyDecision(True, "permission granted by matching attributes", tuple(sorted(allow_matches)))
        return PolicyDecision(False, "permission denied by ABAC attributes", ())

    async def list_policies(self) -> tuple[AttributePolicy, ...]:
        return tuple(
            _attribute_policy_contract(row, conditions)
            for row, conditions in await _StoredAttributePolicy.list_active_with_conditions(self.db)
        )

    async def summary(self) -> dict[str, Any]:
        policies = await self.list_policies()
        return {"policy_count": len(policies), "policies": [policy.name for policy in policies]}

    async def _matching_policies(
        self,
        permission: str,
        *,
        tenant_id: str | None,
        client_id: str | None,
    ) -> tuple[AttributePolicy, ...]:
        policies = await self.list_policies()
        return tuple(
            policy
            for policy in policies
            if _permission_matches(policy.permission, permission)
            and policy.tenant_id in {None, tenant_id}
            and policy.client_id in {None, client_id}
        )


class DelegatedAdministrator:
    def __init__(self, db: Any) -> None:
        self.db = db

    async def grant_scope(
        self,
        subject: str,
        *,
        tenant_ids: Iterable[str],
        permissions: Iterable[str],
        visible_client_fields: Iterable[str] = DELEGATED_VISIBLE_CLIENT_FIELDS,
        mutable_client_fields: Iterable[str] = DELEGATED_MUTABLE_CLIENT_FIELDS,
        service_identity_permissions: Iterable[str] = (),
    ) -> DelegatedAdminScope:
        row = await _StoredDelegatedAdminScope.grant_scope(
            self.db,
            subject=subject,
            tenant_ids=list(_str_tuple(tenant_ids)),
            permissions=list(_str_tuple(permissions)),
            visible_client_fields=list(_str_tuple(visible_client_fields)),
            mutable_client_fields=list(_str_tuple(mutable_client_fields)),
            service_identity_permissions=list(_str_tuple(service_identity_permissions)),
        )
        return _delegated_scope_contract(row)

    async def revoke_scope(self, subject: str) -> DelegatedAdminScope | None:
        row = await _StoredDelegatedAdminScope.revoke_scope(self.db, subject=subject)
        return _delegated_scope_contract(row) if row is not None else None

    async def scope_for(self, subject: str) -> DelegatedAdminScope | None:
        row = await _StoredDelegatedAdminScope.lookup(self.db, subject=subject)
        if row is None or not _row_active(row):
            return None
        return _delegated_scope_contract(row)

    async def authorize(
        self,
        subject: str,
        *,
        tenant_id: str,
        permission: str,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision:
        scope = await self.scope_for(subject)
        if scope is None:
            return PolicyDecision(True, "no delegated scope restriction active", ())
        if tenant_id not in scope.tenant_ids:
            return PolicyDecision(False, "permission denied by delegated tenant scope", (scope.subject,))
        if not any(_permission_matches(grant, permission) for grant in scope.permissions):
            return PolicyDecision(False, "permission denied by delegated admin scope", (scope.subject,))
        patch_field_set = set(patch_fields)
        if patch_field_set and not patch_field_set.issubset(set(scope.mutable_client_fields)):
            return PolicyDecision(False, "permission denied by delegated client mutation scope", tuple(sorted(patch_field_set)))
        return PolicyDecision(True, "permission granted by delegated admin scope", (scope.subject,))

    async def visible_tenant_ids(self, subject: str, tenant_ids: Iterable[str]) -> tuple[str, ...]:
        scope = await self.scope_for(subject)
        if scope is None:
            return tuple(sorted(set(tenant_ids)))
        return tuple(sorted(tenant_id for tenant_id in tenant_ids if tenant_id in scope.tenant_ids))

    async def visible_client_fields_for(self, subject: str) -> tuple[str, ...]:
        scope = await self.scope_for(subject)
        if scope is None:
            return ADMIN_CLIENT_FIELDS
        return scope.visible_client_fields

    async def summary(self) -> dict[str, Any]:
        scopes = [
            _delegated_scope_contract(row)
            for row in await _StoredDelegatedAdminScope.list_active(self.db)
            if _row_active(row)
        ]
        return {
            "scope_count": len(scopes),
            "delegates": sorted(scope.subject for scope in scopes),
            "tenant_map": {
                scope.subject: list(scope.tenant_ids)
                for scope in sorted(scopes, key=lambda scope: scope.subject)
            },
        }


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
