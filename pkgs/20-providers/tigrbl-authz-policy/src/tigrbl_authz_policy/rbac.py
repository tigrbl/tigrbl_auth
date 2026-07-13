from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_core.normalization import (
    row_active as _row_active,
    row_value as _row_value,
    str_tuple as _str_tuple,
)
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.authority import Role
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_identity_storage.tables.role import Role as _StoredRole
from tigrbl_identity_storage.tables.tenant_membership import TenantMembership as _StoredTenantMembership


def _role_contract(row: Any) -> Role:
    return Role(
        name=str(_row_value(row, "name") or ""),
        tenant_id=_row_value(row, "tenant_id"),
        permissions=_str_tuple(_row_value(row, "permissions")),
        denied_permissions=_str_tuple(_row_value(row, "denied_permissions")),
        inherited_roles=_str_tuple(_row_value(row, "inherited_roles")),
    )


class RBACAdministrator:
    def __init__(self, db: Any) -> None:
        self.db = db

    async def upsert_role(
        self,
        name: str,
        permissions: tuple[str, ...],
        *,
        tenant_id: str | None = None,
        denied_permissions: tuple[str, ...] = (),
        inherited_roles: tuple[str, ...] = (),
    ) -> Role:
        if not name or not permissions:
            raise ValueError("role name and permissions are required")
        row = await _StoredRole.handlers.create_role.core(
            {
                "db": self.db,
                "payload": {
                    "name": name,
                    "tenant_id": tenant_id,
                    "permissions": _str_tuple(permissions),
                    "denied_permissions": _str_tuple(denied_permissions),
                    "inherited_roles": _str_tuple(inherited_roles),
                },
            }
        )
        return _role_contract(row)

    async def assign_role(self, subject: str, role_name: str, *, tenant_id: str | None = None) -> None:
        if not tenant_id:
            raise ValueError("tenant_id is required for storage-backed role assignment")
        if await self._role_for(role_name, tenant_id) is None:
            raise KeyError(f"unknown role {role_name!r}")
        await _StoredTenantMembership.handlers.assign_role.core(
            {"payload": {"tenant_id": tenant_id, "principal_id": subject, "role_name": role_name}, "db": self.db}
        )

    async def assignments_for(self, subject: str, tenant_id: str | None = None) -> tuple[str, ...]:
        return await _StoredTenantMembership.handlers.role_names_for_principal.core(
            {"payload": {"principal_id": subject, "tenant_id": tenant_id}, "db": self.db}
        )

    async def list_roles(self, tenant_id: str | None = None) -> tuple[Role, ...]:
        role_map = await self._role_map_for_tenant(tenant_id)
        return tuple(role_map[name] for name in sorted(role_map))

    async def effective_permissions(self, subject: str, tenant_id: str | None = None) -> tuple[str, ...]:
        grants, _denies, _matched = await self._decision_inputs(subject, tenant_id)
        return tuple(sorted(grants))

    async def decide(self, subject: str, permission: str, tenant_id: str | None = None) -> PolicyDecision:
        grants, denies, matched_roles = await self._decision_inputs(subject, tenant_id)
        if any(_permission_matches(deny, permission) for deny in denies):
            return PolicyDecision(False, "permission denied by RBAC role assignments", matched_roles)
        if any(_permission_matches(grant, permission) for grant in grants):
            return PolicyDecision(True, "permission granted by assigned role", matched_roles)
        return PolicyDecision(False, "permission denied by RBAC role assignments", matched_roles)

    async def summary(self, tenant_id: str | None = None) -> dict[str, Any]:
        roles = await self.list_roles(tenant_id)
        return {"role_count": len(roles), "roles": [role.name for role in roles]}

    async def _role_for(self, role_name: str, tenant_id: str | None) -> Role | None:
        return (await self._role_map_for_tenant(tenant_id)).get(role_name)

    async def _role_map_for_tenant(self, tenant_id: str | None) -> dict[str, Role]:
        roles: dict[str, Role] = {}
        for row in await _StoredRole.handlers.list_for_tenant.core(
            {"db": self.db, "payload": {"tenant_id": tenant_id}}
        ):
            if not _row_active(row):
                continue
            role = _role_contract(row)
            if tenant_id is not None and role.tenant_id not in {None, tenant_id}:
                continue
            roles[role.name] = role
        return roles

    async def _decision_inputs(
        self,
        subject: str,
        tenant_id: str | None,
    ) -> tuple[set[str], set[str], tuple[str, ...]]:
        grants: set[str] = set()
        denies: set[str] = set()
        matched_roles: set[str] = set()
        roles = await self._role_map_for_tenant(tenant_id)
        for role_name in await _StoredTenantMembership.handlers.role_names_for_principal.core(
            {"payload": {"principal_id": subject, "tenant_id": tenant_id}, "db": self.db}
        ):
            self._collect_role(role_name, roles, grants, denies, matched_roles, set())
        return grants, denies, tuple(sorted(matched_roles))

    def _collect_role(
        self,
        role_name: str,
        roles: Mapping[str, Role],
        grants: set[str],
        denies: set[str],
        matched_roles: set[str],
        seen: set[str],
    ) -> None:
        if role_name in seen or role_name not in roles:
            return
        seen.add(role_name)
        role = roles[role_name]
        matched_roles.add(role_name)
        grants.update(role.permissions)
        denies.update(role.denied_permissions)
        for inherited in role.inherited_roles:
            self._collect_role(inherited, roles, grants, denies, matched_roles, seen)


__all__ = [
    "RBACAdministrator",
    "Role",
]
