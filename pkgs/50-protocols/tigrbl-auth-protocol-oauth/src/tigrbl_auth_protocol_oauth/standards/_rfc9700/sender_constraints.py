from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_runtime.deployment import ResolvedDeployment
from tigrbl_identity_contracts.protocol_configuration import protocol_settings as settings

from .security_profile import (
    DEVICE_CODE_GRANT_TYPE,
    RFC9700_SPEC_URL,
    TOKEN_EXCHANGE_GRANT_TYPE,
    OAuthPolicyViolation,
    RuntimeSecurityProfile,
    SenderConstraintResult,
    assert_authorization_request_allowed,
    assert_token_request_allowed,
    authorization_enforcement_matrix,
    client_certificate_thumbprint_from_request,
    dpop_proof_from_request,
    runtime_security_profile,
    security_bcp_profile,
)

ML_DSA_65_ALG = "ML-DSA-65"


def _pqc_jose_enabled() -> bool:
    configured = str(getattr(settings, "jwt_signing_alg", "") or "").replace("_", "-").upper()
    return bool(getattr(settings, "enable_pqc_jose", False)) or configured in {"ML-DSA-65", "MLDSA65"}


def _access_token_signing_algs() -> list[str]:
    algs = ["EdDSA"]
    if _pqc_jose_enabled():
        algs.append(ML_DSA_65_ALG)
    return algs

def validate_sender_constraint(
    request: Any,
    deployment: ResolvedDeployment,
    *,
    dpop_proof: str | None = None,
    replay_checker: Any | None = None,
    nonce_consumer: Any | None = None,
) -> SenderConstraintResult:
    policy = runtime_security_profile(deployment)
    cert_thumbprint = client_certificate_thumbprint_from_request(request)
    if dpop_proof and policy.dpop_supported:
        from tigrbl_auth_protocol_oauth.standards.dpop import verify_proof

        jkt = verify_proof(
            dpop_proof,
            getattr(request, "method", "POST"),
            str(getattr(request, "url", "")),
            replay_checker=replay_checker,
            nonce_consumer=nonce_consumer,
        )
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


async def validate_sender_constraint_async(
    request: Any,
    deployment: ResolvedDeployment,
    *,
    dpop_proof: str | None = None,
    replay_checker: Any | None = None,
    nonce_consumer: Any | None = None,
) -> SenderConstraintResult:
    policy = runtime_security_profile(deployment)
    cert_thumbprint = client_certificate_thumbprint_from_request(request)
    if dpop_proof and policy.dpop_supported:
        from tigrbl_auth_protocol_oauth.standards.dpop import verify_proof_async

        jkt = await verify_proof_async(
            dpop_proof,
            getattr(request, "method", "POST"),
            str(getattr(request, "url", "")),
            replay_checker=replay_checker,
            nonce_consumer=nonce_consumer,
        )
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
    replay_checker: Any | None = None,
    nonce_consumer: Any | None = None,
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
        from tigrbl_auth_protocol_oauth.standards.dpop import verify_proof

        try:
            verified_jkt = verify_proof(
                dpop_proof,
                getattr(request, "method", "GET"),
                str(getattr(request, "url", "")),
                jkt=str(jkt),
                access_token=access_token,
                replay_checker=replay_checker,
                nonce_consumer=nonce_consumer,
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
        from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import validate_request_certificate_binding
        from tigrbl_identity_core.errors import InvalidTokenError

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


async def verify_access_token_sender_constraint_async(
    request: Any,
    token_payload: Mapping[str, Any],
    deployment: ResolvedDeployment,
    *,
    access_token: str | None = None,
    dpop_proof: str | None = None,
    replay_checker: Any | None = None,
    nonce_consumer: Any | None = None,
) -> SenderConstraintResult:
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
        from tigrbl_auth_protocol_oauth.standards.dpop import verify_proof_async

        try:
            verified_jkt = await verify_proof_async(
                dpop_proof,
                getattr(request, "method", "GET"),
                str(getattr(request, "url", "")),
                jkt=str(jkt),
                access_token=access_token,
                replay_checker=replay_checker,
                nonce_consumer=nonce_consumer,
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
        from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import validate_request_certificate_binding
        from tigrbl_identity_core.errors import InvalidTokenError

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
        payload["access_token_signing_alg_values_supported"] = _access_token_signing_algs()
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
    "validate_sender_constraint_async",
    "verify_access_token_sender_constraint",
    "verify_access_token_sender_constraint_async",
    "discovery_policy_metadata",
]
