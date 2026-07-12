from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DelegationConstraint:
    name: str
    value: object


@dataclass(frozen=True, slots=True)
class DelegationConstraints:
    constraints: tuple[DelegationConstraint, ...] = ()
    not_after: datetime | None = None
    max_depth: int | None = None


__all__ = ["DelegationConstraint", "DelegationConstraints"]
