from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class DecisionEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


class PolicyKind(str, Enum):
    RBAC = "rbac"
    ABAC = "abac"
    PBAC = "pbac"
    DELEGATION = "delegation"
    ADMIN = "admin"


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason: str
    matched: tuple[str, ...] = ()
    trace_id: str = ""


@dataclass(frozen=True, slots=True)
class PolicyTrace:
    trace_id: str
    subject: str
    tenant_id: str
    action: str
    allowed: bool
    reason: str
    matched: tuple[str, ...]
    evaluated_kinds: tuple[PolicyKind, ...]
    recorded_at: str


@dataclass(frozen=True, slots=True)
class PolicyRequest:
    subject: str
    tenant_id: str
    action: str
    resource: str = ""
    roles: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)
    permissions: tuple[str, ...] = ()
    delegated_by: str | None = None
    admin: bool = False


@dataclass(frozen=True, slots=True)
class RolePolicy:
    role: str
    permissions: tuple[str, ...]
    tenant_id: str | None = None
    effect: DecisionEffect = DecisionEffect.ALLOW


@dataclass(frozen=True, slots=True)
class AttributePolicy:
    policy_id: str
    action: str
    required_attributes: Mapping[str, Any]
    tenant_id: str | None = None
    effect: DecisionEffect = DecisionEffect.ALLOW


@dataclass(frozen=True, slots=True)
class PermissionPolicy:
    policy_id: str
    permissions: tuple[str, ...]
    tenant_id: str | None = None
    effect: DecisionEffect = DecisionEffect.ALLOW


@dataclass(frozen=True, slots=True)
class DelegationPolicy:
    delegate: str
    delegator: str
    tenant_ids: tuple[str, ...]
    actions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AdminPolicy:
    subject: str
    tenant_ids: tuple[str, ...]
    actions: tuple[str, ...]
    superuser: bool = False


__all__ = [
    "AdminPolicy",
    "AttributePolicy",
    "DecisionEffect",
    "DelegationPolicy",
    "PermissionPolicy",
    "PolicyDecision",
    "PolicyKind",
    "PolicyRequest",
    "PolicyTrace",
    "RolePolicy",
]
