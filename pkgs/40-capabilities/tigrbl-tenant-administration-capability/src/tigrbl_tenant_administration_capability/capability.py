"""Tenant-administration capability over injected durable operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenant,
    AdminTenantCreate,
    AdminTenantUpdate,
    TenantAdministrationPolicyError,
    TenantAdministrationValidationError,
    TenantAdministrator,
)
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


TenantListOperation: TypeAlias = Callable[[], object]
TenantCreateOperation: TypeAlias = Callable[[AdminTenantCreate], object]
TenantReadOperation: TypeAlias = Callable[[str], object]
TenantUpdateOperation: TypeAlias = Callable[[str, AdminTenantUpdate], object]
TenantDeleteOperation: TypeAlias = Callable[[str], object]


async def _resolve(value: object) -> object:
    return await value if inspect.isawaitable(value) else value


class TenantAdministrationCapability(Capability):
    def __init__(
        self,
        *,
        lister: TenantListOperation,
        creator: TenantCreateOperation,
        reader: TenantReadOperation,
        updater: TenantUpdateOperation,
        deleter: TenantDeleteOperation,
    ) -> None:
        delegates = {
            "list_tenants": lister,
            "create_tenant": creator,
            "read_tenant": reader,
            "update_tenant": updater,
            "delete_tenant": deleter,
        }
        invalid = tuple(
            sorted(name for name, target in delegates.items() if not callable(target))
        )
        if invalid:
            raise TypeError(
                f"tenant administration delegates must be callable: {invalid}"
            )
        self._lister = lister
        self._creator = creator
        self._reader = reader
        self._updater = updater
        self._deleter = deleter
        super().__init__(
            CapabilityDefinition("identity-admin.tenants", "1.0"),
            operations={
                name: CapabilityOperation(target=getattr(self, name), delegated=True)
                for name in delegates
            },
        )

    @staticmethod
    def _require_admin(actor: TenantAdministrator) -> None:
        if not isinstance(actor, TenantAdministrator) or not (
            actor.is_admin or actor.is_superuser
        ):
            raise TenantAdministrationPolicyError(
                "administrator privileges are required"
            )

    @classmethod
    def _require_superuser(cls, actor: TenantAdministrator, action: str) -> None:
        cls._require_admin(actor)
        if not actor.is_superuser:
            raise TenantAdministrationPolicyError(
                f"superuser privileges are required to {action} tenants"
            )

    async def list_tenants(self, actor: TenantAdministrator) -> tuple[AdminTenant, ...]:
        self._require_admin(actor)
        tenants = tuple(await _resolve(self._lister()))
        if not all(isinstance(tenant, AdminTenant) for tenant in tenants):
            raise TypeError("tenant lister returned an invalid record")
        return tuple(
            sorted(
                tenants, key=lambda item: (item.created_at or "", item.name, item.slug)
            )
        )

    async def create_tenant(
        self,
        actor: TenantAdministrator,
        spec: AdminTenantCreate,
    ) -> AdminTenant:
        self._require_superuser(actor, "provision")
        tenant = await _resolve(self._creator(spec))
        if not isinstance(tenant, AdminTenant):
            raise TypeError("tenant creator returned an invalid record")
        return tenant

    async def read_tenant(
        self,
        actor: TenantAdministrator,
        tenant_id: str,
    ) -> AdminTenant | None:
        self._require_admin(actor)
        tenant = await _resolve(self._reader(tenant_id))
        if tenant is not None and not isinstance(tenant, AdminTenant):
            raise TypeError("tenant reader returned an invalid record")
        return tenant

    async def update_tenant(
        self,
        actor: TenantAdministrator,
        tenant_id: str,
        spec: AdminTenantUpdate,
    ) -> AdminTenant:
        self._require_superuser(actor, "update")
        tenant = await _resolve(self._updater(tenant_id, spec))
        if not isinstance(tenant, AdminTenant):
            raise TypeError("tenant updater returned an invalid record")
        return tenant

    async def delete_tenant(
        self,
        actor: TenantAdministrator,
        tenant_id: str,
    ) -> AdminTenant:
        self._require_superuser(actor, "delete")
        tenant = await self.read_tenant(actor, tenant_id)
        if tenant is None:
            from tigrbl_identity_contracts.admin_tenants import (
                TenantAdministrationNotFoundError,
            )

            raise TenantAdministrationNotFoundError("tenant not found")
        if tenant.slug == "public":
            raise TenantAdministrationValidationError(
                "cannot delete the default public tenant"
            )
        if actor.tenant_id == tenant.tenant_id:
            raise TenantAdministrationValidationError(
                "cannot delete the current administrator tenant"
            )
        deleted = await _resolve(self._deleter(tenant_id))
        if not isinstance(deleted, AdminTenant):
            raise TypeError("tenant deleter returned an invalid record")
        return deleted


__all__ = [
    "TenantAdministrationCapability",
    "TenantCreateOperation",
    "TenantDeleteOperation",
    "TenantListOperation",
    "TenantReadOperation",
    "TenantUpdateOperation",
]
