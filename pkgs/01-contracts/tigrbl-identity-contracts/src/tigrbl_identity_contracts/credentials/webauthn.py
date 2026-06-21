"""WebAuthn credential contract objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WebAuthnCredential:
    credential_id: str
    subject_id: str
    tenant_id: str
    rp_id: str
    algorithm: str
    transports: tuple[str, ...]
    created_at: str
    sign_count: int = 0
    revoked: bool = False


__all__ = ["WebAuthnCredential"]
