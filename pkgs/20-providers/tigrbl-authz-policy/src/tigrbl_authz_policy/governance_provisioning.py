"""Authorization governance-extension public surface."""

from __future__ import annotations
# ruff: noqa: F403,F405

from dataclasses import replace
from datetime import datetime, timedelta
from typing import Any, Callable, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now, utc_now_iso
from tigrbl_identity_core.versions import version_in_range
from tigrbl_identity_contracts.governance import *


class ScimProvisioningPlane:
    def __init__(self) -> None:
        self._schemas: dict[str, ScimSchema] = {}
        self._users: dict[str, ScimUser] = {}
        self._groups: dict[str, ScimGroup] = {}

    @property
    def schemas(self) -> Mapping[str, ScimSchema]:
        return dict(self._schemas)

    @property
    def users(self) -> Mapping[str, ScimUser]:
        return dict(self._users)

    @property
    def groups(self) -> Mapping[str, ScimGroup]:
        return dict(self._groups)

    def register_schema(self, schema_id: str, *, resource_kind: str, required_fields: Iterable[str]) -> ScimSchema:
        schema = ScimSchema(
            schema_id=schema_id,
            resource_kind=resource_kind,
            required_fields=tuple(sorted(set(required_fields))),
            registered_at=utc_now_iso(),
        )
        self._schemas[schema_id] = schema
        return schema

    def provision_user(
        self,
        user_id: str,
        *,
        tenant_id: str,
        user_name: str,
        attributes: Mapping[str, Any],
    ) -> ScimUser:
        schema = next((item for item in self._schemas.values() if item.resource_kind == "User"), None)
        if schema is None:
            raise RuntimeError("user schema must be registered before provisioning users")
        missing_fields = [field for field in schema.required_fields if field not in attributes]
        if missing_fields:
            raise ValueError(f"user payload missing required fields: {', '.join(missing_fields)}")
        user = ScimUser(
            user_id=user_id,
            tenant_id=tenant_id,
            user_name=user_name,
            attributes=dict(attributes),
            created_at=utc_now_iso(),
        )
        self._users[user_id] = user
        return user

    def patch_user(
        self,
        user_id: str,
        *,
        tenant_id: str,
        operations: Iterable[ScimPatchOperation],
    ) -> ScimUser:
        user = self._users[user_id]
        if user.tenant_id != tenant_id:
            raise PermissionError("user tenant mismatch")
        attributes = dict(user.attributes)
        active = user.active
        for operation in operations:
            if operation.op not in {"add", "replace"}:
                raise ValueError(f"unsupported SCIM patch operation {operation.op!r}")
            if operation.path == "active":
                active = bool(operation.value)
            else:
                attributes[operation.path] = operation.value
        updated = ScimUser(
            user_id=user.user_id,
            tenant_id=user.tenant_id,
            user_name=str(attributes.get("userName", user.user_name)),
            attributes=attributes,
            created_at=user.created_at,
            active=active,
        )
        self._users[user_id] = updated
        return updated

    def provision_group(
        self,
        group_id: str,
        *,
        tenant_id: str,
        display_name: str,
        members: Iterable[str] = (),
    ) -> ScimGroup:
        schema = next((item for item in self._schemas.values() if item.resource_kind == "Group"), None)
        if schema is None:
            raise RuntimeError("group schema must be registered before provisioning groups")
        group = ScimGroup(
            group_id=group_id,
            tenant_id=tenant_id,
            display_name=display_name,
            members=tuple(sorted(set(members))),
            created_at=utc_now_iso(),
        )
        self._groups[group_id] = group
        return group

    def add_group_member(self, group_id: str, *, tenant_id: str, member_id: str) -> ScimGroup:
        group = self._groups[group_id]
        if group.tenant_id != tenant_id:
            raise PermissionError("group tenant mismatch")
        updated = replace(group, members=tuple(sorted(set(group.members + (member_id,)))))
        self._groups[group_id] = updated
        return updated

    def tenant_snapshot(self, tenant_id: str) -> dict[str, Any]:
        users = [user for user in self._users.values() if user.tenant_id == tenant_id]
        groups = [group for group in self._groups.values() if group.tenant_id == tenant_id]
        return {
            "tenant_id": tenant_id,
            "schema_ids": sorted(self._schemas),
            "users": [
                {
                    "id": user.user_id,
                    "user_name": user.user_name,
                    "active": user.active,
                }
                for user in sorted(users, key=lambda item: item.user_id)
            ],
            "groups": [
                {
                    "id": group.group_id,
                    "display_name": group.display_name,
                    "member_count": len(group.members),
                }
                for group in sorted(groups, key=lambda item: item.group_id)
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "schema_count": len(self._schemas),
            "user_count": len(self._users),
            "group_count": len(self._groups),
        }


