from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .authentication import ServiceIdentityAuthentication
from .credentials import ServiceCredential
from .delegation import (
    ADMIN_CLIENT_FIELDS,
    DELEGATED_MUTABLE_CLIENT_FIELDS,
    DELEGATED_VISIBLE_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    DelegatedAdminScope,
)
from .principals import ServiceIdentity


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    reason: str
    matched: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Role:
    name: str
    permissions: tuple[str, ...]
    tenant_id: str | None = None
    denied_permissions: tuple[str, ...] = ()
    inherited_roles: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DynamicCondition:
    field: str
    operator: str
    expected: Any

    def evaluate(self, attributes: Mapping[str, Any]) -> bool:
        actual = attributes.get(self.field)
        if self.operator == "eq":
            return actual == self.expected
        if self.operator == "neq":
            return actual != self.expected
        if self.operator == "in":
            return actual in self.expected
        if self.operator == "contains":
            return self.expected in actual if actual is not None else False
        if self.operator == "gte":
            return actual is not None and actual >= self.expected
        if self.operator == "lte":
            return actual is not None and actual <= self.expected
        if self.operator == "prefix":
            return isinstance(actual, str) and actual.startswith(str(self.expected))
        raise ValueError(f"unsupported dynamic condition operator {self.operator!r}")


@dataclass(frozen=True, slots=True)
class AttributePolicy:
    name: str
    permission: str
    required_attributes: Mapping[str, Any]
    tenant_id: str | None = None
    dynamic_conditions: tuple[DynamicCondition, ...] = ()
    effect: str = "allow"
    client_id: str | None = None


__all__ = [
    "ADMIN_CLIENT_FIELDS",
    "AttributePolicy",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "DynamicCondition",
    "PUBLIC_CLIENT_FIELDS",
    "PolicyDecision",
    "Role",
    "ServiceCredential",
    "ServiceIdentity",
    "ServiceIdentityAuthentication",
]
