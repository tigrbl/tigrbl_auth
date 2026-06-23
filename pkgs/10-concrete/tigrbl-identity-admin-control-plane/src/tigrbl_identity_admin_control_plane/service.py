"""Admin control-plane service implementation."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Iterable, Mapping

from tigrbl_identity_contracts.audit.admin import AdminAuditEvent as _AdminAuditEvent
from tigrbl_identity_contracts.credentials import Credential, CredentialKind
from tigrbl_identity_contracts.policy.definitions import PolicyDefinition
from tigrbl_identity_contracts.principals import Principal, PrincipalKind

from .models import (
    AdminControlPlaneError,
    AdminResource,
    AdminResourceKind,
    AdminResourceStatus,
    App,
    _clean_tuple,
    _new_id,
    _utc_now,
)


class AdminControlPlane:
    def __init__(self) -> None:
        self._metadata: dict[AdminResourceKind, dict[str, AdminResource]] = {
            kind: {} for kind in AdminResourceKind
        }
        self._objects: dict[AdminResourceKind, dict[str, object]] = {
            kind: {} for kind in AdminResourceKind
        }
        self._audit_events: list[_AdminAuditEvent] = []

    @property
    def audit_events(self) -> tuple[_AdminAuditEvent, ...]:
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
    ) -> Principal:
        principal = Principal(
            id=_new_id("principal"),
            kind=PrincipalKind(principal_kind),
            subject=subject,
            tenant_id=tenant_id,
            display_name=name,
            roles=_clean_tuple(roles),
            attributes=dict(attributes or {}),
        )
        metadata = self._metadata_for(principal.id, AdminResourceKind.PRINCIPAL, tenant_id, name)
        return self._create(metadata, principal, actor=actor)

    def create_credential(
        self,
        *,
        actor: str,
        tenant_id: str,
        principal_id: str,
        name: str,
        credential_kind: str,
        attributes: Mapping[str, Any] | None = None,
    ) -> Credential:
        self._require(AdminResourceKind.PRINCIPAL, principal_id, tenant_id=tenant_id)
        credential = Credential(
            id=_new_id("credential"),
            principal_id=principal_id,
            kind=CredentialKind(credential_kind),
            metadata=dict(attributes or {}),
        )
        metadata = self._metadata_for(credential.id, AdminResourceKind.CREDENTIAL, tenant_id, name)
        return self._create(metadata, credential, actor=actor)

    def create_app(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        client_ids: Iterable[str],
        owner_principal_id: str | None = None,
    ) -> App:
        if owner_principal_id:
            self._require(AdminResourceKind.PRINCIPAL, owner_principal_id, tenant_id=tenant_id)
        app = App(
            id=_new_id("app"),
            tenant_id=tenant_id,
            name=name,
            client_ids=_clean_tuple(client_ids),
            owner_principal_id=owner_principal_id,
        )
        metadata = self._metadata_for(app.id, AdminResourceKind.APP, tenant_id, name)
        return self._create(metadata, app, actor=actor)

    def create_service_identity(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        scopes: Iterable[str],
        owner_principal_id: str | None = None,
    ) -> Principal:
        if owner_principal_id:
            self._require(AdminResourceKind.PRINCIPAL, owner_principal_id, tenant_id=tenant_id)
        service = Principal(
            id=_new_id("service"),
            kind=PrincipalKind.SERVICE,
            subject=f"service:{name}",
            tenant_id=tenant_id,
            display_name=name,
            attributes={
                "owner_principal_id": owner_principal_id,
                "scopes": _clean_tuple(scopes),
            },
        )
        metadata = self._metadata_for(service.id, AdminResourceKind.SERVICE_IDENTITY, tenant_id, name)
        return self._create(metadata, service, actor=actor)

    def create_resource_server(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        audience: str,
        scopes: Iterable[str],
    ) -> AdminResource:
        if not audience:
            raise ValueError("resource server audience is required")
        metadata = self._metadata_for(
            _new_id("rs"),
            AdminResourceKind.RESOURCE_SERVER,
            tenant_id,
            name,
            attributes={"audience": audience, "scopes": _clean_tuple(scopes)},
        )
        return self._create(metadata, metadata, actor=actor)

    def create_policy(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        policy_kind: str,
        rules: Mapping[str, Any],
        version: int = 1,
    ) -> PolicyDefinition:
        if version <= 0:
            raise ValueError("policy version must be positive")
        policy = PolicyDefinition(
            policy_id=_new_id("policy"),
            name=name,
            tenant_id=tenant_id,
            language=policy_kind,
            created_at=_utc_now(),
        )
        metadata = self._metadata_for(
            policy.policy_id,
            AdminResourceKind.POLICY,
            tenant_id,
            name,
            attributes={"rules": dict(rules), "version": version},
        )
        return self._create(metadata, policy, actor=actor)

    def get(self, kind: AdminResourceKind | str, resource_id: str, *, tenant_id: str) -> object:
        metadata = self._require(AdminResourceKind(kind), resource_id, tenant_id=tenant_id)
        return self._objects[metadata.kind][resource_id]

    def metadata(self, kind: AdminResourceKind | str, resource_id: str, *, tenant_id: str) -> AdminResource:
        return self._require(AdminResourceKind(kind), resource_id, tenant_id=tenant_id)

    def list(self, kind: AdminResourceKind | str, *, tenant_id: str) -> tuple[object, ...]:
        resource_kind = AdminResourceKind(kind)
        return tuple(
            self._objects[resource_kind][metadata.id]
            for metadata in sorted(
                (
                    resource
                    for resource in self._metadata[resource_kind].values()
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
    ) -> object:
        resource_kind = AdminResourceKind(kind)
        metadata = self._require(resource_kind, resource_id, tenant_id=tenant_id)
        updated_metadata = replace(
            metadata,
            name=name if name is not None else metadata.name,
            attributes=dict(attributes) if attributes is not None else metadata.attributes,
            status=AdminResourceStatus(status) if status is not None else metadata.status,
            updated_at=_utc_now(),
        )
        current = self._objects[resource_kind][resource_id]
        updated = self._replace_object(current, name=name, attributes=attributes)
        self._metadata[resource_kind][resource_id] = updated_metadata
        self._objects[resource_kind][resource_id] = updated
        self._record(actor, "update", updated_metadata, "ok")
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
        metadata = self._require(resource_kind, resource_id, tenant_id=tenant_id)
        deleted = replace(metadata, status=AdminResourceStatus.DELETED, updated_at=_utc_now())
        self._metadata[resource_kind][resource_id] = deleted
        self._record(actor, "delete", deleted, "ok")
        return deleted

    def _metadata_for(
        self,
        resource_id: str,
        kind: AdminResourceKind,
        tenant_id: str,
        name: str,
        *,
        attributes: Mapping[str, Any] | None = None,
    ) -> AdminResource:
        return AdminResource(
            id=resource_id,
            kind=kind,
            tenant_id=tenant_id,
            name=name,
            attributes=dict(attributes or {}),
        )

    def _create(self, metadata: AdminResource, resource: object, *, actor: str) -> Any:
        self._metadata[metadata.kind][metadata.id] = metadata
        self._objects[metadata.kind][metadata.id] = resource
        self._record(actor, "create", metadata, "ok")
        return resource

    def _require(self, kind: AdminResourceKind, resource_id: str, *, tenant_id: str) -> AdminResource:
        resource = self._metadata[kind].get(resource_id)
        if resource is None or resource.status == AdminResourceStatus.DELETED:
            raise AdminControlPlaneError(f"{kind.value} resource not found")
        if resource.tenant_id != tenant_id:
            raise AdminControlPlaneError("resource tenant mismatch")
        return resource

    def _replace_object(
        self,
        resource: object,
        *,
        name: str | None,
        attributes: Mapping[str, Any] | None,
    ) -> object:
        if isinstance(resource, Principal):
            return replace(
                resource,
                display_name=name if name is not None else resource.display_name,
                attributes=dict(attributes) if attributes is not None else resource.attributes,
            )
        if isinstance(resource, App):
            return replace(
                resource,
                name=name if name is not None else resource.name,
                attributes=dict(attributes) if attributes is not None else resource.attributes,
            )
        if isinstance(resource, PolicyDefinition):
            return replace(resource, name=name if name is not None else resource.name)
        if isinstance(resource, AdminResource):
            return replace(
                resource,
                name=name if name is not None else resource.name,
                attributes=dict(attributes) if attributes is not None else resource.attributes,
            )
        return resource

    def _record(self, actor: str, action: str, resource: AdminResource, outcome: str) -> None:
        self._audit_events.append(
            _AdminAuditEvent(
                event_id=_new_id("audit"),
                actor=actor,
                action=action,
                resource_kind=resource.kind,
                resource_id=resource.id,
                tenant_id=resource.tenant_id,
                outcome=outcome,
            )
        )


__all__ = ["AdminControlPlane"]
