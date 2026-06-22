"""Storage-owned helpers for authorization policy state."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .tables.attribute_policy import AttributePolicy
from .tables.delegated_admin_scope import DelegatedAdminScope
from .tables.policy_condition import PolicyCondition
from .tables.role import Role
from .tables.tenant_membership import TenantMembership


def record_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def record_id(row: Any) -> str:
    return str(record_value(row, "id", "") or "")


def record_active(row: Any) -> bool:
    return str(record_value(row, "status", "active") or "active") == "active"


def str_tuple(values: Any, *, sort: bool = True) -> tuple[str, ...]:
    if values is None or values == "" or values is False:
        return ()
    if isinstance(values, str):
        items = (values,)
    else:
        items = tuple(str(value) for value in values if value not in {None, ""})
    return tuple(sorted(set(items))) if sort else tuple(items)


def role_record(row: Any) -> dict[str, Any]:
    return {
        "name": str(record_value(row, "name") or ""),
        "tenant_id": record_value(row, "tenant_id"),
        "permissions": str_tuple(record_value(row, "permissions")),
        "denied_permissions": str_tuple(record_value(row, "denied_permissions")),
        "inherited_roles": str_tuple(record_value(row, "inherited_roles")),
        "status": str(record_value(row, "status", "active") or "active"),
    }


def condition_record(row: Any) -> dict[str, Any]:
    return {
        "field_name": str(record_value(row, "field_name") or ""),
        "operator": str(record_value(row, "operator") or ""),
        "expected": record_value(row, "expected"),
    }


def attribute_policy_record(row: Any, conditions: Iterable[Mapping[str, Any]] = ()) -> dict[str, Any]:
    return {
        "id": record_id(row),
        "name": str(record_value(row, "name") or ""),
        "tenant_id": record_value(row, "tenant_id"),
        "client_id": record_value(row, "client_id"),
        "permission": str(record_value(row, "permission") or ""),
        "effect": str(record_value(row, "effect", "allow") or "allow"),
        "required_attributes": dict(record_value(row, "required_attributes", {}) or {}),
        "dynamic_conditions": tuple(dict(condition) for condition in conditions),
        "status": str(record_value(row, "status", "active") or "active"),
    }


def delegated_scope_record(row: Any) -> dict[str, Any]:
    return {
        "subject": str(record_value(row, "subject") or ""),
        "tenant_ids": str_tuple(record_value(row, "tenant_ids")),
        "permissions": str_tuple(record_value(row, "permissions")),
        "visible_client_fields": str_tuple(record_value(row, "visible_client_fields")),
        "mutable_client_fields": str_tuple(record_value(row, "mutable_client_fields")),
        "service_identity_permissions": str_tuple(record_value(row, "service_identity_permissions")),
        "status": str(record_value(row, "status", "active") or "active"),
    }


class AuthzPolicyStore:
    def __init__(self, db: Any) -> None:
        self.db = db

    async def upsert_role(
        self,
        *,
        name: str,
        permissions: Iterable[str],
        tenant_id: str | None = None,
        denied_permissions: Iterable[str] = (),
        inherited_roles: Iterable[str] = (),
    ) -> dict[str, Any]:
        row = await Role.create_role(
            self.db,
            name=name,
            tenant_id=tenant_id,
            permissions=str_tuple(permissions),
            denied_permissions=str_tuple(denied_permissions),
            inherited_roles=str_tuple(inherited_roles),
        )
        return role_record(row)

    async def role_records(self, *, tenant_id: str | None = None) -> tuple[dict[str, Any], ...]:
        rows = await Role.list_for_tenant(self.db)
        records: list[dict[str, Any]] = []
        for row in rows:
            record = role_record(row)
            if record["status"] != "active":
                continue
            if tenant_id is not None and record["tenant_id"] not in {None, tenant_id}:
                continue
            records.append(record)
        return tuple(records)

    async def assign_role(self, *, subject: str, role_name: str, tenant_id: str) -> None:
        membership = await TenantMembership.lookup(self.db, tenant_id=tenant_id, principal_id=subject)
        roles = set(str_tuple(record_value(membership, "roles") if membership is not None else ()))
        roles.add(role_name)
        await TenantMembership.grant_membership(
            self.db,
            tenant_id=tenant_id,
            principal_id=subject,
            roles=tuple(sorted(roles)),
        )

    async def assignment_names_for(self, *, subject: str, tenant_id: str | None = None) -> tuple[str, ...]:
        rows = await TenantMembership.list_for_principal(self.db, principal_id=subject)
        roles: set[str] = set()
        for row in rows:
            if not record_active(row):
                continue
            row_tenant = record_value(row, "tenant_id")
            if tenant_id is not None and row_tenant != tenant_id:
                continue
            roles.update(str_tuple(record_value(row, "roles")))
        return tuple(sorted(roles))

    async def upsert_attribute_policy(
        self,
        *,
        name: str,
        permission: str,
        required_attributes: Mapping[str, Any],
        tenant_id: str | None = None,
        dynamic_conditions: Iterable[Mapping[str, Any]] = (),
        effect: str = "allow",
        client_id: str | None = None,
    ) -> dict[str, Any]:
        row = await AttributePolicy.create_policy(
            self.db,
            name=name,
            tenant_id=tenant_id,
            client_id=client_id,
            permission=permission,
            effect=effect,
            required_attributes=dict(required_attributes),
        )
        conditions = tuple(dict(condition) for condition in dynamic_conditions)
        await PolicyCondition.replace_for_policy(
            self.db,
            policy_id=record_id(row) or name,
            conditions=conditions,
        )
        return attribute_policy_record(row, conditions)

    async def active_attribute_policy_records(self) -> tuple[dict[str, Any], ...]:
        records: list[dict[str, Any]] = []
        for row in await AttributePolicy.list_active(self.db):
            if not record_active(row):
                continue
            policy_id = record_id(row) or str(record_value(row, "name") or "")
            conditions = tuple(condition_record(item) for item in await PolicyCondition.list_for_policy(self.db, policy_id=policy_id))
            records.append(attribute_policy_record(row, conditions))
        return tuple(records)

    async def upsert_delegated_scope(
        self,
        *,
        subject: str,
        tenant_ids: Iterable[str],
        permissions: Iterable[str],
        visible_client_fields: Iterable[str],
        mutable_client_fields: Iterable[str],
        service_identity_permissions: Iterable[str] = (),
    ) -> dict[str, Any]:
        row = await DelegatedAdminScope.grant_scope(
            self.db,
            subject=subject,
            tenant_ids=list(str_tuple(tenant_ids)),
            permissions=list(str_tuple(permissions)),
            visible_client_fields=list(str_tuple(visible_client_fields)),
            mutable_client_fields=list(str_tuple(mutable_client_fields)),
            service_identity_permissions=list(str_tuple(service_identity_permissions)),
        )
        return delegated_scope_record(row)

    async def revoke_delegated_scope(self, *, subject: str) -> dict[str, Any] | None:
        row = await DelegatedAdminScope.revoke_scope(self.db, subject=subject)
        return delegated_scope_record(row) if row is not None else None

    async def delegated_scope_for(self, *, subject: str) -> dict[str, Any] | None:
        row = await DelegatedAdminScope.lookup(self.db, subject=subject)
        if row is None or not record_active(row):
            return None
        return delegated_scope_record(row)

    async def active_delegated_scope_records(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            delegated_scope_record(row)
            for row in await DelegatedAdminScope.list_active(self.db)
            if record_active(row)
        )


__all__ = [
    "AuthzPolicyStore",
    "attribute_policy_record",
    "condition_record",
    "delegated_scope_record",
    "record_active",
    "record_id",
    "record_value",
    "role_record",
    "str_tuple",
]
