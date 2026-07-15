"""Executable verifier-grade protected-resource contracts."""

from __future__ import annotations

from tigrbl_identity_contracts.oauth import ProtectedResourceVerifierContract
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    OAuthDeploymentProfile,
    runtime_security_profile,
)

ML_DSA_65_ALG = "ML-DSA-65"


def _pqc_jose_enabled(deployment: OAuthDeploymentProfile) -> bool:
    configured = (
        str(
            getattr(deployment, "jwt_signing_alg", "")
            or deployment.flags.get("jwt_signing_alg", "")
        )
        .replace("_", "-")
        .upper()
    )
    return deployment.flag_enabled("enable_pqc_jose") or configured in {
        "ML-DSA-65",
        "MLDSA65",
    }


def _allowed_token_algs(
    deployment: OAuthDeploymentProfile,
) -> tuple[str, ...]:
    algs = ["RS256", "ES256", "EdDSA"]
    if _pqc_jose_enabled(deployment):
        algs.append(ML_DSA_65_ALG)
    return tuple(algs)


def build_protected_resource_verifier_contract(
    deployment: OAuthDeploymentProfile,
) -> ProtectedResourceVerifierContract:
    policy = runtime_security_profile(deployment)
    issuer = str(getattr(deployment, "issuer", "")).rstrip("/")
    resource = str(getattr(deployment, "protected_resource_identifier", ""))
    if not issuer or not resource:
        raise ValueError("protected-resource deployment requires issuer and resource")

    modes: list[str] = ["bearer"]
    if policy.dpop_supported:
        modes.append("dpop")
    if policy.mtls_supported:
        modes.append("mtls")

    required_claims = ["iss", "sub", "aud", "exp", "iat"]
    if policy.sender_constraint_required:
        required_claims.append("cnf")

    replay_expectation = (
        "proof-bound replay resistant"
        if policy.sender_constraint_required
        else "bearer replay constrained by token lifetime"
    )
    freshness_expectation = "introspection or local validation required at request time"
    return ProtectedResourceVerifierContract(
        verifier_logic_id=f"resource-verifier:{deployment.profile}",
        issuer=issuer,
        accepted_issuers=(issuer,),
        resource=resource,
        accepted_audiences=(resource,),
        accepted_token_classes=("access_token",),
        allowed_algs=_allowed_token_algs(deployment),
        jwks_uri=f"{issuer}/.well-known/jwks.json",
        introspection_endpoint=f"{issuer}/introspect",
        sender_constraint_modes=tuple(dict.fromkeys(modes)),
        sender_constraint_required=bool(policy.sender_constraint_required),
        required_claims=tuple(required_claims),
        required_scopes=("openid",),
        max_authz_staleness_seconds=300,
        cache_policy="cache metadata and JWKS only within configured freshness windows; fail closed on stale authorization state",
        clock_skew_seconds=60,
        fail_closed=True,
        revocation_check="introspection required for opaque tokens and for JWTs when local freshness cannot be proven",
        replay_expectation=replay_expectation,
        freshness_expectation=freshness_expectation,
        introspection_auth_methods=tuple(policy.allowed_client_auth_methods),
    )


__all__ = [
    "ProtectedResourceVerifierContract",
    "build_protected_resource_verifier_contract",
]
