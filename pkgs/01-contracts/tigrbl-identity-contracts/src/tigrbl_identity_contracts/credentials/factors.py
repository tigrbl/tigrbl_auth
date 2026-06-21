"""Authenticator factor contract objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MfaFactor:
    factor_id: str
    subject_id: str
    tenant_id: str
    method: str
    created_at: str
    bound_credential_id: str | None = None
    revoked: bool = False


__all__ = ["MfaFactor"]
