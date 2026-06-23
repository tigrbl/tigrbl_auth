"""Credential contract enums."""

from __future__ import annotations

from enum import Enum


class CredentialKind(str, Enum):
    PASSWORD = "password"
    PASSWORD_RESET = "password_reset"
    PASSKEY_WEBAUTHN = "passkey_webauthn"
    API_KEY = "api_key"
    SERVICE_KEY = "service_key"
    CLIENT_SECRET = "client_secret"
    MTLS_CERTIFICATE = "mtls_certificate"
    DPOP_KEY = "dpop_key"
    MFA_FACTOR = "mfa_factor"


class CredentialStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ROTATED = "rotated"
    REVOKED = "revoked"
    EXPIRED = "expired"
    CONSUMED = "consumed"


class CredentialAuditAction(str, Enum):
    CREATED = "created"
    VERIFIED = "verified"
    FAILED = "failed"
    ROTATED = "rotated"
    REVOKED = "revoked"
    CONSUMED = "consumed"


__all__ = ["CredentialAuditAction", "CredentialKind", "CredentialStatus"]
