"""Authentication challenge contract objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthenticationChallenge:
    challenge_id: str
    subject_id: str
    tenant_id: str
    challenge_kind: str
    expected_nonce: str
    issued_at: str
    expires_at: str
    allowed_methods: tuple[str, ...]
    step_up_required: bool
    bound_credential_id: str | None = None
    consumed: bool = False


__all__ = ["AuthenticationChallenge"]
