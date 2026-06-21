"""Policy definition contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PolicyDefinition:
    policy_id: str
    name: str
    tenant_id: str
    language: str
    created_at: str


__all__ = ["PolicyDefinition"]
