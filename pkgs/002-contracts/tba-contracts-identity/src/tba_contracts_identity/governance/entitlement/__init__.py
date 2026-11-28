"""Entitlement governance contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EntitlementDefinition:
    entitlement_id: str
    tenant_id: str
    name: str
    owner: str
    description: str
    created_at: str


@dataclass(frozen=True, slots=True)
class EntitlementAssignment:
    assignment_id: str
    entitlement_id: str
    tenant_id: str
    subject_id: str
    justification: str
    assigned_by: str
    created_at: str
    expires_at: str | None = None
    active: bool = True
    revoked_reason: str | None = None


__all__ = [
    "EntitlementAssignment",
    "EntitlementDefinition",
]
