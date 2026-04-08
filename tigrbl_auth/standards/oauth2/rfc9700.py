"""Executable security-BCP posture helpers for RFC 9700-aligned deployments.

This module converts hardening, FAPI 2.0 security, and peer profiles from declarative target sets
into runtime-enforceable policy.  The authoritative release path uses these
helpers from the authorization endpoint, token endpoint, contract generation,
and discovery metadata generation so the published posture matches runtime
behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Iterable, Mapping, Sequence

from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_auth.standards.oauth2.assertion_framework import JWT_BEARER_GRANT_TYPE

RFC9700_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9700"
DEVICE_CODE_GRANT_TYPE: Final[str] = "urn:ietf:params:oauth:grant-type:device_code"
TOKEN_EXCHANGE_GRANT_TYPE: Final[str] = "urn:ietf:params:oauth:grant-type:token-exchange"
_DPOP_HEADER_NAMES: Final[tuple[str, ...]] = ("DPoP", "dpop")
_CLIENT_CERT_HEADER_NAMES: Final[tuple[str, ...]] = (
    "X-Client-Cert-SHA256",
    "X-SSL-Client-SHA256",
    "X_SSL_CLIENT_CERT_SHA256",
    "MTLS-Client-Cert-SHA256",
)


@dataclass(frozen=True, slots=True)
class OAuthPolicyViolation(ValueError):
    """A fail-closed runtime policy violation."""

    error: str
    description: str
    status_code: int = 400


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


def _as_deployment(
    settings_obj: object | ResolvedDeployment | None = None,
    *,
    profile: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
) -> ResolvedDeployment:
    if isinstance(settings_obj, ResolvedDeployment):
        return settings_obj
    return resolve_deployment(settings_obj, profile=profile, flag_overrides=flag_overrides)


def _is_hardened_profile(deployment: ResolvedDeployment) -> bool:
    return deployment.profile in {"hardening", "fapi2-security", "peer-claim"}


def _is_fapi_profile(deployment: ResolvedDeployment) -> bool:
    return deployment.profile == "fapi2-security"


def _base_response_types(deployment: ResolvedDeployment) -> tuple[str, ...]:
    if not deployment.flag_enabled("enable_oidc_core"):
        return ("code",)
    if _is_hardened_profile(deployment):
        return ("code",)
    return (
        "code",
        "token",
        "id_token",
        "code token",
        "code id_token",
        "token id_token",
        "code token id_token",
    )


def _base_response_modes(deployment: ResolvedDeployment) -> tuple[str, ...]:
    if _is_hardened_profile(deployment):
        return ("query", "form_post")
    return ("query", "fragment", "form_post")


def _base_grant_types(deployment: ResolvedDeployment) -> tuple[str, ...]:
    grants: list[str] = ["authorization_code", "client_credentials", "refresh_token"]
    if not _is_hardened_profile(deployment):
        grants.append("password")
    if deployment.flag_enabled("enable_rfc7521") or deployment.flag_enabled("enable_rfc7523"):
        grants.append(JWT_BEARER_GRANT_TYPE)
    if deployment.flag_enabled("enable_rfc8628"):
        grants.append(DEVICE_CODE_GRANT_TYPE)
    if deployment.flag_enabled("enable_rfc8693"):
        grants.append(TOKEN_EXCHANGE_GRANT_TYPE)
    return tuple(dict.fromkeys(grants))


def _allowed_client_auth_methods(deployment: ResolvedDeployment) -> tuple[str, ...]:
    if _is_fapi_profile(deployment):
        return ("private_key_jwt", "tls_client_auth", "self_signed_tls_client_auth")
    methods: list[str] = ["client_secret_basic", "client_secret_post", "private_key_jwt"]
    if deployment.flag_enabled("enable_rfc8705") or _is_hardened_profile(deployment):
        methods.extend(["tls_client_auth", "self_signed_tls_client_auth"])
    return tuple(dict.fromkeys(methods))


def runtime_security_profile(
    settings_obj: object | ResolvedDeployment | None = None,
    *,
    profile: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
) -> RuntimeSecurityProfile:
    deployment = _as_deployment(settings_obj, profile=profile, flag_overrides=flag_overrides)
    hardened = _is_hardened_profile(deployment)
    fapi_mode = _is_fapi_profile(deployment)
    enabled = deployment.flag_enabled("enable_rfc9700") if hardened else False
    dpop_supported = deployment.flag_enabled("enable_rfc9449")
    mtls_supported = deployment.flag_enabled("enable_rfc8705") or hardened
    return RuntimeSecurityProfile(
        profile=deployment.profile,
        enabled=enabled,
        fapi_mode=fapi_mode,
        oauth21_alignment_mode=str(deployment.flags.get("oauth21_alignment_mode", "tracked")),
        require_tls=bool(deployment.flags.get("require_tls", True)),
        pkce_required=deployment.flag_enabled("enable_rfc7636"),
        pkce_required_for_all_clients=deployment.flag_enabled("enable_rfc7636") and hardened,
        pkce_s256_required=hardened,
        implicit_hybrid_allowed=not hardened,
        password_grant_allowed=not hardened,
        par_required=enabled and deployment.flag_enabled("enable_rfc9126"),
        par_client_auth_required=fapi_mode,
        par_redirect_uri_required=fapi_mode,
        request_uri_max_lifetime_seconds=599 if fapi_mode else 600,
        minimal_frontchannel_authorization=fapi_mode,
        sender_constraint_required=enabled and (dpop_supported or mtls_supported),
        dpop_supported=dpop_supported,
        mtls_supported=mtls_supported,
        allowed_client_auth_methods=_allowed_client_auth_methods(deployment),
        resource_indicators_supported=deployment.flag_enabled("enable_rfc8707"),
        rich_authorization_requests_supported=deployment.flag_enabled("enable_rfc9396"),
        request_objects_supported=deployment.flag_enabled("enable_rfc9101"),
        issuer_identification_supported=deployment.flag_enabled("enable_rfc9207"),
        authorization_response_iss_required=fapi_mode or deployment.flag_enabled("enable_rfc9207"),
        query_bearer_disabled=not bool(deployment.flags.get("enable_rfc6750_query", False)),
        form_bearer_disabled=not bool(deployment.flags.get("enable_rfc6750_form", False)),
        allowed_response_types=_base_response_types(deployment),
        allowed_response_modes=_base_response_modes(deployment),
        allowed_grant_types=_base_grant_types(deployment),
    )


def security_bcp_profile(settings_obj: object | ResolvedDeployment | None = None) -> dict[str, object]:
    return runtime_security_profile(settings_obj).as_dict()


def authorization_enforcement_matrix(
    profiles: Sequence[str] = ("baseline", "production", "hardening", "fapi2-security", "peer-claim"),
) -> list[dict[str, object]]:
    return [runtime_security_profile(profile=profile_name).as_dict() for profile_name in profiles]


def assert_authorization_request_allowed(
    params: dict[str, Any],
    deployment: ResolvedDeployment,
) -> None:
    policy = runtime_security_profile(deployment)
    if policy.minimal_frontchannel_authorization and params.get("_frontchannel_request"):
        extra_keys = {
            key
            for key, value in params.items()
            if value not in (None, "", [], (), {})
            and key not in {"client_id", "request_uri", "_frontchannel_request"}
            and not str(key).startswith("_")
        }
        if extra_keys:
            raise OAuthPolicyViolation(
                "invalid_request",
                "FAPI front-channel authorization requests must be limited to client_id and request_uri",
            )
    response_type = str(params.get("response_type") or "").strip()
    if response_type not in set(policy.allowed_response_types):
        raise OAuthPolicyViolation(
            "unsupported_response_type",
            f"response_type {response_type!r} is not permitted by the active RFC 9700 profile",
        )
    requested_mode = str(params.get("response_mode") or "").strip()
    if requested_mode and requested_mode not in set(policy.allowed_response_modes):
        raise OAuthPolicyViolation(
            "unsupported_response_mode",
            f"response_mode {requested_mode!r} is not permitted by the active RFC 9700 profile",
        )
    if policy.pkce_required_for_all_clients and response_type == "code" and not params.get("code_challenge"):
        raise OAuthPolicyViolation(
            "invalid_request",
            "PKCE is mandatory for authorization_code flows in hardening, FAPI, and peer profiles",
        )
    if policy.pkce_s256_required and params.get("code_challenge_method") not in {None, "", "S256"}:
        raise OAuthPolicyViolation(
            "invalid_request",
            "PKCE code_challenge_method must be S256 in hardening, FAPI, and peer profiles",
        )
    if policy.par_required and not params.get("request_uri"):
        raise OAuthPolicyViolation(
            "invalid_request",
            "Pushed authorization requests are mandatory in hardening, FAPI, and peer profiles when RFC 9126 is enabled",
        )


def assert_token_request_allowed(
    data: dict[str, str],
    deployment: ResolvedDeployment,
) -> None:
    policy = runtime_security_profile(deployment)
    grant_type = str(data.get("grant_type") or "").strip()
    if grant_type not in set(policy.allowed_grant_types):
        raise OAuthPolicyViolation(
            "unsupported_grant_type",
            f"grant_type {grant_type!r} is not permitted by the active RFC 9700 profile",
        )
    if not policy.password_grant_allowed and grant_type == "password":
        raise OAuthPolicyViolation(
            "unsupported_grant_type",
            "resource owner password credentials grant is disabled in hardening, FAPI, and peer profiles",
        )


def dpop_proof_from_request(request: Any) -> str | None:
    headers = getattr(request, "headers", {}) or {}
    for name in _DPOP_HEADER_NAMES:
        value = headers.get(name) if hasattr(headers, "get") else None
        if value:
            return str(value)
    return None


def client_certificate_thumbprint_from_request(request: Any) -> str | None:
    from tigrbl_auth.standards.oauth2.mtls import presented_certificate_thumbprint

    return presented_certificate_thumbprint(request)


def validate_sender_constraint(
    request: Any,
    deployment: ResolvedDeployment,
    *,
    dpop_proof: str | None = None,
) -> SenderConstraintResult:
    policy = runtime_security_profile(deployment)
    cert_thumbprint = client_certificate_thumbprint_from_request(request)
    if dpop_proof and policy.dpop_supported:
        from tigrbl_auth.standards.oauth2.dpop import verify_proof

        jkt = verify_proof(dpop_proof, getattr(request, "method", "POST"), str(getattr(request, "url", "")))
        return SenderConstraintResult(
            mechanism="dpop",
            token_type="DPoP",
            confirmation_claim={"jkt": jkt},
            jkt=jkt,
        )
    if cert_thumbprint and policy.mtls_supported:
        return SenderConstraintResult(
            mechanism="mtls",
            token_type="bearer",
            confirmation_claim={"x5t#S256": cert_thumbprint},
            cert_thumbprint=cert_thumbprint,
        )
    if policy.sender_constraint_required:
        allowed: list[str] = []
        if policy.dpop_supported:
            allowed.append("DPoP proof")
        if policy.mtls_supported:
            allowed.append("mutual-TLS certificate thumbprint")
        detail = " or ".join(allowed) if allowed else "sender-constrained token proof"
        raise OAuthPolicyViolation(
            "invalid_request",
            f"hardening, FAPI, and peer profiles require {detail} at the token issuance boundary",
        )
    return SenderConstraintResult()


def verify_access_token_sender_constraint(
    request: Any,
    token_payload: Mapping[str, Any],
    deployment: ResolvedDeployment,
    *,
    access_token: str | None = None,
    dpop_proof: str | None = None,
) -> SenderConstraintResult:
    """Validate sender-constrained access-token presentation on resource paths.

    The helper is intentionally fail-closed for bound tokens but does not reject
    ordinary bearer tokens simply because hardening mode is enabled; that
    issuance-side requirement is enforced at the token boundary.
    """

    policy = runtime_security_profile(deployment)
    cnf = token_payload.get("cnf") if isinstance(token_payload.get("cnf"), Mapping) else {}
    jkt = cnf.get("jkt")
    x5t = cnf.get("x5t#S256")

    if jkt:
        if not policy.dpop_supported:
            raise OAuthPolicyViolation(
                "invalid_token",
                "DPoP-bound token presented while DPoP support is disabled",
                status_code=401,
            )
        if not dpop_proof:
            raise OAuthPolicyViolation(
                "invalid_token",
                "missing DPoP proof for DPoP-bound access token",
                status_code=401,
            )
        from tigrbl_auth.standards.oauth2.dpop import verify_proof

        try:
            verified_jkt = verify_proof(
                dpop_proof,
                getattr(request, "method", "GET"),
                str(getattr(request, "url", "")),
                jkt=str(jkt),
                access_token=access_token,
            )
        except ValueError as exc:
            raise OAuthPolicyViolation("invalid_token", str(exc), status_code=401) from exc
        return SenderConstraintResult(
            mechanism="dpop",
            token_type="DPoP",
            confirmation_claim={"jkt": verified_jkt},
            jkt=verified_jkt,
        )

    if dpop_proof:
        raise OAuthPolicyViolation(
            "invalid_token",
            "unexpected DPoP proof for non-DPoP access token",
            status_code=401,
        )

    if x5t:
        if not policy.mtls_supported:
            raise OAuthPolicyViolation(
                "invalid_token",
                "certificate-bound token presented while mTLS support is disabled",
                status_code=401,
            )
        from tigrbl_auth.standards.oauth2.mtls import validate_request_certificate_binding
        from tigrbl_auth.errors import InvalidTokenError

        try:
            cert_thumbprint = validate_request_certificate_binding(token_payload, request)
        except InvalidTokenError as exc:
            raise OAuthPolicyViolation("invalid_token", str(exc), status_code=401) from exc
        return SenderConstraintResult(
            mechanism="mtls",
            token_type="bearer",
            confirmation_claim={"x5t#S256": str(x5t)},
            cert_thumbprint=cert_thumbprint,
        )

    return SenderConstraintResult()


def discovery_policy_metadata(deployment: ResolvedDeployment) -> dict[str, object]:
    policy = runtime_security_profile(deployment)
    payload: dict[str, object] = {
        "response_types_supported": list(policy.allowed_response_types),
        "grant_types_supported": list(policy.allowed_grant_types),
        "response_modes_supported": list(policy.allowed_response_modes),
        "code_challenge_methods_supported": ["S256"] if policy.pkce_required else [],
        "token_endpoint_auth_methods_supported": list(policy.allowed_client_auth_methods),
    }
    if policy.authorization_response_iss_required:
        payload["authorization_response_iss_parameter_supported"] = True
    if policy.dpop_supported:
        payload["dpop_signing_alg_values_supported"] = ["EdDSA"]
    if policy.mtls_supported or policy.sender_constraint_required:
        payload["tls_client_certificate_bound_access_tokens"] = True
    if policy.par_required:
        payload["require_pushed_authorization_requests"] = True
    if policy.request_objects_supported:
        payload["request_parameter_supported"] = True
        payload["request_object_signing_alg_values_supported"] = ["HS256", "HS384", "HS512"]
    if policy.resource_indicators_supported:
        payload["resource_parameter_supported"] = True
    if policy.rich_authorization_requests_supported:
        payload["authorization_details_types_supported"] = ["*"]
    if deployment.flag_enabled("enable_rfc9068") or deployment.profile in {"production", "hardening", "fapi2-security", "peer-claim"}:
        payload["access_token_signing_alg_values_supported"] = ["EdDSA"]
    if policy.fapi_mode:
        payload["fapi_profiles_supported"] = ["fapi2-security"]
    return payload


__all__ = [
    "RFC9700_SPEC_URL",
    "DEVICE_CODE_GRANT_TYPE",
    "TOKEN_EXCHANGE_GRANT_TYPE",
    "OAuthPolicyViolation",
    "SenderConstraintResult",
    "RuntimeSecurityProfile",
    "security_bcp_profile",
    "runtime_security_profile",
    "authorization_enforcement_matrix",
    "assert_authorization_request_allowed",
    "assert_token_request_allowed",
    "dpop_proof_from_request",
    "client_certificate_thumbprint_from_request",
    "validate_sender_constraint",
    "verify_access_token_sender_constraint",
    "discovery_policy_metadata",
]
