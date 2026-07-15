"""Durable runtime composition for identity-administration capability calls."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from tigrbl_identity_admin_control_plane import IdentityAdministrationCapability
from tigrbl_identity_contracts.admin_identities import (
    AdminIdentity,
    AdminIdentityCreate,
    AdminIdentityUpdate,
    IdentityAdministrationConflictError,
    IdentityAdministrationNotFoundError,
    IdentityAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import PlatformAdministrator
from tigrbl_identity_storage.tables import Tenant, User
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import (
    create_table_record,
    delete_table_record,
    field_value,
    first_table_record,
    list_table_records,
    read_table_record,
    update_table_record,
)
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher

from .platform_tenant_administration import require_tenant_administrator


_SECRET_HASHER = BcryptSecretHasher()


def _uuid(value: str, *, label: str) -> UUID:
    try:
        return UUID(str(value))
    except (TypeError, ValueError) as exc:
        raise IdentityAdministrationValidationError(f"invalid {label}") from exc


def _identity(row: Any) -> AdminIdentity:
    created_at = field_value(row, "created_at")
    updated_at = field_value(row, "updated_at")
    return AdminIdentity(
        identity_id=str(field_value(row, "id")),
        tenant_id=str(field_value(row, "tenant_id")),
        username=str(field_value(row, "username")),
        email=str(field_value(row, "email")),
        is_active=bool(field_value(row, "is_active", True)),
        is_admin=bool(field_value(row, "is_admin", False)),
        is_superuser=bool(field_value(row, "is_superuser", False)),
        must_change_password=bool(field_value(row, "must_change_password", False)),
        roles=tuple(field_value(row, "roles", ())),
        created_at=created_at.isoformat() if created_at else None,
        updated_at=updated_at.isoformat() if updated_at else None,
    )


def build_identity_administration_capability(
    db: object,
) -> IdentityAdministrationCapability:
    async def lister(tenant_id: str) -> tuple[AdminIdentity, ...]:
        key = _uuid(tenant_id, label="tenant_id")
        return tuple(
            _identity(row)
            for row in await list_table_records(User, db, {"tenant_id": key})
        )

    async def reader(identity_id: str) -> AdminIdentity | None:
        row = await read_table_record(User, db, _uuid(identity_id, label="user_id"))
        return _identity(row) if row is not None else None

    async def creator(spec: AdminIdentityCreate) -> AdminIdentity:
        tenant = await read_table_record(
            Tenant,
            db,
            _uuid(spec.tenant_id, label="tenant_id"),
        )
        if tenant is None:
            raise IdentityAdministrationNotFoundError("tenant not found")
        existing = await first_table_record(User, db, {"username": spec.username})
        if existing is None:
            existing = await first_table_record(User, db, {"email": spec.email})
        if existing is not None:
            raise IdentityAdministrationConflictError(
                "username or email already exists"
            )
        password_hash = _SECRET_HASHER.hash_secret(spec.password).encoded
        row = await create_table_record(
            User,
            db,
            {
                "tenant_id": field_value(tenant, "id"),
                "username": spec.username,
                "email": spec.email,
                "password_hash": password_hash,
                "is_admin": spec.is_admin,
                "is_superuser": spec.is_superuser,
                "must_change_password": spec.must_change_password,
            },
        )
        return _identity(row)

    async def updater(identity_id: str, spec: AdminIdentityUpdate) -> AdminIdentity:
        key = _uuid(identity_id, label="user_id")
        row = await read_table_record(User, db, key)
        if row is None:
            raise IdentityAdministrationNotFoundError("user not found")
        changes: dict[str, object] = {}
        for field_name in (
            "username",
            "is_active",
            "is_admin",
            "is_superuser",
            "must_change_password",
        ):
            value = getattr(spec, field_name)
            if value is not None:
                changes[field_name] = value
        if spec.email is not None:
            changes["email"] = spec.email
        if spec.password is not None:
            changes["password_hash"] = _SECRET_HASHER.hash_secret(spec.password).encoded
        if changes:
            row = await update_table_record(User, db, key, changes)
        return _identity(row)

    async def deleter(identity_id: str) -> AdminIdentity:
        key = _uuid(identity_id, label="user_id")
        row = await read_table_record(User, db, key)
        if row is None:
            raise IdentityAdministrationNotFoundError("user not found")
        snapshot = _identity(row)
        await delete_table_record(User, db, key)
        return snapshot

    return IdentityAdministrationCapability(
        lister=lister,
        creator=creator,
        reader=reader,
        updater=updater,
        deleter=deleter,
    )


async def require_identity_administrator(
    request: object,
    db: object,
) -> PlatformAdministrator:
    return await require_tenant_administrator(request, db)


def identity_administration_for_request(
    request: object,
    db: object,
) -> IdentityAdministrationCapability:
    state = getattr(getattr(request, "app", None), "state", None)
    registry = getattr(state, "tigrbl_auth_capability_registry", None)
    if registry is not None:
        try:
            capability = registry.materialize("identity-admin.identities", db)
        except KeyError:
            pass
        else:
            if not isinstance(capability, IdentityAdministrationCapability):
                raise TypeError(
                    "identity capability factory returned an invalid capability"
                )
            return capability
    return build_identity_administration_capability(db)


__all__ = [
    "build_identity_administration_capability",
    "get_db",
    "identity_administration_for_request",
    "require_identity_administrator",
]
