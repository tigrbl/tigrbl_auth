"""Canonical public-key assertion authentication contracts."""

from __future__ import annotations

from dataclasses import dataclass

from .ceremonies import CeremonyContext
from .credentials import CredentialDescriptor
from .evidence import PublicKeyAuthenticationEvidence


@dataclass(frozen=True, slots=True)
class PublicKeyAuthenticationIntent:
    tenant_id: str
    rp_id: str
    origin: str
    principal_id: str | None = None


@dataclass(frozen=True, slots=True)
class PublicKeyAuthenticationOptions:
    ceremony: CeremonyContext
    allowed_credentials: tuple[CredentialDescriptor, ...] = ()
    user_verification: str = "preferred"


@dataclass(frozen=True, slots=True)
class VerifiedPublicKeyAssertion:
    ceremony_id: str
    credential_id: str
    principal_id: str
    sign_count: int
    evidence: PublicKeyAuthenticationEvidence


@dataclass(frozen=True, slots=True)
class PublicKeyAuthenticationResult:
    authenticated: bool
    principal_id: str | None = None
    evidence: PublicKeyAuthenticationEvidence | None = None
    reason: str | None = None


__all__ = [
    "PublicKeyAuthenticationIntent",
    "PublicKeyAuthenticationOptions",
    "PublicKeyAuthenticationResult",
    "VerifiedPublicKeyAssertion",
]
