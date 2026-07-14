"""Credential lifecycle and verification surfaces for the Tigrbl identity package suite."""

from __future__ import annotations

from tigrbl_identity_contracts.audit.credentials import CredentialAuditEvent
from tigrbl_identity_contracts.credentials import CredentialAuditAction, CredentialError

from .lifecycle import (
    Credential,
    CredentialKind,
    CredentialStateError,
    CredentialStatus,
    CredentialVerificationError,
    IssuedCredential,
    consume_one_time_credential,
    create_api_key_credential,
    create_client_secret_credential,
    create_mfa_factor_credential,
    create_passkey_credential,
    create_password_credential,
    create_password_reset_credential,
    create_service_key_credential,
    hash_secret,
    issue_shared_secret,
    new_credential_id,
    revoke_credential,
    rotate_credential,
    utc_now,
    verify_credential,
    verify_secret,
)
from .proof_bindings import (
    DpopKeyCredential,
    MtlsCertificateCredential,
    ProofBinding,
    create_dpop_key_credential,
    create_mtls_certificate_credential,
)

__all__ = [
    "Credential",
    "CredentialAuditAction",
    "CredentialAuditEvent",
    "CredentialError",
    "CredentialKind",
    "CredentialStateError",
    "CredentialStatus",
    "CredentialVerificationError",
    "DpopKeyCredential",
    "IssuedCredential",
    "MtlsCertificateCredential",
    "ProofBinding",
    "consume_one_time_credential",
    "create_api_key_credential",
    "create_client_secret_credential",
    "create_dpop_key_credential",
    "create_mfa_factor_credential",
    "create_mtls_certificate_credential",
    "create_passkey_credential",
    "create_password_credential",
    "create_password_reset_credential",
    "create_service_key_credential",
    "hash_secret",
    "issue_shared_secret",
    "new_credential_id",
    "revoke_credential",
    "rotate_credential",
    "utc_now",
    "verify_credential",
    "verify_secret",
]
