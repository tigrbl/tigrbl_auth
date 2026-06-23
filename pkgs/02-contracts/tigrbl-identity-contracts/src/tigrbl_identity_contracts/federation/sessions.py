"""Federated session contract objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class FederatedSession:
    session_id: str
    provider_id: str
    tenant_id: str
    issuer: str
    audience: str
    logout_supported: bool
    normalized_claims: Mapping[str, Any]
    bound_at: str


__all__ = ["FederatedSession"]
