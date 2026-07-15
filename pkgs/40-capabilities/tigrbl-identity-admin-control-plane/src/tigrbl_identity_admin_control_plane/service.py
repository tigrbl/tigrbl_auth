"""Administrative use cases over injected durable table operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable, Iterable, Mapping
from dataclasses import replace
from typing import Any, TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.audit.admin import AdminAuditEvent
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)
from tigrbl_identity_contracts.credentials import Credential, CredentialKind
from tigrbl_identity_contracts.policy.definitions import PolicyDefinition
from tigrbl_identity_contracts.principals import Principal, PrincipalKind

from .models import (
    AdminControlPlaneError,
    AdminResource,
    AdminResourceKind,
    AdminResourceRecord,
    AdminResourceStatus,
    App,
    _clean_tuple,
    _new_id,
    _utc_now,
)

AdminCreateOperation: TypeAlias = Callable[[AdminResourceRecord], object]
AdminReadOperation: TypeAlias = Callable[[AdminResourceKind, str], object]
AdminListOperation: TypeAlias = Callable[[AdminResourceKind, str], object]
AdminUpdateOperation: TypeAlias = Callable[[AdminResourceRecord], object]
AdminDeleteOperation: TypeAlias = Callable[[AdminResourceRecord], object]
AdminAuditOperation: TypeAlias = Callable[[AdminAuditEvent], object]
AdminAuditListOperation: TypeAlias = Callable[[], object]


async def _resolve(value):
    return await value if inspect.isawaitable(value) else value


class AdminControlPlane(Capability):
    def __init__(
        self,
        creator: AdminCreateOperation,
        reader: AdminReadOperation,
        lister: AdminListOperation,
        updater: AdminUpdateOperation,
        deleter: AdminDeleteOperation,
        audit_recorder: AdminAuditOperation,
        audit_lister: AdminAuditListOperation,
    ) -> None:
        self._creator = creator
        self._reader = reader
        self._lister = lister
        self._updater = updater
        self._deleter = deleter
        self._audit_recorder = audit_recorder
        self._audit_lister = audit_lister
        operation_names = (
            "create_principal",
            "create_credential",
            "create_app",
            "create_service_identity",
            "create_resource_server",
            "create_policy",
            "get",
            "metadata",
            "list",
            "update",
            "delete",
            "list_audit_events",
        )
        super().__init__(
            CapabilityDefinition(
                capability_id="identity-admin.control-plane",
                version="1.0",
            ),
            operations={
                name: CapabilityOperation(
                    target=getattr(self, name),
                    delegated=True,
                )
                for name in operation_names
            },
        )

    async def create_principal(
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
        metadata = self._metadata_for(
            principal.id,
            AdminResourceKind.PRINCIPAL,
            tenant_id,
            name,
        )
        return await self._create(metadata, principal, actor=actor)

    async def create_credential(
        self,
        *,
        actor: str,
        tenant_id: str,
        principal_id: str,
        name: str,
        credential_kind: str,
        attributes: Mapping[str, Any] | None = None,
    ) -> Credential:
        await self._require(
            AdminResourceKind.PRINCIPAL,
            principal_id,
            tenant_id=tenant_id,
        )
        credential = Credential(
            id=_new_id("credential"),
            principal_id=principal_id,
            kind=CredentialKind(credential_kind),
            metadata=dict(attributes or {}),
        )
        metadata = self._metadata_for(
            credential.id,
            AdminResourceKind.CREDENTIAL,
            tenant_id,
            name,
        )
        return await self._create(metadata, credential, actor=actor)

    async def create_app(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        client_ids: Iterable[str],
        owner_principal_id: str | None = None,
    ) -> App:
        if owner_principal_id:
            await self._require(
                AdminResourceKind.PRINCIPAL,
                owner_principal_id,
                tenant_id=tenant_id,
            )
        app = App(
            id=_new_id("app"),
            tenant_id=tenant_id,
            name=name,
            client_ids=_clean_tuple(client_ids),
            owner_principal_id=owner_principal_id,
        )
        metadata = self._metadata_for(
            app.id,
            AdminResourceKind.APP,
            tenant_id,
            name,
        )
        return await self._create(metadata, app, actor=actor)

    async def create_service_identity(
        self,
        *,
        actor: str,
        tenant_id: str,
        name: str,
        scopes: Iterable[str],
        owner_principal_id: str | None = None,
    ) -> Principal:
        if owner_principal_id:
            await self._require(
                AdminResourceKind.PRINCIPAL,
                owner_principal_id,
                tenant_id=tenant_id,
            )
        service = Principal(
            id=_new_id("service"),
            kind=PrincipalKind.SERVICE_IDENTITY,
            subject=f"service:{name}",
            tenant_id=tenant_id,
            display_name=name,
            attributes={
                "owner_principal_id": owner_principal_id,
                "scopes": _clean_tuple(scopes),
            },
        )
        metadata = self._metadata_for(
            service.id,
            AdminResourceKind.SERVICE_IDENTITY,
            tenant_id,
            name,
        )
        return await self._create(metadata, service, actor=actor)

    async def create_resource_server(
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
        return await self._create(metadata, metadata, actor=actor)

    async def create_policy(
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
        return await self._create(metadata, policy, actor=actor)

    async def get(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        tenant_id: str,
    ) -> object:
        return (await self._require(kind, resource_id, tenant_id=tenant_id)).resource

    async def metadata(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        tenant_id: str,
    ) -> AdminResource:
        return (await self._require(kind, resource_id, tenant_id=tenant_id)).metadata

    async def list(
        self,
        kind: AdminResourceKind | str,
        *,
        tenant_id: str,
    ) -> tuple[object, ...]:
        resource_kind = AdminResourceKind(kind)
        records = tuple(await _resolve(self._lister(resource_kind, tenant_id)))
        self._validate_records(records)
        visible = (
            record
            for record in records
            if record.metadata.kind == resource_kind
            and record.metadata.tenant_id == tenant_id
            and record.metadata.status != AdminResourceStatus.DELETED
        )
        return tuple(
            record.resource
            for record in sorted(
                visible,
                key=lambda record: (record.metadata.name, record.metadata.id),
            )
        )

    async def update(
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
        record = await self._require(kind, resource_id, tenant_id=tenant_id)
        metadata = record.metadata
        updated_metadata = replace(
            metadata,
            name=name if name is not None else metadata.name,
            attributes=(
                dict(attributes) if attributes is not None else metadata.attributes
            ),
            status=(
                AdminResourceStatus(status) if status is not None else metadata.status
            ),
            updated_at=_utc_now(),
        )
        updated = self._replace_object(
            record.resource,
            name=name,
            attributes=attributes,
        )
        await _resolve(self._updater(AdminResourceRecord(updated_metadata, updated)))
        await self._record(actor, "update", updated_metadata, "ok")
        return updated

    async def delete(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        actor: str,
        tenant_id: str,
    ) -> AdminResource:
        record = await self._require(kind, resource_id, tenant_id=tenant_id)
        deleted = replace(
            record.metadata,
            status=AdminResourceStatus.DELETED,
            updated_at=_utc_now(),
        )
        await _resolve(self._deleter(AdminResourceRecord(deleted, record.resource)))
        await self._record(actor, "delete", deleted, "ok")
        return deleted

    async def list_audit_events(self) -> tuple[AdminAuditEvent, ...]:
        events = tuple(await _resolve(self._audit_lister()))
        if not all(isinstance(event, AdminAuditEvent) for event in events):
            raise TypeError("admin audit operation returned an invalid event")
        return events

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

    async def _create(
        self,
        metadata: AdminResource,
        resource: object,
        *,
        actor: str,
    ) -> Any:
        await _resolve(self._creator(AdminResourceRecord(metadata, resource)))
        await self._record(actor, "create", metadata, "ok")
        return resource

    async def _require(
        self,
        kind: AdminResourceKind | str,
        resource_id: str,
        *,
        tenant_id: str,
    ) -> AdminResourceRecord:
        resource_kind = AdminResourceKind(kind)
        value = await _resolve(self._reader(resource_kind, resource_id))
        if value is None:
            raise AdminControlPlaneError(f"{resource_kind.value} resource not found")
        if not isinstance(value, AdminResourceRecord):
            raise TypeError("admin read operation returned an invalid record")
        if value.metadata.status == AdminResourceStatus.DELETED:
            raise AdminControlPlaneError(f"{resource_kind.value} resource not found")
        if value.metadata.kind != resource_kind:
            raise AdminControlPlaneError("resource kind mismatch")
        if value.metadata.tenant_id != tenant_id:
            raise AdminControlPlaneError("resource tenant mismatch")
        return value

    @staticmethod
    def _validate_records(records: tuple[object, ...]) -> None:
        if not all(isinstance(record, AdminResourceRecord) for record in records):
            raise TypeError("admin list operation returned an invalid record")

    @staticmethod
    def _replace_object(
        resource: object,
        *,
        name: str | None,
        attributes: Mapping[str, Any] | None,
    ) -> object:
        if isinstance(resource, Principal):
            return replace(
                resource,
                display_name=name if name is not None else resource.display_name,
                attributes=(
                    dict(attributes) if attributes is not None else resource.attributes
                ),
            )
        if isinstance(resource, App):
            return replace(
                resource,
                name=name if name is not None else resource.name,
                attributes=(
                    dict(attributes) if attributes is not None else resource.attributes
                ),
            )
        if isinstance(resource, PolicyDefinition):
            return replace(resource, name=name if name is not None else resource.name)
        if isinstance(resource, AdminResource):
            return replace(
                resource,
                name=name if name is not None else resource.name,
                attributes=(
                    dict(attributes) if attributes is not None else resource.attributes
                ),
            )
        return resource

    async def _record(
        self,
        actor: str,
        action: str,
        resource: AdminResource,
        outcome: str,
    ) -> None:
        await _resolve(
            self._audit_recorder(
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
        )


__all__ = [
    "AdminAuditListOperation",
    "AdminAuditOperation",
    "AdminControlPlane",
    "AdminCreateOperation",
    "AdminDeleteOperation",
    "AdminListOperation",
    "AdminReadOperation",
    "AdminUpdateOperation",
]
