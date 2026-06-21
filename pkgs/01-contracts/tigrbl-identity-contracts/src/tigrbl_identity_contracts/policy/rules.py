"""Policy rule contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .conditions import DynamicCondition
from .effects import DecisionEffect


@dataclass(frozen=True, slots=True)
class RolePolicy:
    role: str
    permissions: tuple[str, ...]
    tenant_id: str | None = None
    effect: DecisionEffect | str = DecisionEffect.ALLOW

    def __post_init__(self) -> None:
        object.__setattr__(self, "effect", DecisionEffect(self.effect))


@dataclass(frozen=True, slots=True)
class AttributePolicy:
    required_attributes: Mapping[str, Any]
    policy_id: str = ""
    action: str = ""
    tenant_id: str | None = None
    effect: DecisionEffect | str = DecisionEffect.ALLOW
    name: str = ""
    permission: str = ""
    dynamic_conditions: tuple[DynamicCondition, ...] = ()
    client_id: str | None = None

    def __post_init__(self) -> None:
        policy_id = self.policy_id or self.name
        action = self.action or self.permission
        name = self.name or policy_id
        permission = self.permission or action
        if not policy_id:
            raise ValueError("attribute policy requires policy_id or name")
        if not action:
            raise ValueError("attribute policy requires action or permission")
        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "action", action)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "permission", permission)
        object.__setattr__(self, "required_attributes", dict(self.required_attributes))
        object.__setattr__(self, "effect", DecisionEffect(self.effect))
        object.__setattr__(self, "dynamic_conditions", tuple(self.dynamic_conditions))


@dataclass(frozen=True, slots=True)
class PermissionPolicy:
    policy_id: str
    permissions: tuple[str, ...]
    tenant_id: str | None = None
    effect: DecisionEffect | str = DecisionEffect.ALLOW

    def __post_init__(self) -> None:
        object.__setattr__(self, "effect", DecisionEffect(self.effect))


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
    "DelegationPolicy",
    "PermissionPolicy",
    "RolePolicy",
]
