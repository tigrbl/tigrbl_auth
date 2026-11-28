"""Canonical, transport-neutral platform authorization contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Mapping


def _required(value: str, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label} is required")
    return normalized


class AuthorizationEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    INDETERMINATE = "indeterminate"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True, slots=True)
class PrincipalRef:
    principal_id: str
    principal_type: str
    tenant_id: str | None = None
    attributes: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "principal_id", _required(self.principal_id, "principal_id"))
        object.__setattr__(self, "principal_type", _required(self.principal_type, "principal_type"))


@dataclass(frozen=True, slots=True)
class ResourceRef:
    resource_type: str
    resource_id: str
    tenant_id: str
    scope_path: tuple[str, ...] = ()
    attributes: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "resource_type", _required(self.resource_type, "resource_type"))
        object.__setattr__(self, "resource_id", _required(self.resource_id, "resource_id"))
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))


@dataclass(frozen=True, slots=True)
class AuthenticationContext:
    acr: str | None = None
    amr: tuple[str, ...] = ()
    authenticated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    principal: PrincipalRef
    action: str
    resource: ResourceRef
    authentication: AuthenticationContext = field(default_factory=AuthenticationContext)
    environment: Mapping[str, object] = field(default_factory=dict)
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "action", _required(self.action, "action"))


@dataclass(frozen=True, slots=True)
class ActionDefinition:
    key: str
    resource_type: str
    description: str = ""
    required_acr: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "key", _required(self.key, "action key"))
        object.__setattr__(self, "resource_type", _required(self.resource_type, "resource_type"))


@dataclass(frozen=True, slots=True)
class RoleDefinition:
    role_id: str
    name: str
    tenant_id: str
    actions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "role_id", _required(self.role_id, "role_id"))
        object.__setattr__(self, "name", _required(self.name, "name"))
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))


@dataclass(frozen=True, slots=True)
class RoleGrant:
    grant_id: str
    tenant_id: str
    principal: PrincipalRef
    role_id: str
    resource: ResourceRef
    valid_from: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    conditions: Mapping[str, object] = field(default_factory=dict)
    effect: AuthorizationEffect | str = AuthorizationEffect.ALLOW

    def __post_init__(self) -> None:
        object.__setattr__(self, "grant_id", _required(self.grant_id, "grant_id"))
        object.__setattr__(self, "tenant_id", _required(self.tenant_id, "tenant_id"))
        object.__setattr__(self, "role_id", _required(self.role_id, "role_id"))
        object.__setattr__(self, "effect", AuthorizationEffect(self.effect))
        if self.valid_from and self.expires_at and self.expires_at <= self.valid_from:
            raise ValueError("expires_at must be later than valid_from")


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    decision_id: str
    effect: AuthorizationEffect
    reason_code: str
    matched_role_ids: tuple[str, ...] = ()
    matched_grant_ids: tuple[str, ...] = ()
    matched_policy_versions: tuple[str, ...] = ()
    obligations: tuple[str, ...] = ()
    missing_facts: tuple[str, ...] = ()
    evaluated_at: datetime | None = None

    @property
    def allowed(self) -> bool:
        return self.effect is AuthorizationEffect.ALLOW


__all__ = [
    "ActionDefinition", "AuthenticationContext", "AuthorizationDecision",
    "AuthorizationEffect", "AuthorizationRequest", "PrincipalRef", "ResourceRef",
    "RoleDefinition", "RoleGrant",
]
