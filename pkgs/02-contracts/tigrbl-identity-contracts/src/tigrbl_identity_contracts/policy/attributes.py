"""Policy attribute designator and selector contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from .requests import PolicyRequest


@dataclass(frozen=True, slots=True)
class AttributeDesignator:
    attribute_id: str
    category: str = "subject"
    required: bool = False


@dataclass(frozen=True, slots=True)
class AttributeSelector:
    path: tuple[str, ...]
    required: bool = False


class AttributeResolverPort(Protocol):
    def resolve(
        self, designator: AttributeDesignator, request: PolicyRequest, /
    ) -> Any: ...


class AttributeSelectorPort(Protocol):
    def select(
        self, selector: AttributeSelector, values: Mapping[str, Any], /
    ) -> Any: ...


__all__ = [
    "AttributeDesignator",
    "AttributeResolverPort",
    "AttributeSelector",
    "AttributeSelectorPort",
]
