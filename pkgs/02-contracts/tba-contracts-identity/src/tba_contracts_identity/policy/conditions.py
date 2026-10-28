"""Policy condition contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


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


__all__ = ["DynamicCondition"]
