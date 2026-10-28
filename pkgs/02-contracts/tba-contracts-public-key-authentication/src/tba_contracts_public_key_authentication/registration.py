"""Canonical public-key credential registration contracts."""

from __future__ import annotations

from dataclasses import dataclass

from .attestation import AttestationTrustResult
from .ceremonies import CeremonyContext
from .credentials import PublicKeyCredentialSource


@dataclass(frozen=True, slots=True)
class PublicKeyRegistrationIntent:
    tenant_id: str
    principal_id: str
    rp_id: str
    origin: str
    user_handle: bytes
    display_name: str | None = None


@dataclass(frozen=True, slots=True)
class PublicKeyRegistrationOptions:
    ceremony: CeremonyContext
    algorithms: tuple[int, ...]
    excluded_credential_ids: tuple[bytes, ...] = ()
    user_verification: str = "preferred"
    resident_key: str = "preferred"
    attestation: str = "none"


@dataclass(frozen=True, slots=True)
class VerifiedCredentialRegistration:
    ceremony_id: str
    credential: PublicKeyCredentialSource
    attestation: AttestationTrustResult | None = None


@dataclass(frozen=True, slots=True)
class CredentialRegistrationResult:
    registered: bool
    credential: PublicKeyCredentialSource | None = None
    reason: str | None = None


__all__ = [
    "CredentialRegistrationResult",
    "PublicKeyRegistrationIntent",
    "PublicKeyRegistrationOptions",
    "VerifiedCredentialRegistration",
]
