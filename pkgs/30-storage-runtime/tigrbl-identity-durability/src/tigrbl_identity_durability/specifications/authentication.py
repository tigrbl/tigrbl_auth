"""Authentication and federation table aliases for capability composition."""

from tigrbl_identity_storage.tables import (
    AuthenticationChallenge,
    Credential,
    CredentialMfaFactor,
    CredentialRecoveryCode,
    FederatedSession,
    Federation,
    IdentityProvider,
)

AuthenticationChallengeTable = AuthenticationChallenge
CredentialTable = Credential
CredentialMfaFactorTable = CredentialMfaFactor
CredentialRecoveryCodeTable = CredentialRecoveryCode
FederatedSessionTable = FederatedSession
FederationTable = Federation
IdentityProviderTable = IdentityProvider

__all__ = [
    "AuthenticationChallengeTable",
    "CredentialMfaFactorTable",
    "CredentialRecoveryCodeTable",
    "CredentialTable",
    "FederatedSessionTable",
    "FederationTable",
    "IdentityProviderTable",
]
