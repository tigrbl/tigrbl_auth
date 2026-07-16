from __future__ import annotations

from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.authentication import ServiceIdentityAuthentication
from tigrbl_identity_credentials_concrete import ServiceCredential
from tigrbl_identity_identities_concrete import ServiceIdentity


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
            raise ValueError(
                "service identity requires service_id, tenant_id, and name"
            )
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
        credential = next(
            (item for item in self._credentials.values() if item.raw_key == raw_key),
            None,
        )
        if credential is None:
            raise PermissionError("unknown service credential")
        if credential.revoked:
            raise PermissionError("service credential is revoked")
        service = self._services.get(credential.service_id)
        if service is None or not service.enabled:
            raise PermissionError("service identity is inactive")
        if service.tenant_id != tenant_id:
            raise PermissionError("service identity tenant mismatch")
        if required_permission and not any(
            _permission_matches(scope, required_permission) for scope in service.scopes
        ):
            raise PermissionError(
                "service identity scope does not authorize requested permission"
            )
        return ServiceIdentityAuthentication(
            service=service,
            credential_id=credential.credential_id,
            granted_permissions=service.scopes,
        )

    def summary(self) -> dict[str, Any]:
        active_services = [
            service for service in self._services.values() if service.enabled
        ]
        active_credentials = [
            credential
            for credential in self._credentials.values()
            if not credential.revoked
        ]
        return {
            "service_count": len(self._services),
            "active_service_count": len(active_services),
            "active_credential_count": len(active_credentials),
            "tenants": sorted(
                {service.tenant_id for service in self._services.values()}
            ),
        }


__all__ = [
    "ServiceCredential",
    "ServiceIdentity",
    "ServiceIdentityAuthentication",
    "ServiceIdentityRegistry",
]
