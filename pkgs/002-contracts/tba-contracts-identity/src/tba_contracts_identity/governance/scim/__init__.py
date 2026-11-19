"""SCIM governance contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ScimSchema:
    schema_id: str
    resource_kind: str
    required_fields: tuple[str, ...]
    registered_at: str


@dataclass(frozen=True, slots=True)
class ScimUser:
    user_id: str
    tenant_id: str
    user_name: str
    attributes: Mapping[str, Any]
    created_at: str
    active: bool = True


@dataclass(frozen=True, slots=True)
class ScimGroup:
    group_id: str
    tenant_id: str
    display_name: str
    members: tuple[str, ...]
    created_at: str


@dataclass(frozen=True, slots=True)
class ScimPatchOperation:
    op: str
    path: str
    value: Any


__all__ = [
    "ScimGroup",
    "ScimPatchOperation",
    "ScimSchema",
    "ScimUser",
]
