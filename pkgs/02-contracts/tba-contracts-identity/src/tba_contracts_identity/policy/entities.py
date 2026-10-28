from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True, slots=True)
class PolicyEntity:
    entity_type: str
    identifier: str
    properties: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PolicyEntityChain:
    entities: tuple[PolicyEntity, ...]


__all__ = ["PolicyEntity", "PolicyEntityChain"]
