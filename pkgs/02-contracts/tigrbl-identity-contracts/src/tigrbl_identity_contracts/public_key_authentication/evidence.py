"""Normalized evidence produced by verified public-key ceremonies."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserPresenceEvidence:
    present: bool


@dataclass(frozen=True, slots=True)
class UserVerificationEvidence:
    verified: bool
    method: str | None = None


@dataclass(frozen=True, slots=True)
class VerifierBindingEvidence:
    rp_id: str
    origin: str
    valid: bool


@dataclass(frozen=True, slots=True)
class CredentialBackupEvidence:
    eligible: bool
    backed_up: bool


@dataclass(frozen=True, slots=True)
class AuthenticatorProvenanceEvidence:
    aaguid: bytes | None = None
    attestation_format: str | None = None
    trusted: bool | None = None


@dataclass(frozen=True, slots=True)
class PublicKeyAuthenticationEvidence:
    credential_id: str
    user_presence: UserPresenceEvidence
    user_verification: UserVerificationEvidence
    verifier_binding: VerifierBindingEvidence
    backup: CredentialBackupEvidence
    provenance: AuthenticatorProvenanceEvidence | None = None


__all__ = [
    "AuthenticatorProvenanceEvidence",
    "CredentialBackupEvidence",
    "PublicKeyAuthenticationEvidence",
    "UserPresenceEvidence",
    "UserVerificationEvidence",
    "VerifierBindingEvidence",
]
