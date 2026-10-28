from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class PlaneAccess(str, Enum):
    PUBLIC = "public"
    USER = "user"
    TENANT_ADMIN = "tenant_admin"
    SERVICE_ADMIN = "service_admin"
    PLATFORM_ADMIN = "platform_admin"
    DEVELOPER = "developer"
    RESOURCE_VALIDATION = "resource_validation"
    OPERATOR = "operator"
    INTERNAL = "internal"


class PlaneCapability(str, Enum):
    AUTHENTICATE = "authenticate"
    AUTHORIZE = "authorize"
    ISSUE_TOKEN = "issue_token"
    INTROSPECT_TOKEN = "introspect_token"
    MANAGE_PRINCIPALS = "manage_principals"
    MANAGE_CREDENTIALS = "manage_credentials"
    MANAGE_POLICIES = "manage_policies"
    MANAGE_CLIENTS = "manage_clients"
    MANAGE_KEYS = "manage_keys"
    VIEW_AUDIT = "view_audit"
    VERIFY_RESOURCE_ACCESS = "verify_resource_access"


@dataclass(frozen=True, slots=True)
class PlaneCapabilityDeclaration:
    capability: PlaneCapability
    access: tuple[PlaneAccess, ...]
    scopes: tuple[str, ...] = ()
    audiences: tuple[str, ...] = ()
    required_permissions: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "capability",
            PlaneCapability(self.capability),
        )
        object.__setattr__(
            self,
            "access",
            tuple(PlaneAccess(value) for value in self.access),
        )
        object.__setattr__(self, "scopes", tuple(self.scopes))
        object.__setattr__(self, "audiences", tuple(self.audiences))
        object.__setattr__(self, "required_permissions", tuple(self.required_permissions))
        object.__setattr__(self, "metadata", dict(self.metadata))

    def permits_access(self, access: PlaneAccess | str) -> bool:
        return PlaneAccess(access) in self.access


@dataclass(frozen=True, slots=True)
class PlaneAccessDeclaration:
    surface: str
    access: PlaneAccess
    capabilities: tuple[PlaneCapability, ...]
    default_audience: str | None = None
    default_scopes: tuple[str, ...] = ()
    network_segment: str | None = None
    deployment_profile: str | None = None

    def __post_init__(self) -> None:
        if not self.surface:
            raise ValueError("surface is required")
        object.__setattr__(self, "access", PlaneAccess(self.access))
        object.__setattr__(
            self,
            "capabilities",
            tuple(PlaneCapability(value) for value in self.capabilities),
        )
        object.__setattr__(self, "default_scopes", tuple(self.default_scopes))

    def declares_capability(self, capability: PlaneCapability | str) -> bool:
        return PlaneCapability(capability) in self.capabilities


__all__ = [
    "PlaneAccess",
    "PlaneAccessDeclaration",
    "PlaneCapability",
    "PlaneCapabilityDeclaration",
]
