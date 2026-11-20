"""Policy rule contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .effects import DecisionEffect
from .kinds import PolicyKind


@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyRule:
    kind: PolicyKind
    policy_id: str = ""
    effect: DecisionEffect | str = DecisionEffect.ALLOW
    tenant_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", PolicyKind(self.kind))
        object.__setattr__(self, "policy_id", str(self.policy_id).strip())
        object.__setattr__(self, "effect", DecisionEffect(self.effect))
        object.__setattr__(self, "metadata", dict(self.metadata))


__all__ = [
    "PolicyRule",
]
