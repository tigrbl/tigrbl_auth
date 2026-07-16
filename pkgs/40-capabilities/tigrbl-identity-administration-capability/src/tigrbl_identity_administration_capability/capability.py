"""Identity-administration capability over injected durable operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.admin_identities import (
    AdminIdentity,
    AdminIdentityCreate,
    AdminIdentityUpdate,
    IdentityAdministrationNotFoundError,
    IdentityAdministrationPolicyError,
    IdentityAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import PlatformAdministrator
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


IdentityListOperation: TypeAlias = Callable[[str], object]
IdentityCreateOperation: TypeAlias = Callable[[AdminIdentityCreate], object]
IdentityReadOperation: TypeAlias = Callable[[str], object]
IdentityUpdateOperation: TypeAlias = Callable[[str, AdminIdentityUpdate], object]
IdentityDeleteOperation: TypeAlias = Callable[[str], object]


async def _resolve(value: object) -> object:
    return await value if inspect.isawaitable(value) else value


class IdentityAdministrationCapability(Capability):
    def __init__(
        self,
        *,
        lister: IdentityListOperation,
        creator: IdentityCreateOperation,
        reader: IdentityReadOperation,
        updater: IdentityUpdateOperation,
        deleter: IdentityDeleteOperation,
    ) -> None:
        delegates = {
            "list_identities": lister,
            "create_identity": creator,
            "read_identity": reader,
            "update_identity": updater,
            "delete_identity": deleter,
        }
        invalid = tuple(
            sorted(name for name, target in delegates.items() if not callable(target))
        )
        if invalid:
            raise TypeError(
                f"identity administration delegates must be callable: {invalid}"
            )
        self._lister = lister
        self._creator = creator
        self._reader = reader
        self._updater = updater
        self._deleter = deleter
        super().__init__(
            CapabilityDefinition("identity-admin.identities", "1.0"),
            operations={
                name: CapabilityOperation(target=getattr(self, name), delegated=True)
                for name in delegates
            },
        )

    @staticmethod
    def _require_admin(actor: PlatformAdministrator) -> None:
        if not isinstance(actor, PlatformAdministrator) or not (
            actor.is_admin or actor.is_superuser
        ):
            raise IdentityAdministrationPolicyError(
                "administrator privileges are required"
            )

    @classmethod
    def _require_tenant_authority(
        cls,
        actor: PlatformAdministrator,
        tenant_id: str,
    ) -> None:
        cls._require_admin(actor)
        if actor.tenant_id != tenant_id and not actor.is_superuser:
            raise IdentityAdministrationPolicyError(
                "superuser privileges are required for cross-tenant administration"
            )

    @staticmethod
    def _require_privilege_assignment(
        actor: PlatformAdministrator,
        *,
        is_admin: bool,
        is_superuser: bool,
    ) -> None:
        if (is_admin or is_superuser) and not actor.is_superuser:
            raise IdentityAdministrationPolicyError(
                "superuser privileges are required to administer privileged identities"
            )

    async def list_identities(
        self,
        actor: PlatformAdministrator,
        tenant_id: str | None = None,
    ) -> tuple[AdminIdentity, ...]:
        effective_tenant = tenant_id or actor.tenant_id
        self._require_tenant_authority(actor, effective_tenant)
        identities = tuple(await _resolve(self._lister(effective_tenant)))
        if not all(isinstance(identity, AdminIdentity) for identity in identities):
            raise TypeError("identity lister returned an invalid record")
        return tuple(sorted(identities, key=lambda item: item.created_at or ""))

    async def create_identity(
        self,
        actor: PlatformAdministrator,
        spec: AdminIdentityCreate,
    ) -> AdminIdentity:
        self._require_tenant_authority(actor, spec.tenant_id)
        self._require_privilege_assignment(
            actor,
            is_admin=spec.is_admin,
            is_superuser=spec.is_superuser,
        )
        identity = await _resolve(self._creator(spec))
        if not isinstance(identity, AdminIdentity):
            raise TypeError("identity creator returned an invalid record")
        return identity

    async def read_identity(
        self,
        actor: PlatformAdministrator,
        identity_id: str,
    ) -> AdminIdentity | None:
        self._require_admin(actor)
        identity = await _resolve(self._reader(identity_id))
        if identity is not None and not isinstance(identity, AdminIdentity):
            raise TypeError("identity reader returned an invalid record")
        if identity is not None:
            self._require_tenant_authority(actor, identity.tenant_id)
        return identity

    async def update_identity(
        self,
        actor: PlatformAdministrator,
        identity_id: str,
        spec: AdminIdentityUpdate,
    ) -> AdminIdentity:
        current = await self.read_identity(actor, identity_id)
        if current is None:
            raise IdentityAdministrationNotFoundError("user not found")
        next_admin = spec.is_admin if spec.is_admin is not None else current.is_admin
        next_superuser = (
            spec.is_superuser if spec.is_superuser is not None else current.is_superuser
        )
        self._require_privilege_assignment(
            actor,
            is_admin=next_admin,
            is_superuser=next_superuser,
        )
        if actor.actor_id == current.identity_id and spec.is_active is False:
            raise IdentityAdministrationValidationError(
                "cannot deactivate the current administrator"
            )
        identity = await _resolve(self._updater(identity_id, spec))
        if not isinstance(identity, AdminIdentity):
            raise TypeError("identity updater returned an invalid record")
        return identity

    async def delete_identity(
        self,
        actor: PlatformAdministrator,
        identity_id: str,
    ) -> AdminIdentity:
        current = await self.read_identity(actor, identity_id)
        if current is None:
            raise IdentityAdministrationNotFoundError("user not found")
        if actor.actor_id == current.identity_id:
            raise IdentityAdministrationValidationError(
                "cannot delete the current administrator"
            )
        if current.is_superuser and not actor.is_superuser:
            raise IdentityAdministrationPolicyError("superuser privileges are required")
        deleted = await _resolve(self._deleter(identity_id))
        if not isinstance(deleted, AdminIdentity):
            raise TypeError("identity deleter returned an invalid record")
        return deleted


__all__ = [
    "IdentityAdministrationCapability",
    "IdentityCreateOperation",
    "IdentityDeleteOperation",
    "IdentityListOperation",
    "IdentityReadOperation",
    "IdentityUpdateOperation",
]
