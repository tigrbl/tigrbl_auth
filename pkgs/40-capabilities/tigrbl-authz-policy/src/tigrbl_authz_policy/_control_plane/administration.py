from __future__ import annotations

from typing import Any, Iterable, Mapping
from uuid import uuid4

from .models import *
from .models import _permission_matches, _utc_now

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
            created_at=_utc_now(),
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


