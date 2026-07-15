"""Administrative resource creation operations for the control-plane capability."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from tigrbl_identity_contracts.credentials import Credential, CredentialKind
from tigrbl_identity_contracts.policy.definitions import PolicyDefinition
from tigrbl_identity_contracts.principals import Principal, PrincipalKind

from .models import AdminResourceKind, App, _clean_tuple, _new_id, _utc_now


class AdminCreationOperations:
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
            principal.id, AdminResourceKind.PRINCIPAL, tenant_id, name
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
            AdminResourceKind.PRINCIPAL, principal_id, tenant_id=tenant_id
        )
        credential = Credential(
            id=_new_id("credential"),
            principal_id=principal_id,
            kind=CredentialKind(credential_kind),
            metadata=dict(attributes or {}),
        )
        metadata = self._metadata_for(
            credential.id, AdminResourceKind.CREDENTIAL, tenant_id, name
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
        metadata = self._metadata_for(app.id, AdminResourceKind.APP, tenant_id, name)
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
            service.id, AdminResourceKind.SERVICE_IDENTITY, tenant_id, name
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
    ):
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


__all__ = ["AdminCreationOperations"]
