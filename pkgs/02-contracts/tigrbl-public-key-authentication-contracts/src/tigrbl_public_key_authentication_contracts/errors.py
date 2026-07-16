"""Canonical public-key ceremony and credential errors."""


class PublicKeyAuthenticationError(RuntimeError):
    """Base failure for public-key registration and authentication."""


class CeremonyStateError(PublicKeyAuthenticationError):
    """Raised when ceremony state is missing, expired, or already consumed."""


class PublicKeyCredentialVerificationError(PublicKeyAuthenticationError):
    """Raised when credential proof verification fails."""


# Compatibility alias; the canonical generic error lives in credentials.errors.
CredentialVerificationError = PublicKeyCredentialVerificationError


class AttestationVerificationError(PublicKeyAuthenticationError):
    """Raised when authenticator attestation cannot be accepted."""


class RelyingPartyPolicyError(PublicKeyAuthenticationError):
    """Raised when a relying-party policy binding is violated."""


__all__ = [
    "AttestationVerificationError",
    "CeremonyStateError",
    "CredentialVerificationError",
    "PublicKeyCredentialVerificationError",
    "PublicKeyAuthenticationError",
    "RelyingPartyPolicyError",
]
