from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class PasswordlessCredential:
    credential_id: str
    subject_id: str
    tenant_id: str
    credential_kind: str
    recovery_codes: tuple[str, ...]
    created_at: str
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class MfaFactor:
    factor_id: str
    subject_id: str
    tenant_id: str
    method: str
    created_at: str
    bound_credential_id: str | None = None
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class WebAuthnCredential:
    credential_id: str
    subject_id: str
    tenant_id: str
    rp_id: str
    algorithm: str
    transports: tuple[str, ...]
    created_at: str
    sign_count: int = 0
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class AuthenticationChallenge:
    challenge_id: str
    subject_id: str
    tenant_id: str
    challenge_kind: str
    expected_nonce: str
    issued_at: str
    expires_at: str
    allowed_methods: tuple[str, ...]
    step_up_required: bool
    bound_credential_id: str | None = None
    consumed: bool = False


@dataclass(frozen=True, slots=True)
class IdentityProvider:
    provider_id: str
    tenant_id: str
    kind: str
    issuer: str
    discovery_url: str
    audience: str
    logout_supported: bool
    display_name: str
    claim_mapping: Mapping[str, str]
    scopes: tuple[str, ...]
    key_set_version: int = 1
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class FederatedSession:
    session_id: str
    provider_id: str
    tenant_id: str
    issuer: str
    audience: str
    logout_supported: bool
    normalized_claims: Mapping[str, Any]
    bound_at: str


@dataclass(frozen=True, slots=True)
class DeviceIdentity:
    device_id: str
    subject_id: str
    tenant_id: str
    credential_posture: str
    last_ip_country: str | None
    created_at: str
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class WorkloadIdentity:
    workload_id: str
    tenant_id: str
    trust_domain: str
    cloud: str
    namespace: str
    attestor: str
    credential_id: str
    created_at: str
    revoked: bool = False


__all__ = [
    "AuthenticationChallenge",
    "DeviceIdentity",
    "FederatedSession",
    "IdentityProvider",
    "MfaFactor",
    "PasswordlessCredential",
    "WebAuthnCredential",
    "WorkloadIdentity",
]
