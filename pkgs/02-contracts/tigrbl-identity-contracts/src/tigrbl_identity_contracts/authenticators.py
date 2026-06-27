"""Authenticator contracts and authentication evidence types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable

from tigrbl_security_trust_contracts import AcrValue, AmrValue

from .authentication import AuthenticationChallenge
from .credentials import CredentialKind


class AuthenticatorKind(str, Enum):
    PASSWORD_LOCAL = "password_local"
    API_KEY_LOCAL = "api_key_local"
    SERVICE_KEY_LOCAL = "service_key_local"
    CLIENT_SECRET_LOCAL = "client_secret_local"
    SESSION_LOCAL = "session_local"
    OTP_LOCAL = "otp_local"
    RECOVERY_CODE_LOCAL = "recovery_code_local"
    WEBAUTHN_LOCAL = "webauthn_local"
    MTLS_CLIENT_CERT = "mtls_client_cert"
    DPOP_PROOF = "dpop_proof"
    REMOTE_INTROSPECTION = "remote_introspection"
    FEDERATED_OIDC = "federated_oidc"


class AuthenticationStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CHALLENGE_REQUIRED = "challenge_required"


class AuthenticationFactorClass(str, Enum):
    KNOWLEDGE = "knowledge"
    POSSESSION = "possession"
    INHERENCE = "inherence"
    CONTEXT = "context"
    FEDERATED = "federated"
    SERVICE = "service"


class AuthenticatorProperty(str, Enum):
    PHISHING_RESISTANT = "phishing_resistant"
    VERIFIER_NAME_BOUND = "verifier_name_bound"
    HARDWARE_BACKED = "hardware_backed"
    SOFTWARE_BACKED = "software_backed"
    USER_PRESENT = "user_present"
    USER_VERIFIED = "user_verified"
    SENDER_CONSTRAINED = "sender_constrained"
    REPLAY_RESISTANT = "replay_resistant"


@dataclass(frozen=True, slots=True)
class AuthenticatorMetadata:
    kind: AuthenticatorKind | str
    factor_class: AuthenticationFactorClass | str
    credential_kind: CredentialKind | str | None = None
    amr: tuple[AmrValue | str, ...] = ()
    properties: tuple[AuthenticatorProperty | str, ...] = ()
    challenge_based: bool = False
    description: str | None = None


@dataclass(frozen=True, slots=True)
class AuthenticationRequest:
    subject_hint: str | None = None
    tenant_id: str | None = None
    realm_id: str | None = None
    credential_id: str | None = None
    presented_secret: str | bytes | None = None
    challenge_id: str | None = None
    challenge_response: Mapping[str, Any] = field(default_factory=dict)
    headers: Mapping[str, str] = field(default_factory=dict)
    request_context: Mapping[str, Any] = field(default_factory=dict)
    raw_claims: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ChallengeStartRequest:
    subject_hint: str | None = None
    tenant_id: str | None = None
    realm_id: str | None = None
    credential_id: str | None = None
    request_context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ChallengeFinishRequest:
    challenge_id: str
    subject_hint: str | None = None
    tenant_id: str | None = None
    realm_id: str | None = None
    credential_id: str | None = None
    challenge_response: Mapping[str, Any] = field(default_factory=dict)
    request_context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AuthenticationEvidence:
    amr: tuple[AmrValue | str, ...] = ()
    properties: tuple[AuthenticatorProperty | str, ...] = ()
    authenticator_kind: AuthenticatorKind | str | None = None
    credential_kind: CredentialKind | str | None = None
    credential_id: str | None = None
    challenge_id: str | None = None
    subject_id: str | None = None
    raw_claims: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AuthenticationResult:
    status: AuthenticationStatus | str
    evidence: AuthenticationEvidence = field(default_factory=AuthenticationEvidence)
    subject_id: str | None = None
    principal_id: str | None = None
    acr: AcrValue | str | None = None
    aal: str | None = None
    challenge: AuthenticationChallenge | None = None
    reason: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.status == AuthenticationStatus.SUCCEEDED or self.status == AuthenticationStatus.SUCCEEDED.value


@runtime_checkable
class IAuthenticator(Protocol):
    kind: AuthenticatorKind | str

    def metadata(self) -> AuthenticatorMetadata: ...

    def supported_amr(self) -> tuple[AmrValue | str, ...]: ...

    async def authenticate(self, request: AuthenticationRequest) -> AuthenticationResult: ...


@runtime_checkable
class IChallengeAuthenticator(IAuthenticator, Protocol):
    async def start_challenge(self, request: ChallengeStartRequest) -> AuthenticationChallenge: ...

    async def finish_challenge(self, request: ChallengeFinishRequest) -> AuthenticationResult: ...


__all__ = [
    "AuthenticationEvidence",
    "AuthenticationFactorClass",
    "AuthenticationRequest",
    "AuthenticationResult",
    "AuthenticationStatus",
    "AuthenticatorKind",
    "AuthenticatorMetadata",
    "AuthenticatorProperty",
    "ChallengeFinishRequest",
    "ChallengeStartRequest",
    "IAuthenticator",
    "IChallengeAuthenticator",
]
