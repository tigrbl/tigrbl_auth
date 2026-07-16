"""Realm-administration capability over injected durable operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.admin_realms import (
    AdminRealm,
    AdminRealmCreate,
    AdminRealmUpdate,
    RealmAdministrationNotFoundError,
    RealmAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenant,
    AdminTenantCreate,
    PlatformAdministrator,
    TenantAdministrationPolicyError,
)
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


RealmListOperation: TypeAlias = Callable[[], object]
RealmCreateOperation: TypeAlias = Callable[[AdminRealmCreate], object]
RealmReadOperation: TypeAlias = Callable[[str], object]
RealmUpdateOperation: TypeAlias = Callable[[str, AdminRealmUpdate], object]
RealmDeleteOperation: TypeAlias = Callable[[str], object]
RealmTenantListOperation: TypeAlias = Callable[[PlatformAdministrator, str], object]
RealmTenantCreateOperation: TypeAlias = Callable[
    [PlatformAdministrator, AdminTenantCreate], object
]


async def _resolve(value: object) -> object:
    return await value if inspect.isawaitable(value) else value


class RealmAdministrationCapability(Capability):
    def __init__(
        self,
        *,
        lister: RealmListOperation,
        creator: RealmCreateOperation,
        reader: RealmReadOperation,
        updater: RealmUpdateOperation,
        deleter: RealmDeleteOperation,
        tenant_lister: RealmTenantListOperation,
        tenant_creator: RealmTenantCreateOperation,
    ) -> None:
        delegates = {
            "list_realms": lister,
            "create_realm": creator,
            "read_realm": reader,
            "update_realm": updater,
            "delete_realm": deleter,
            "list_realm_tenants": tenant_lister,
            "create_realm_tenant": tenant_creator,
        }
        invalid = tuple(
            sorted(name for name, target in delegates.items() if not callable(target))
        )
        if invalid:
            raise TypeError(
                f"realm administration delegates must be callable: {invalid}"
            )
        self._lister = lister
        self._creator = creator
        self._reader = reader
        self._updater = updater
        self._deleter = deleter
        self._tenant_lister = tenant_lister
        self._tenant_creator = tenant_creator
        super().__init__(
            CapabilityDefinition("identity-admin.realms", "1.0"),
            operations={
                name: CapabilityOperation(target=getattr(self, name), delegated=True)
                for name in delegates
            },
        )

    @staticmethod
    def _require_superuser(actor: PlatformAdministrator) -> None:
        if not isinstance(actor, PlatformAdministrator) or not actor.is_superuser:
            raise TenantAdministrationPolicyError("superuser privileges are required")

    async def list_realms(self, actor: PlatformAdministrator) -> tuple[AdminRealm, ...]:
        self._require_superuser(actor)
        realms = tuple(await _resolve(self._lister()))
        if not all(isinstance(realm, AdminRealm) for realm in realms):
            raise TypeError("realm lister returned an invalid record")
        return tuple(
            sorted(
                realms, key=lambda item: (item.created_at or "", item.name, item.slug)
            )
        )

    async def create_realm(
        self, actor: PlatformAdministrator, spec: AdminRealmCreate
    ) -> AdminRealm:
        self._require_superuser(actor)
        realm = await _resolve(self._creator(spec))
        if not isinstance(realm, AdminRealm):
            raise TypeError("realm creator returned an invalid record")
        return realm

    async def read_realm(
        self, actor: PlatformAdministrator, realm_id: str
    ) -> AdminRealm | None:
        self._require_superuser(actor)
        realm = await _resolve(self._reader(realm_id))
        if realm is not None and not isinstance(realm, AdminRealm):
            raise TypeError("realm reader returned an invalid record")
        return realm

    async def update_realm(
        self,
        actor: PlatformAdministrator,
        realm_id: str,
        spec: AdminRealmUpdate,
    ) -> AdminRealm:
        self._require_superuser(actor)
        realm = await _resolve(self._updater(realm_id, spec))
        if not isinstance(realm, AdminRealm):
            raise TypeError("realm updater returned an invalid record")
        return realm

    async def delete_realm(
        self, actor: PlatformAdministrator, realm_id: str
    ) -> AdminRealm:
        self._require_superuser(actor)
        realm = await self.read_realm(actor, realm_id)
        if realm is None:
            raise RealmAdministrationNotFoundError("realm not found")
        tenants = tuple(await _resolve(self._tenant_lister(actor, realm_id)))
        if tenants:
            raise RealmAdministrationValidationError(
                "cannot delete a realm that still owns tenants"
            )
        deleted = await _resolve(self._deleter(realm_id))
        if not isinstance(deleted, AdminRealm):
            raise TypeError("realm deleter returned an invalid record")
        return deleted

    async def list_realm_tenants(
        self, actor: PlatformAdministrator, realm_id: str
    ) -> tuple[AdminTenant, ...]:
        self._require_superuser(actor)
        if await self.read_realm(actor, realm_id) is None:
            raise RealmAdministrationNotFoundError("realm not found")
        tenants = tuple(await _resolve(self._tenant_lister(actor, realm_id)))
        if not all(isinstance(tenant, AdminTenant) for tenant in tenants):
            raise TypeError("realm tenant lister returned an invalid record")
        return tuple(
            sorted(
                tenants, key=lambda item: (item.created_at or "", item.name, item.slug)
            )
        )

    async def create_realm_tenant(
        self,
        actor: PlatformAdministrator,
        realm_id: str,
        spec: AdminTenantCreate,
    ) -> AdminTenant:
        self._require_superuser(actor)
        if await self.read_realm(actor, realm_id) is None:
            raise RealmAdministrationNotFoundError("realm not found")
        effective = AdminTenantCreate(
            realm_id=realm_id,
            slug=spec.slug,
            name=spec.name,
            email=spec.email,
        )
        tenant = await _resolve(self._tenant_creator(actor, effective))
        if not isinstance(tenant, AdminTenant):
            raise TypeError("realm tenant creator returned an invalid record")
        return tenant


__all__ = [
    "RealmAdministrationCapability",
    "RealmCreateOperation",
    "RealmDeleteOperation",
    "RealmListOperation",
    "RealmReadOperation",
    "RealmTenantCreateOperation",
    "RealmTenantListOperation",
    "RealmUpdateOperation",
]
