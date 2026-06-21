"""Passwordless credential contract objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PasswordlessCredential:
    credential_id: str
    subject_id: str
    tenant_id: str
    credential_kind: str
    recovery_codes: tuple[str, ...]
    created_at: str
    revoked: bool = False


__all__ = ["PasswordlessCredential"]
