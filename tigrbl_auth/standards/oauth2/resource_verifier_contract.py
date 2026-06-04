"""Executable verifier-grade protected-resource contracts."""

from __future__ import annotations

from dataclasses import dataclass

from tigrbl_auth.config.deployment import ResolvedDeployment, deployment_from_request, resolve_deployment
from tigrbl_auth.config.settings import settings
from tigrbl_auth.standards.oauth2.rfc9700 import runtime_security_profile


@dataclass(frozen=True, slots=True)
class ProtectedResourceVerifierContract:
    verifier_logic_id: str
    issuer: str
    accepted_issuers: tuple[str, ...]
    resource: str
    accepted_audiences: tuple[str, ...]
    accepted_token_classes: tuple[str, ...]
    allowed_algs: tuple[str, ...]
    jwks_uri: str
    introspection_endpoint: str
    sender_constraint_modes: tuple[str, ...]
    sender_constraint_required: bool
    required_claims: tuple[str, ...]
    required_scopes: tuple[str, ...]
    max_authz_staleness_seconds: int
    cache_policy: str
    clock_skew_seconds: int
    fail_closed: bool
    revocation_check: str
    replay_expectation: str
    freshness_expectation: str
    introspection_auth_methods: tuple[str, ...]

    def as_metadata_projection(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "resource": self.resource,
            "authorization_servers": list(self.accepted_issuers),
            "issuer": self.issuer,
            "accepted_audiences": list(self.accepted_audiences),
            "token_types_supported": list(self.accepted_token_classes),
            "allowed_algorithms": list(self.allowed_algs),
            "jwks_uri": self.jwks_uri,
            "introspection_endpoint": self.introspection_endpoint,
            "proof_modes_supported": list(self.sender_constraint_modes),
            "proof_binding_required": self.sender_constraint_required,
            "required_claims": list(self.required_claims),
            "required_scopes": list(self.required_scopes),
            "max_authz_staleness_seconds": self.max_authz_staleness_seconds,
            "cache_policy": self.cache_policy,
            "clock_skew_seconds": self.clock_skew_seconds,
            "fail_closed": self.fail_closed,
            "revocation_check": self.revocation_check,
            "introspection_endpoint_auth_methods_supported": list(self.introspection_auth_methods),
            "verifier_logic": self.verifier_logic_id,
            "verification_freshness_expectation": self.freshness_expectation,
            "verification_replay_expectation": self.replay_expectation,
        }
        return payload


def build_protected_resource_verifier_contract(
    deployment: ResolvedDeployment | None = None,
) -> ProtectedResourceVerifierContract:
    active_deployment = deployment or resolve_deployment(settings)
    policy = runtime_security_profile(active_deployment)
    issuer = str(active_deployment.issuer or settings.issuer).rstrip("/")
    resource = str(active_deployment.protected_resource_identifier or settings.protected_resource_identifier)

    modes: list[str] = ["bearer"]
    if policy.dpop_supported:
        modes.append("dpop")
    if policy.mtls_supported:
        modes.append("mtls")

    required_claims = ["iss", "sub", "aud", "exp", "iat"]
    if policy.sender_constraint_required:
        required_claims.append("cnf")

    replay_expectation = "proof-bound replay resistant" if policy.sender_constraint_required else "bearer replay constrained by token lifetime"
    freshness_expectation = "introspection or local validation required at request time"
    return ProtectedResourceVerifierContract(
        verifier_logic_id=f"resource-verifier:{active_deployment.profile}",
        issuer=issuer,
        accepted_issuers=(issuer,),
        resource=resource,
        accepted_audiences=(resource,),
        accepted_token_classes=("access_token",),
        allowed_algs=("RS256", "ES256", "EdDSA"),
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


def protected_resource_verifier_contract_from_request(request) -> ProtectedResourceVerifierContract:
    return build_protected_resource_verifier_contract(deployment_from_request(request, settings))


__all__ = [
    "ProtectedResourceVerifierContract",
    "build_protected_resource_verifier_contract",
    "protected_resource_verifier_contract_from_request",
]
