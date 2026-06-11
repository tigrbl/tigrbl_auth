from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable, Mapping

from .models import (
    AdminAuditEvent,
    AdminControlPlaneError,
    AdminResource,
    AdminResourceKind,
    AdminResourceStatus,
    AdminUiState,
    AdminUiView,
    AppRecord,
    CredentialRecord,
    PolicyRecord,
    PrincipalRecord,
    ResourceServerRecord,
    ServiceIdentityRecord,
    _clean_tuple,
    _new_id,
    _utc_now,
)


class AdminControlPlane:
    def __init__(self) -> None:
        self._resources: dict[AdminResourceKind, dict[str, AdminResource]] = {
            kind: {} for kind in AdminResourceKind
        }
        self._audit_events: list[AdminAuditEvent] = []

    @property
    def audit_events(self) -> tuple[AdminAuditEvent, ...]:
        return tuple(self._audit_events)

    def create_principal(
        self,
        *,
        actor: str,
        tenant_id: str,
        subject: str,
        name: str,
        principal_kind: str = "user",
        roles: Iterable[str] = (),
        attributes: Mapping[str, Any] | None = None,
    ) -> PrincipalRecord:
        return self._create(
            PrincipalRecord(
                id=_new_id("principal"),
                kind=AdminResourceKind.PRINCIPAL,
                tenant_id=tenant_id,
                subject=subject,
                name=name,
                principal_kind=principal_kind,
                roles=_clean_tuple(roles),
                attributes=dict(attributes or {}),
            ),
            actor=actor,
        )

    def create_credential(
        self,
        *,
        actor: str,
        tenant_id: str,
        principal_id: str,
        name: str,
        credential_kind: str,
        attributes: Mapping[str, Any] | None = None,
    ) -> CredentialRecord:
        self._require(AdminResourceKind.PRINCIPAL, principal_id, tenant_id=tenant_id)
        return self._create(
            CredentialRecord(
                id=_new_id("credential"),
                kind=AdminResourceKind.CREDENTIAL,
                tenant_id=tenant_id,
                principal_id=principal_id,
                name=name,
                credential_kind=credential_kind,
                attributes=dict(attributes or {}),
            ),
            actor=actor,
        )

    def create_app(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        client_ids: Iterable[str],
        owner_principal_id: str | None = None,
    ) -> AppRecord:
        if owner_principal_id:
            self._require(AdminResourceKind.PRINCIPAL, owner_principal_id, tenant_id=tenant_id)
        return self._create(
            AppRecord(
                id=_new_id("app"),
                kind=AdminResourceKind.APP,
                tenant_id=tenant_id,
                name=name,
                client_ids=_clean_tuple(client_ids),
                owner_principal_id=owner_principal_id,
            ),
            actor=actor,
        )

    def create_service_identity(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        scopes: Iterable[str],
        owner_principal_id: str | None = None,
    ) -> ServiceIdentityRecord:
        if owner_principal_id:
            self._require(AdminResourceKind.PRINCIPAL, owner_principal_id, tenant_id=tenant_id)
        return self._create(
            ServiceIdentityRecord(
                id=_new_id("service"),
                kind=AdminResourceKind.SERVICE_IDENTITY,
                tenant_id=tenant_id,
                name=name,
                scopes=_clean_tuple(scopes),
                owner_principal_id=owner_principal_id,
            ),
            actor=actor,
        )

    def create_resource_server(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        audience: str,
        scopes: Iterable[str],
    ) -> ResourceServerRecord:
        return self._create(
            ResourceServerRecord(
                id=_new_id("rs"),
                kind=AdminResourceKind.RESOURCE_SERVER,
                tenant_id=tenant_id,
                name=name,
                audience=audience,
                scopes=_clean_tuple(scopes),
            ),
            actor=actor,
        )

    def create_policy(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        policy_kind: str,
        rules: Mapping[str, Any],
        version: int = 1,
    ) -> PolicyRecord:
        return self._create(
            PolicyRecord(
                id=_new_id("policy"),
                kind=AdminResourceKind.POLICY,
                tenant_id=tenant_id,
                name=name,
                policy_kind=policy_kind,
                rules=dict(rules),
                version=version,
            ),
            actor=actor,
        )

    def get(self, kind: AdminResourceKind | str, resource_id: str, *, tenant_id: str) -> AdminResource:
        return self._require(AdminResourceKind(kind), resource_id, tenant_id=tenant_id)

    def list(self, kind: AdminResourceKind | str, *, tenant_id: str) -> tuple[AdminResource, ...]:
        resource_kind = AdminResourceKind(kind)
        return tuple(
            sorted(
                (
                    resource
                    for resource in self._resources[resource_kind].values()
                    if resource.tenant_id == tenant_id and resource.status != AdminResourceStatus.DELETED
                ),
                key=lambda resource: (resource.name, resource.id),
            )
        )

    def update(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        actor: str,
        tenant_id: str,
        name: str | None = None,
        attributes: Mapping[str, Any] | None = None,
        status: AdminResourceStatus | str | None = None,
    ) -> AdminResource:
        resource_kind = AdminResourceKind(kind)
        resource = self._require(resource_kind, resource_id, tenant_id=tenant_id)
        updated = replace(
            resource,
            name=name if name is not None else resource.name,
            attributes=dict(attributes) if attributes is not None else resource.attributes,
            status=AdminResourceStatus(status) if status is not None else resource.status,
            updated_at=_utc_now(),
        )
        self._resources[resource_kind][resource_id] = updated
        self._record(actor, "update", updated, "ok")
        return updated

    def delete(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        actor: str,
        tenant_id: str,
    ) -> AdminResource:
        resource_kind = AdminResourceKind(kind)
        resource = self._require(resource_kind, resource_id, tenant_id=tenant_id)
        deleted = replace(resource, status=AdminResourceStatus.DELETED, updated_at=_utc_now())
        self._resources[resource_kind][resource_id] = deleted
        self._record(actor, "delete", deleted, "ok")
        return deleted

    def render_uix_view(
        self,
        kind: AdminResourceKind | str,
        *,
        tenant_id: str,
        loading: bool = False,
        error: str | None = None,
    ) -> AdminUiView:
        resource_kind = AdminResourceKind(kind)
        if loading:
            return AdminUiView(AdminUiState.LOADING, resource_kind)
        if error:
            return AdminUiView(AdminUiState.ERROR, resource_kind, error=error)
        rows = self.list(resource_kind, tenant_id=tenant_id)
        if not rows:
            return AdminUiView(AdminUiState.EMPTY, resource_kind)
        return AdminUiView(AdminUiState.READY, resource_kind, rows=rows)

    def _create(self, resource: AdminResource, *, actor: str) -> Any:
        self._resources[resource.kind][resource.id] = resource
        self._record(actor, "create", resource, "ok")
        return resource

    def _require(self, kind: AdminResourceKind, resource_id: str, *, tenant_id: str) -> AdminResource:
        resource = self._resources[kind].get(resource_id)
        if resource is None or resource.status == AdminResourceStatus.DELETED:
            raise AdminControlPlaneError(f"{kind.value} resource not found")
        if resource.tenant_id != tenant_id:
            raise AdminControlPlaneError("resource tenant mismatch")
        return resource

    def _record(self, actor: str, action: str, resource: AdminResource, outcome: str) -> None:
        self._audit_events.append(
            AdminAuditEvent(
                event_id=_new_id("audit"),
                actor=actor,
                action=action,
                resource_kind=resource.kind,
                resource_id=resource.id,
                tenant_id=resource.tenant_id,
                outcome=outcome,
            )
        )
