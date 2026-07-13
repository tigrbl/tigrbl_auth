from __future__ import annotations

from typing import Any, Iterable

from tigrbl_identity_core.normalization import (
    row_active as _row_active,
    row_value as _row_value,
    str_tuple as _str_tuple,
)
from tigrbl_identity_core.patterns import matches_dotted_pattern as _permission_matches
from tigrbl_identity_contracts.delegation import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    DelegatedAdminScope,
)
from tigrbl_identity_contracts.policy.decisions import PolicyDecision
from tigrbl_identity_storage.tables.delegated_admin_scope import DelegatedAdminScope as _StoredDelegatedAdminScope


def _delegated_scope_contract(row: Any) -> DelegatedAdminScope:
    visible = _str_tuple(_row_value(row, "visible_client_fields")) or DELEGATED_VISIBLE_CLIENT_FIELDS
    mutable = _str_tuple(_row_value(row, "mutable_client_fields")) or DELEGATED_MUTABLE_CLIENT_FIELDS
    return DelegatedAdminScope(
        subject=str(_row_value(row, "subject") or ""),
        tenant_ids=_str_tuple(_row_value(row, "tenant_ids")),
        permissions=_str_tuple(_row_value(row, "permissions")),
        visible_client_fields=visible,
        mutable_client_fields=mutable,
        service_identity_permissions=_str_tuple(_row_value(row, "service_identity_permissions")),
    )


class DelegatedAdministrator:
    def __init__(self, db: Any) -> None:
        self.db = db

    async def grant_scope(
        self,
        subject: str,
        *,
        tenant_ids: Iterable[str],
        permissions: Iterable[str],
        visible_client_fields: Iterable[str] = DELEGATED_VISIBLE_CLIENT_FIELDS,
        mutable_client_fields: Iterable[str] = DELEGATED_MUTABLE_CLIENT_FIELDS,
        service_identity_permissions: Iterable[str] = (),
    ) -> DelegatedAdminScope:
        row = await _StoredDelegatedAdminScope.handlers.grant_scope.core(
            {"payload": {"subject": subject,
            "tenant_ids": list(_str_tuple(tenant_ids)),
            "permissions": list(_str_tuple(permissions)),
            "visible_client_fields": list(_str_tuple(visible_client_fields)),
            "mutable_client_fields": list(_str_tuple(mutable_client_fields)),
            "service_identity_permissions": list(_str_tuple(service_identity_permissions))}, "db": self.db}
        )
        return _delegated_scope_contract(row)

    async def revoke_scope(self, subject: str) -> DelegatedAdminScope | None:
        row = await _StoredDelegatedAdminScope.handlers.revoke_scope.core(
            {"payload": {"subject": subject}, "db": self.db}
        )
        return _delegated_scope_contract(row) if row is not None else None

    async def scope_for(self, subject: str) -> DelegatedAdminScope | None:
        row = await _StoredDelegatedAdminScope.handlers.lookup.core(
            {"db": self.db, "payload": {"subject": subject}}
        )
        if row is None or not _row_active(row):
            return None
        return _delegated_scope_contract(row)

    async def authorize(
        self,
        subject: str,
        *,
        tenant_id: str,
        permission: str,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision:
        scope = await self.scope_for(subject)
        if scope is None:
            return PolicyDecision(True, "no delegated scope restriction active", ())
        if tenant_id not in scope.tenant_ids:
            return PolicyDecision(False, "permission denied by delegated tenant scope", (scope.subject,))
        if not any(_permission_matches(grant, permission) for grant in scope.permissions):
            return PolicyDecision(False, "permission denied by delegated admin scope", (scope.subject,))
        patch_field_set = set(patch_fields)
        if patch_field_set and not patch_field_set.issubset(set(scope.mutable_client_fields)):
            return PolicyDecision(False, "permission denied by delegated client mutation scope", tuple(sorted(patch_field_set)))
        return PolicyDecision(True, "permission granted by delegated admin scope", (scope.subject,))

    async def visible_tenant_ids(self, subject: str, tenant_ids: Iterable[str]) -> tuple[str, ...]:
        scope = await self.scope_for(subject)
        if scope is None:
            return tuple(sorted(set(tenant_ids)))
        return tuple(sorted(tenant_id for tenant_id in tenant_ids if tenant_id in scope.tenant_ids))

    async def visible_client_fields_for(self, subject: str) -> tuple[str, ...]:
        scope = await self.scope_for(subject)
        if scope is None:
            return ADMIN_CLIENT_FIELDS
        return scope.visible_client_fields

    async def summary(self) -> dict[str, Any]:
        scopes = [
            _delegated_scope_contract(row)
            for row in await _StoredDelegatedAdminScope.handlers.list_active.core(
                {"db": self.db, "payload": {}}
            )
            if _row_active(row)
        ]
        return {
            "scope_count": len(scopes),
            "delegates": sorted(scope.subject for scope in scopes),
            "tenant_map": {
                scope.subject: list(scope.tenant_ids)
                for scope in sorted(scopes, key=lambda scope: scope.subject)
            },
        }


__all__ = [
    "ADMIN_CLIENT_FIELDS",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "DelegatedAdministrator",
]
