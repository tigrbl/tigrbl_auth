"""Authorization control-plane public surface."""

from __future__ import annotations

from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.audit.policy import PolicyAuditEvent as _PolicyAuditEvent
from tigrbl_identity_contracts.authentication import ServiceIdentityAuthentication
from tigrbl_identity_contracts.authority import Role
from tigrbl_identity_contracts.delegation import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    DelegatedAdminScope,
)
from tigrbl_identity_contracts.policy.conditions import DynamicCondition
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_identity_concrete import ServiceCredential, ServiceIdentity
from tigrbl_authz_policy_concrete import AttributePolicy


def _pick_fields(record: Mapping[str, Any], fields: Iterable[str]) -> dict[str, Any]:
    return {field: record[field] for field in fields if field in record}


class ServiceIdentityRegistry:
    def __init__(self) -> None:
        self._services: dict[str, ServiceIdentity] = {}
        self._credentials: dict[str, ServiceCredential] = {}

    @property
    def services(self) -> Mapping[str, ServiceIdentity]:
        return dict(self._services)

    @property
    def credentials(self) -> Mapping[str, ServiceCredential]:
        return dict(self._credentials)

    def register_service(
        self,
        service_id: str,
        *,
        tenant_id: str,
        name: str,
        scopes: Iterable[str],
        enabled: bool = True,
    ) -> ServiceIdentity:
        if not service_id or not tenant_id or not name:
            raise ValueError("service identity requires service_id, tenant_id, and name")
        identity = ServiceIdentity(
            service_id=service_id,
            tenant_id=tenant_id,
            name=name,
            scopes=tuple(sorted(set(scopes))),
            enabled=bool(enabled),
        )
        self._services[service_id] = identity
        return identity

    def disable_service(self, service_id: str) -> ServiceIdentity:
        service = self._services[service_id]
        updated = ServiceIdentity(
            service_id=service.service_id,
            tenant_id=service.tenant_id,
            name=service.name,
            scopes=service.scopes,
            enabled=False,
        )
        self._services[service_id] = updated
        return updated

    def issue_credential(
        self,
        service_id: str,
        *,
        label: str,
        raw_key: str | None = None,
        expires_at: str | None = None,
    ) -> ServiceCredential:
        if service_id not in self._services:
            raise KeyError(f"unknown service identity {service_id!r}")
        credential = ServiceCredential(
            credential_id=f"svc-cred-{uuid4().hex}",
            service_id=service_id,
            label=label,
            raw_key=raw_key or f"svc-{uuid4().hex}",
            created_at=utc_now_iso(),
            expires_at=expires_at,
        )
        self._credentials[credential.credential_id] = credential
        return credential

    def revoke_credential(self, credential_id: str) -> ServiceCredential:
        credential = self._credentials[credential_id]
        updated = ServiceCredential(
            credential_id=credential.credential_id,
            service_id=credential.service_id,
            label=credential.label,
            raw_key=credential.raw_key,
            created_at=credential.created_at,
            revoked=True,
            expires_at=credential.expires_at,
        )
        self._credentials[credential_id] = updated
        return updated

    def authenticate(
        self,
        raw_key: str,
        *,
        tenant_id: str,
        required_permission: str | None = None,
    ) -> ServiceIdentityAuthentication:
        credential = next((item for item in self._credentials.values() if item.raw_key == raw_key), None)
        if credential is None:
            raise PermissionError("unknown service credential")
        if credential.revoked:
            raise PermissionError("service credential is revoked")
        service = self._services.get(credential.service_id)
        if service is None or not service.enabled:
            raise PermissionError("service identity is inactive")
        if service.tenant_id != tenant_id:
            raise PermissionError("service identity tenant mismatch")
        if required_permission and not any(_permission_matches(scope, required_permission) for scope in service.scopes):
            raise PermissionError("service identity scope does not authorize requested permission")
        return ServiceIdentityAuthentication(
            service=service,
            credential_id=credential.credential_id,
            granted_permissions=service.scopes,
        )

    def summary(self) -> dict[str, Any]:
        active_services = [service for service in self._services.values() if service.enabled]
        active_credentials = [credential for credential in self._credentials.values() if not credential.revoked]
        return {
            "service_count": len(self._services),
            "active_service_count": len(active_services),
            "active_credential_count": len(active_credentials),
            "tenants": sorted({service.tenant_id for service in self._services.values()}),
        }


class RBACAdministration:
    def __init__(self) -> None:
        self._roles: dict[str, Role] = {}
        self._assignments: dict[str, set[tuple[str, str | None]]] = {}

    @property
    def roles(self) -> Mapping[str, Role]:
        return dict(self._roles)

    @property
    def assignments(self) -> Mapping[str, tuple[str, ...]]:
        return {
            subject: tuple(sorted(role_name for role_name, _tenant_id in assignments))
            for subject, assignments in self._assignments.items()
        }

    def upsert_role(
        self,
        name: str,
        permissions: tuple[str, ...],
        *,
        tenant_id: str | None = None,
        denied_permissions: tuple[str, ...] = (),
        inherited_roles: tuple[str, ...] = (),
    ) -> Role:
        if not name or not permissions:
            raise ValueError("role name and permissions are required")
        role = Role(
            name=name,
            permissions=tuple(sorted(set(permissions))),
            tenant_id=tenant_id,
            denied_permissions=tuple(sorted(set(denied_permissions))),
            inherited_roles=tuple(sorted(set(inherited_roles))),
        )
        self._roles[name] = role
        return role

    def assign_role(self, subject: str, role_name: str, *, tenant_id: str | None = None) -> None:
        if role_name not in self._roles:
            raise KeyError(f"unknown role {role_name!r}")
        self._assignments.setdefault(subject, set()).add((role_name, tenant_id))

    def effective_permissions(self, subject: str, tenant_id: str | None = None) -> tuple[str, ...]:
        grants, _denies, _matched = self._decision_inputs(subject, tenant_id)
        return tuple(sorted(grants))

    def decide(self, subject: str, permission: str, tenant_id: str | None = None) -> PolicyDecision:
        grants, denies, matched_roles = self._decision_inputs(subject, tenant_id)
        if any(_permission_matches(deny, permission) for deny in denies):
            return PolicyDecision(False, "permission denied by RBAC role assignments", matched_roles)
        if any(_permission_matches(grant, permission) for grant in grants):
            return PolicyDecision(True, "permission granted by assigned role", matched_roles)
        return PolicyDecision(False, "permission denied by RBAC role assignments", matched_roles)

    def _decision_inputs(
        self,
        subject: str,
        tenant_id: str | None,
    ) -> tuple[set[str], set[str], tuple[str, ...]]:
        grants: set[str] = set()
        denies: set[str] = set()
        matched_roles: set[str] = set()
        for role_name, assignment_tenant in self._assignments.get(subject, set()):
            if assignment_tenant not in {None, tenant_id}:
                continue
            self._collect_role(role_name, tenant_id, grants, denies, matched_roles, set())
        return grants, denies, tuple(sorted(matched_roles))

    def _collect_role(
        self,
        role_name: str,
        tenant_id: str | None,
        grants: set[str],
        denies: set[str],
        matched_roles: set[str],
        seen: set[str],
    ) -> None:
        if role_name in seen:
            return
        seen.add(role_name)
        role = self._roles[role_name]
        if role.tenant_id not in {None, tenant_id}:
            return
        matched_roles.add(role_name)
        grants.update(role.permissions)
        denies.update(role.denied_permissions)
        for inherited in role.inherited_roles:
            if inherited in self._roles:
                self._collect_role(inherited, tenant_id, grants, denies, matched_roles, seen)


class ABACAdministration:
    def __init__(self) -> None:
        self._policies: dict[str, AttributePolicy] = {}

    @property
    def policies(self) -> Mapping[str, AttributePolicy]:
        return dict(self._policies)

    def upsert_policy(
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
        policy = AttributePolicy(
            name=name,
            permission=permission,
            required_attributes=dict(required_attributes),
            tenant_id=tenant_id,
            dynamic_conditions=tuple(dynamic_conditions),
            effect=effect,
            client_id=client_id,
        )
        self._policies[name] = policy
        return policy

    def has_relevant_policy(self, permission: str, tenant_id: str | None = None, client_id: str | None = None) -> bool:
        return any(
            _permission_matches(policy.permission, permission)
            and policy.tenant_id in {None, tenant_id}
            and policy.client_id in {None, client_id}
            for policy in self._policies.values()
        )

    def decide(
        self,
        *,
        permission: str,
        attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        client_id: str | None = None,
    ) -> PolicyDecision:
        allow_matches: list[str] = []
        deny_matches: list[str] = []
        for policy in self._policies.values():
            if not _permission_matches(policy.permission, permission):
                continue
            if policy.tenant_id not in {None, tenant_id}:
                continue
            if policy.client_id not in {None, client_id}:
                continue
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


class DelegatedAdministration:
    def __init__(self) -> None:
        self._scopes: dict[str, DelegatedAdminScope] = {}

    @property
    def scopes(self) -> Mapping[str, DelegatedAdminScope]:
        return dict(self._scopes)

    def grant_scope(
        self,
        subject: str,
        *,
        tenant_ids: Iterable[str],
        permissions: Iterable[str],
        visible_client_fields: Iterable[str] = DELEGATED_VISIBLE_CLIENT_FIELDS,
        mutable_client_fields: Iterable[str] = DELEGATED_MUTABLE_CLIENT_FIELDS,
        service_identity_permissions: Iterable[str] = (),
    ) -> DelegatedAdminScope:
        scope = DelegatedAdminScope(
            subject=subject,
            tenant_ids=tuple(sorted(set(tenant_ids))),
            permissions=tuple(sorted(set(permissions))),
            visible_client_fields=tuple(sorted(set(visible_client_fields))),
            mutable_client_fields=tuple(sorted(set(mutable_client_fields))),
            service_identity_permissions=tuple(sorted(set(service_identity_permissions))),
        )
        self._scopes[subject] = scope
        return scope

    def scope_for(self, subject: str) -> DelegatedAdminScope | None:
        return self._scopes.get(subject)

    def authorize(
        self,
        subject: str,
        *,
        tenant_id: str,
        permission: str,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision:
        scope = self._scopes.get(subject)
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

    def visible_tenant_ids(self, subject: str, tenant_ids: Iterable[str]) -> tuple[str, ...]:
        scope = self._scopes.get(subject)
        if scope is None:
            return tuple(sorted(set(tenant_ids)))
        return tuple(sorted(tenant_id for tenant_id in tenant_ids if tenant_id in scope.tenant_ids))

    def visible_client_fields_for(self, subject: str) -> tuple[str, ...]:
        scope = self._scopes.get(subject)
        if scope is None:
            return ADMIN_CLIENT_FIELDS
        return scope.visible_client_fields

    def summary(self) -> dict[str, Any]:
        return {
            "scope_count": len(self._scopes),
            "delegates": sorted(self._scopes),
            "tenant_map": {
                subject: list(scope.tenant_ids)
                for subject, scope in sorted(self._scopes.items())
            },
        }


class PolicyEngine:
    def __init__(
        self,
        *,
        rbac: RBACAdministration | None = None,
        abac: ABACAdministration | None = None,
        delegated_admin: DelegatedAdministration | None = None,
    ) -> None:
        self.rbac = rbac or RBACAdministration()
        self.abac = abac or ABACAdministration()
        self.delegated_admin = delegated_admin or DelegatedAdministration()
        self._audit_events: list[_PolicyAuditEvent] = []

    @property
    def audit_events(self) -> tuple[_PolicyAuditEvent, ...]:
        return tuple(self._audit_events)

    def evaluate(
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
        delegated = self.delegated_admin.authorize(
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
            rbac_decision = self.rbac.decide(subject, permission, tenant_id)

        abac_decision = self.abac.decide(
            permission=permission,
            attributes=attributes,
            tenant_id=tenant_id,
            client_id=client_id,
        )
        requires_abac = self.abac.has_relevant_policy(permission, tenant_id, client_id)

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

    def compliance_report(
        self,
        *,
        service_registry: ServiceIdentityRegistry,
        tenants: Iterable[Mapping[str, Any]],
        clients: Iterable[Mapping[str, Any]],
    ) -> dict[str, Any]:
        tenant_ids = [str(tenant["id"]) for tenant in tenants if "id" in tenant]
        return build_compliance_report(
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


def simulate_policy(
    *,
    rbac: RBACAdministration,
    abac: ABACAdministration,
    subject: str,
    permission: str,
    attributes: Mapping[str, Any],
    tenant_id: str | None = None,
    client_id: str | None = None,
) -> PolicyDecision:
    tenant = tenant_id or str(attributes.get("tenant_id") or "")
    engine = PolicyEngine(rbac=rbac, abac=abac)
    if tenant:
        return engine.evaluate(
            subject=subject,
            permission=permission,
            tenant_id=tenant,
            attributes=attributes,
            client_id=client_id,
        )
    rbac_decision = rbac.decide(subject, permission, tenant_id)
    abac_decision = abac.decide(permission=permission, attributes=attributes, tenant_id=tenant_id, client_id=client_id)
    if rbac_decision.allowed and abac_decision.allowed:
        return PolicyDecision(
            True,
            "permission granted by RBAC assignment and ABAC attributes",
            rbac_decision.matched + abac_decision.matched,
        )
    reasons = [rbac_decision.reason, abac_decision.reason]
    return PolicyDecision(False, "; ".join(reasons), rbac_decision.matched + abac_decision.matched)


def filter_visible_tenants(
    tenants: Iterable[Mapping[str, Any]],
    *,
    subject: str,
    delegated_admin: DelegatedAdministration | None = None,
) -> list[dict[str, Any]]:
    tenants_list = [dict(tenant) for tenant in tenants]
    if delegated_admin is None:
        return tenants_list
    visible_ids = set(delegated_admin.visible_tenant_ids(subject, (str(tenant.get("id")) for tenant in tenants_list)))
    return [tenant for tenant in tenants_list if str(tenant.get("id")) in visible_ids]


def expose_client_record(
    client: Mapping[str, Any],
    *,
    plane: str,
    subject: str | None = None,
    delegated_admin: DelegatedAdministration | None = None,
) -> dict[str, Any]:
    if plane == "public":
        return _pick_fields(client, PUBLIC_CLIENT_FIELDS)
    if plane != "admin":
        raise ValueError(f"unsupported exposure plane {plane!r}")
    if delegated_admin is not None and subject is not None and delegated_admin.scope_for(subject) is not None:
        return _pick_fields(client, delegated_admin.visible_client_fields_for(subject))
    return _pick_fields(client, ADMIN_CLIENT_FIELDS)


def assert_client_mutation_authority(
    *,
    subject: str,
    tenant_id: str,
    patch: Mapping[str, Any],
    delegated_admin: DelegatedAdministration | None = None,
) -> None:
    patch_fields = tuple(sorted(set(patch)))
    if "tenant_id" in patch and patch["tenant_id"] != tenant_id:
        raise PermissionError("tenant mutation is not allowed")
    if delegated_admin is None:
        return
    decision = delegated_admin.authorize(
        subject,
        tenant_id=tenant_id,
        permission="client.update",
        patch_fields=patch_fields,
    )
    if not decision.allowed:
        raise PermissionError(decision.reason)


def build_compliance_report(
    *,
    service_registry: ServiceIdentityRegistry,
    rbac: RBACAdministration,
    abac: ABACAdministration,
    delegated_admin: DelegatedAdministration,
    audit_events: Iterable[_PolicyAuditEvent],
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
    "ADMIN_CLIENT_FIELDS",
    "AttributePolicy",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "DelegatedAdministration",
    "DynamicCondition",
    "PUBLIC_CLIENT_FIELDS",
    "PolicyDecision",
    "PolicyEngine",
    "RBACAdministration",
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
