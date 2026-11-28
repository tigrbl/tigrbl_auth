"""Fail-closed normalization for the legacy role JSON representation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True, slots=True)
class NormalizedRoleGrant:
    grant_id: str
    tenant_id: str
    principal_id: str
    role_id: str
    resource_type: str
    resource_id: str


@dataclass(frozen=True, slots=True)
class NormalizedAuthorization:
    role_permissions: tuple[tuple[str, str, str], ...]
    role_grants: tuple[NormalizedRoleGrant, ...]


def normalize_legacy_authorization(*, roles: Iterable[Mapping[str, object]], memberships: Iterable[Mapping[str, object]]) -> NormalizedAuthorization:
    by_key: dict[tuple[str, str], Mapping[str, object]] = {}
    permissions: list[tuple[str, str, str]] = []
    for role in roles:
        tenant_id, name, role_id = str(role["tenant_id"]), str(role["name"]), str(role["id"])
        key = (tenant_id, name)
        if key in by_key:
            raise ValueError(f"duplicate legacy role {tenant_id}/{name}")
        by_key[key] = role
        permissions.extend((role_id, str(permission), "allow") for permission in role.get("permissions", ()))
    grants: list[NormalizedRoleGrant] = []
    for membership in memberships:
        tenant_id = str(membership["tenant_id"])
        principal_id = str(membership["principal_id"])
        for name in membership.get("roles", ()):
            role = by_key.get((tenant_id, str(name)))
            if role is None:
                raise ValueError(f"unknown legacy role {tenant_id}/{name}")
            role_id = str(role["id"])
            grants.append(NormalizedRoleGrant(f"legacy:{tenant_id}:{principal_id}:{role_id}", tenant_id, principal_id, role_id, "tenant", tenant_id))
    return NormalizedAuthorization(tuple(permissions), tuple(grants))
