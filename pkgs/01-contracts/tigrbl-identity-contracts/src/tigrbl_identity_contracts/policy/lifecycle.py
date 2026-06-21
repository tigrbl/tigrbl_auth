"""Policy lifecycle contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PolicyDefinition:
    policy_id: str
    name: str
    tenant_id: str
    language: str
    created_at: str


@dataclass(frozen=True, slots=True)
class PolicyVersion:
    version_id: str
    policy_id: str
    version_number: int
    source: str
    created_at: str
    relation: str
    context_equals: tuple[tuple[str, Any], ...]
    promoted: bool = False


__all__ = ["PolicyDefinition", "PolicyVersion"]
