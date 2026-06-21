from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from tigrbl_identity_contracts.policy.conditions import DynamicCondition
from tigrbl_identity_contracts.policy.effects import DecisionEffect
from tigrbl_identity_contracts.policy.kinds import PolicyKind
from tigrbl_identity_contracts.policy.rules import PolicyRule


def _clean_tuple(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    return tuple(str(value).strip() for value in values if str(value).strip())


@dataclass(frozen=True, slots=True, kw_only=True)
class RolePolicy(PolicyRule):
    kind: PolicyKind = field(default=PolicyKind.RBAC, init=False)
    role: str
    permissions: tuple[str, ...]

    def __post_init__(self) -> None:
        role = str(self.role).strip()
        if not role:
            raise ValueError("role policy requires role")
        object.__setattr__(self, "role", role)
        object.__setattr__(self, "policy_id", self.policy_id or role)
        object.__setattr__(self, "permissions", _clean_tuple(self.permissions))
        PolicyRule.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class AttributePolicy(PolicyRule):
    kind: PolicyKind = field(default=PolicyKind.ABAC, init=False)
    required_attributes: Mapping[str, Any]
    action: str = ""
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
        object.__setattr__(self, "policy_id", str(policy_id).strip())
        object.__setattr__(self, "action", str(action).strip())
        object.__setattr__(self, "name", str(name).strip())
        object.__setattr__(self, "permission", str(permission).strip())
        object.__setattr__(self, "required_attributes", dict(self.required_attributes))
        object.__setattr__(self, "dynamic_conditions", tuple(self.dynamic_conditions))
        PolicyRule.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class PermissionPolicy(PolicyRule):
    kind: PolicyKind = field(default=PolicyKind.PBAC, init=False)
    policy_id: str
    permissions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not str(self.policy_id).strip():
            raise ValueError("permission policy requires policy_id")
        object.__setattr__(self, "permissions", _clean_tuple(self.permissions))
        PolicyRule.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class DelegationPolicy(PolicyRule):
    kind: PolicyKind = field(default=PolicyKind.DELEGATION, init=False)
    delegate: str
    delegator: str
    tenant_ids: tuple[str, ...]
    actions: tuple[str, ...]

    def __post_init__(self) -> None:
        delegate = str(self.delegate).strip()
        delegator = str(self.delegator).strip()
        if not delegate:
            raise ValueError("delegation policy requires delegate")
        if not delegator:
            raise ValueError("delegation policy requires delegator")
        object.__setattr__(self, "delegate", delegate)
        object.__setattr__(self, "delegator", delegator)
        object.__setattr__(self, "policy_id", self.policy_id or f"{delegator}->{delegate}")
        object.__setattr__(self, "tenant_ids", _clean_tuple(self.tenant_ids))
        object.__setattr__(self, "actions", _clean_tuple(self.actions))
        PolicyRule.__post_init__(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPolicy(PolicyRule):
    kind: PolicyKind = field(default=PolicyKind.ADMIN, init=False)
    subject: str
    tenant_ids: tuple[str, ...]
    actions: tuple[str, ...]
    superuser: bool = False

    def __post_init__(self) -> None:
        subject = str(self.subject).strip()
        if not subject:
            raise ValueError("admin policy requires subject")
        object.__setattr__(self, "subject", subject)
        object.__setattr__(self, "policy_id", self.policy_id or subject)
        object.__setattr__(self, "tenant_ids", _clean_tuple(self.tenant_ids))
        object.__setattr__(self, "actions", _clean_tuple(self.actions))
        PolicyRule.__post_init__(self)


__all__ = [
    "AdminPolicy",
    "AttributePolicy",
    "DelegationPolicy",
    "PermissionPolicy",
    "RolePolicy",
]
