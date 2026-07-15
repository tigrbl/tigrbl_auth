"""WebAuthn credential evidence normalization helpers."""

from tigrbl_identity_contracts.public_key_authentication import (
    CredentialBackupEvidence,
    UserPresenceEvidence,
    UserVerificationEvidence,
)


def normalize_credential_evidence(
    *,
    user_present: bool,
    user_verified: bool,
    backup_eligible: bool,
    backup_state: bool,
) -> tuple[UserPresenceEvidence, UserVerificationEvidence, CredentialBackupEvidence]:
    if backup_state and not backup_eligible:
        raise ValueError("backup state cannot be set when backup eligibility is false")
    return (
        UserPresenceEvidence(user_present),
        UserVerificationEvidence(user_verified),
        CredentialBackupEvidence(backup_eligible, backup_state),
    )


__all__ = ["normalize_credential_evidence"]
