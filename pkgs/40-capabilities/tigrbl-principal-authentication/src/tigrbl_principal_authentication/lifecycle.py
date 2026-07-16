"""Credential lifecycle behavior for authn credentials."""

from __future__ import annotations

import hmac
import secrets
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping
from uuid import uuid4

from tigrbl_identity_contracts.credentials import (
    Credential,
    CredentialKind,
    CredentialStateError,
    CredentialStatus,
    CredentialVerificationError,
    IssuedCredential,
)
from tigrbl_identity_credentials_concrete import (
    ApiKeyCredential,
    ClientSecretCredential,
    DpopKeyCredential,
    MfaCredential,
    MtlsCertificateCredential,
    PasskeyCredential,
    PasswordCredential,
    PasswordResetCredential,
    ServiceKeyCredential,
)
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher

UTC = timezone.utc
_SECRET_HASHER = BcryptSecretHasher()


def new_credential_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(UTC)


def hash_secret(secret: str) -> str:
    """Hash through the configured provider; no lifecycle-owned format exists."""

    encoded = _SECRET_HASHER.hash_secret(secret).encoded
    return encoded.decode("utf-8") if isinstance(encoded, bytes) else encoded


def verify_secret(secret: str, encoded: str | None) -> bool:
    return _SECRET_HASHER.verify_secret(secret, encoded).verified


def issue_shared_secret(
    principal_id: str,
    kind: CredentialKind | str,
    *,
    secret: str | None = None,
    public_id: str | None = None,
    ttl: timedelta | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> IssuedCredential:
    active_secret = secret or secrets.token_urlsafe(32)
    now = utc_now()
    credential_cls = {
        CredentialKind.API_KEY: ApiKeyCredential,
        CredentialKind.CLIENT_SECRET: ClientSecretCredential,
        CredentialKind.MFA_FACTOR: MfaCredential,
        CredentialKind.PASSWORD: PasswordCredential,
        CredentialKind.PASSWORD_RESET: PasswordResetCredential,
        CredentialKind.SERVICE_KEY: ServiceKeyCredential,
    }.get(CredentialKind(kind), Credential)
    credential_kwargs = {
        "principal_id": principal_id,
        "secret_digest": hash_secret(active_secret),
        "public_id": public_id,
        "created_at": now,
        "expires_at": now + ttl if ttl is not None else None,
        "metadata": dict(metadata or {}),
    }
    if credential_cls is Credential:
        credential = Credential(
            id=new_credential_id(), kind=CredentialKind(kind), **credential_kwargs
        )
    else:
        credential = credential_cls(**credential_kwargs)
    return IssuedCredential(credential=credential, secret=active_secret)


def create_password_credential(principal_id: str, password: str) -> Credential:
    return issue_shared_secret(
        principal_id, CredentialKind.PASSWORD, secret=password
    ).credential


def create_password_reset_credential(
    principal_id: str,
    *,
    ttl: timedelta = timedelta(minutes=15),
) -> IssuedCredential:
    return issue_shared_secret(
        principal_id,
        CredentialKind.PASSWORD_RESET,
        ttl=ttl,
        metadata={"one_time": True},
    )


def create_api_key_credential(
    principal_id: str,
    *,
    public_id: str | None = None,
) -> IssuedCredential:
    return issue_shared_secret(
        principal_id,
        CredentialKind.API_KEY,
        public_id=public_id or f"ak_{secrets.token_hex(8)}",
    )


def create_service_key_credential(
    principal_id: str,
    *,
    public_id: str | None = None,
) -> IssuedCredential:
    return issue_shared_secret(
        principal_id,
        CredentialKind.SERVICE_KEY,
        public_id=public_id or f"sk_{secrets.token_hex(8)}",
    )


def create_client_secret_credential(
    principal_id: str,
    *,
    public_id: str | None = None,
) -> IssuedCredential:
    return issue_shared_secret(
        principal_id,
        CredentialKind.CLIENT_SECRET,
        public_id=public_id or f"cs_{secrets.token_hex(8)}",
    )


def create_mfa_factor_credential(
    principal_id: str,
    factor_secret: str,
    *,
    factor_type: str = "totp",
) -> Credential:
    return issue_shared_secret(
        principal_id,
        CredentialKind.MFA_FACTOR,
        secret=factor_secret,
        metadata={"factor_type": factor_type},
    ).credential


def create_passkey_credential(
    principal_id: str,
    *,
    credential_id: str,
    public_key: str,
    sign_count: int = 0,
) -> Credential:
    if not credential_id:
        raise ValueError("passkey credential_id is required")
    if not public_key:
        raise ValueError("passkey public_key is required")
    return PasskeyCredential(
        principal_id=principal_id,
        credential_id=credential_id,
        public_key=public_key,
        sign_count=sign_count,
    )


def verify_credential(
    credential: Credential,
    presented_secret: str,
    *,
    now: datetime | None = None,
) -> bool:
    credential.require_usable(now)
    if credential.kind is CredentialKind.PASSKEY_WEBAUTHN:
        return hmac.compare_digest(str(credential.public_id or ""), presented_secret)
    return verify_secret(presented_secret, credential.secret_digest)


def rotate_credential(
    credential: Credential,
    *,
    new_secret: str | None = None,
) -> IssuedCredential:
    if credential.status is CredentialStatus.REVOKED:
        raise CredentialStateError("revoked credential cannot be rotated")
    issued = issue_shared_secret(
        credential.principal_id,
        credential.kind,
        secret=new_secret,
        public_id=credential.public_id,
        metadata=credential.metadata,
    )
    return IssuedCredential(
        credential=replace(
            issued.credential,
            version=credential.version + 1,
            rotated_from=credential.id,
        ),
        secret=issued.secret,
    )


def revoke_credential(
    credential: Credential, *, reason: str | None = None
) -> Credential:
    metadata = dict(credential.metadata)
    if reason:
        metadata["revocation_reason"] = reason
    return replace(credential, status=CredentialStatus.REVOKED, metadata=metadata)


def consume_one_time_credential(
    credential: Credential, presented_secret: str
) -> Credential:
    if credential.metadata.get("one_time") is not True:
        raise CredentialStateError("credential is not one-time")
    if not verify_credential(credential, presented_secret):
        raise CredentialVerificationError("credential verification failed")
    return replace(credential, status=CredentialStatus.CONSUMED)


def create_dpop_key_credential(
    principal_id: str,
    *,
    jwk_thumbprint: str,
    public_jwk: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DpopKeyCredential:
    return DpopKeyCredential(
        principal_id=principal_id,
        jwk_thumbprint=jwk_thumbprint,
        public_jwk=dict(public_jwk or {}),
        metadata=dict(metadata or {}),
    )


def create_mtls_certificate_credential(
    principal_id: str,
    *,
    certificate_thumbprint: str,
    subject_dn: str | None = None,
    san_dns: tuple[str, ...] | list[str] | None = None,
    san_uri: tuple[str, ...] | list[str] | None = None,
    san_ip: tuple[str, ...] | list[str] | None = None,
    san_email: tuple[str, ...] | list[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> MtlsCertificateCredential:
    return MtlsCertificateCredential(
        principal_id=principal_id,
        certificate_thumbprint=certificate_thumbprint,
        subject_dn=subject_dn,
        san_dns=tuple(san_dns or ()),
        san_uri=tuple(san_uri or ()),
        san_ip=tuple(san_ip or ()),
        san_email=tuple(san_email or ()),
        metadata=dict(metadata or {}),
    )


__all__ = [
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
