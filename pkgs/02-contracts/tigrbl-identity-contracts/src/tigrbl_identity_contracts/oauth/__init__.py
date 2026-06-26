from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from importlib import import_module
from typing import Any, Protocol

from ..protocols import OAuthGrantStatus


@dataclass(frozen=True, slots=True)
class OAuthClient:
    client_id: str
    tenant_id: str
    allowed_scopes: tuple[str, ...]
    redirect_uris: tuple[str, ...] = ()
    jwk_thumbprint: str | None = None
    mtls_thumbprint: str | None = None
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class DeviceAuthorization:
    device_code: str
    user_code: str
    client_id: str
    tenant_id: str
    scopes: tuple[str, ...]
    expires_at: datetime
    interval_seconds: int = 5
    status: OAuthGrantStatus = OAuthGrantStatus.PENDING
    subject: str | None = None
    poll_count: int = 0


@dataclass(frozen=True, slots=True)
class TokenExchangeResult:
    issued_token: str
    subject: str
    actor: str
    audience: str
    scopes: tuple[str, ...]
    token_type: str = "urn:ietf:params:oauth:token-type:access_token"


@dataclass(frozen=True, slots=True)
class DPoPProof:
    jti: str
    htm: str
    htu: str
    iat: int
    jwk_thumbprint: str
    access_token_hash: str | None = None


class OAuthRepositoryPort(Protocol):
    def save_client(self, client: OAuthClient) -> None: ...

    def get_client(self, client_id: str) -> OAuthClient | None: ...

    def save_device_authorization(self, grant: DeviceAuthorization) -> None: ...

    def get_device_authorization(self, device_code: str) -> DeviceAuthorization | None: ...

    def remember_dpop_jti(self, client_id: str, jti: str) -> bool: ...


@dataclass(frozen=True, slots=True)
class RequestObjectPolicy:
    allowed_algs: tuple[str, ...] = ("HS256", "HS384", "HS512")
    require_signature: bool = True
    max_clock_skew_seconds: int = 60


@dataclass(frozen=True, slots=True)
class PARValidationResult:
    request_uri: str
    client_id: str | None
    expires_at: datetime
    consumed: bool
    params: dict[str, Any]


@dataclass(frozen=True, slots=True)
class AuthorizationDetailsBinding:
    details: list[dict[str, Any]]
    resource: str | None
    audience: str | None


@dataclass(frozen=True, slots=True)
class ResourceSelection:
    resources: tuple[str, ...]
    resource: str | None
    audience: str | None


@dataclass(frozen=True, slots=True)
class NativeRedirectAssessment:
    redirect_uri: str
    kind: str
    scheme: str
    host: str | None
    port: int | None
    pkce_required: bool = True


@dataclass(frozen=True, slots=True)
class SenderConstraintResult:
    mechanism: str | None = None
    token_type: str = "bearer"
    confirmation_claim: dict[str, str] | None = None
    cert_thumbprint: str | None = None
    jkt: str | None = None


@dataclass(frozen=True, slots=True)
class RuntimeSecurityProfile:
    profile: str
    enabled: bool
    fapi_mode: bool
    oauth21_alignment_mode: str
    require_tls: bool
    pkce_required: bool
    pkce_required_for_all_clients: bool
    pkce_s256_required: bool
    implicit_hybrid_allowed: bool
    password_grant_allowed: bool
    par_required: bool
    par_client_auth_required: bool
    par_redirect_uri_required: bool
    request_uri_max_lifetime_seconds: int
    minimal_frontchannel_authorization: bool
    sender_constraint_required: bool
    dpop_supported: bool
    mtls_supported: bool
    allowed_client_auth_methods: tuple[str, ...]
    resource_indicators_supported: bool
    rich_authorization_requests_supported: bool
    request_objects_supported: bool
    issuer_identification_supported: bool
    authorization_response_iss_required: bool
    query_bearer_disabled: bool
    form_bearer_disabled: bool
    allowed_response_types: tuple[str, ...]
    allowed_response_modes: tuple[str, ...]
    allowed_grant_types: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "profile": self.profile,
            "enabled": self.enabled,
            "fapi_mode": self.fapi_mode,
            "oauth21_alignment_mode": self.oauth21_alignment_mode,
            "require_tls": self.require_tls,
            "pkce_required": self.pkce_required,
            "pkce_required_for_all_clients": self.pkce_required_for_all_clients,
            "pkce_s256_required": self.pkce_s256_required,
            "implicit_hybrid_allowed": self.implicit_hybrid_allowed,
            "password_grant_allowed": self.password_grant_allowed,
            "par_required": self.par_required,
            "par_client_auth_required": self.par_client_auth_required,
            "par_redirect_uri_required": self.par_redirect_uri_required,
            "request_uri_max_lifetime_seconds": self.request_uri_max_lifetime_seconds,
            "minimal_frontchannel_authorization": self.minimal_frontchannel_authorization,
            "sender_constraint_required": self.sender_constraint_required,
            "dpop_supported": self.dpop_supported,
            "mtls_supported": self.mtls_supported,
            "allowed_client_auth_methods": list(self.allowed_client_auth_methods),
            "resource_indicators_supported": self.resource_indicators_supported,
            "rich_authorization_requests_supported": self.rich_authorization_requests_supported,
            "request_objects_supported": self.request_objects_supported,
            "issuer_identification_supported": self.issuer_identification_supported,
            "authorization_response_iss_required": self.authorization_response_iss_required,
            "query_bearer_disabled": self.query_bearer_disabled,
            "form_bearer_disabled": self.form_bearer_disabled,
            "allowed_response_types": list(self.allowed_response_types),
            "allowed_response_modes": list(self.allowed_response_modes),
            "allowed_grant_types": list(self.allowed_grant_types),
        }


@dataclass(frozen=True, slots=True)
class ProtectedResourceVerifierContract:
    verifier_logic_id: str
    issuer: str
    accepted_issuers: tuple[str, ...]
    resource: str
    accepted_audiences: tuple[str, ...]
    accepted_token_classes: tuple[str, ...]
    sender_constraint_modes: tuple[str, ...]
    sender_constraint_required: bool
    required_claims: tuple[str, ...]
    replay_expectation: str
    freshness_expectation: str
    introspection_auth_methods: tuple[str, ...]
    allowed_algs: tuple[str, ...] = ()
    jwks_uri: str = ""
    introspection_endpoint: str = ""
    required_scopes: tuple[str, ...] = ()
    max_authz_staleness_seconds: int = 0
    cache_policy: str = ""
    clock_skew_seconds: int = 0
    fail_closed: bool = True
    revocation_check: str = ""

    def as_metadata_projection(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "resource": self.resource,
            "authorization_servers": list(self.accepted_issuers),
            "token_types_supported": list(self.accepted_token_classes),
            "proof_modes_supported": list(self.sender_constraint_modes),
            "proof_binding_required": self.sender_constraint_required,
            "required_claims": list(self.required_claims),
            "introspection_endpoint_auth_methods_supported": list(self.introspection_auth_methods),
            "verifier_logic": self.verifier_logic_id,
            "verification_freshness_expectation": self.freshness_expectation,
            "verification_replay_expectation": self.replay_expectation,
        }
        if self.issuer:
            payload["issuer"] = self.issuer
        if self.accepted_audiences:
            payload["accepted_audiences"] = list(self.accepted_audiences)
        if self.allowed_algs:
            payload["allowed_algorithms"] = list(self.allowed_algs)
        if self.jwks_uri:
            payload["jwks_uri"] = self.jwks_uri
        if self.introspection_endpoint:
            payload["introspection_endpoint"] = self.introspection_endpoint
        if self.required_scopes:
            payload["required_scopes"] = list(self.required_scopes)
        if self.max_authz_staleness_seconds:
            payload["max_authz_staleness_seconds"] = self.max_authz_staleness_seconds
        if self.cache_policy:
            payload["cache_policy"] = self.cache_policy
        if self.clock_skew_seconds:
            payload["clock_skew_seconds"] = self.clock_skew_seconds
        payload["fail_closed"] = self.fail_closed
        if self.revocation_check:
            payload["revocation_check"] = self.revocation_check
        return payload


_LAZY_EXPORTS = {
    "AuthorizationServerConfigPort": ".authorization_server",
    "AuthorizationServerCreateRequest": ".authorization_server",
    "AuthorizationServerMetadataPublisherPort": ".authorization_server",
    "AuthorizationServerReadResponse": ".authorization_server",
    "AuthorizationServerResolverPort": ".authorization_server",
    "AuthorizationServerUpdateRequest": ".authorization_server",
    "ConsentCreateRequest": ".consent",
    "ConsentReadResponse": ".consent",
    "ConsentServicePort": ".consent",
    "ConsentUpdateRequest": ".consent",
    "RefreshIn": ".refresh",
    "RefreshTokenLifecyclePort": ".refresh",
    "RevocationIn": ".revocation",
    "RevocationOut": ".revocation",
    "RevokedTokenReadResponse": ".revocation",
    "ScopeMatchRequest": ".scope",
    "ScopeMatchResult": ".scope",
    "ScopeMatcherPort": ".scope",
    "TokenExchangeRequest": ".exchange",
    "TokenExchangeServicePort": ".exchange",
    "TokenPair": ".refresh",
    "TokenRecordReadResponse": ".refresh",
    "TokenRevocationPort": ".revocation",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(name)
    module = import_module(_LAZY_EXPORTS[name], __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value


__all__ = [
    "AuthorizationDetailsBinding",
    "DPoPProof",
    "DeviceAuthorization",
    "NativeRedirectAssessment",
    "OAuthClient",
    "OAuthRepositoryPort",
    "PARValidationResult",
    "ProtectedResourceVerifierContract",
    "RequestObjectPolicy",
    "ResourceSelection",
    "RuntimeSecurityProfile",
    "SenderConstraintResult",
    "TokenExchangeResult",
]
