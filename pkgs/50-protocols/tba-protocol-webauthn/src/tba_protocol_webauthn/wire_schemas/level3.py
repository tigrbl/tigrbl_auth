"""WebAuthn Level 3 schema surface; additional behavior is feature-gated."""

from .level2 import (
    AuthenticatorAssertionResponse,
    AuthenticatorAttestationResponse,
    AuthenticatorSelectionCriteria,
    CollectedClientData,
    PublicKeyCredential,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialParameters,
    PublicKeyCredentialRequestOptions,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
)

__all__ = [
    "AuthenticatorAssertionResponse",
    "AuthenticatorAttestationResponse",
    "AuthenticatorSelectionCriteria",
    "CollectedClientData",
    "PublicKeyCredential",
    "PublicKeyCredentialCreationOptions",
    "PublicKeyCredentialDescriptor",
    "PublicKeyCredentialParameters",
    "PublicKeyCredentialRequestOptions",
    "PublicKeyCredentialRpEntity",
    "PublicKeyCredentialUserEntity",
]
