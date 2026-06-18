"""Executable verifier-grade protected-resource contracts."""

from __future__ import annotations

from dataclasses import dataclass

from tigrbl_identity_runtime.deployment import ResolvedDeployment, deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_auth_protocol_oauth.standards.rfc9700 import runtime_security_profile

ML_DSA_65_ALG = "ML-DSA-65"


def _pqc_jose_enabled() -> bool:
    configured = str(getattr(settings, "jwt_signing_alg", "") or "").replace("_", "-").upper()
    return bool(getattr(settings, "enable_pqc_jose", False)) or configured in {"ML-DSA-65", "MLDSA65"}


def _allowed_token_algs() -> tuple[str, ...]:
    algs = ["RS256", "ES256", "EdDSA"]
    if _pqc_jose_enabled():
        algs.append(ML_DSA_65_ALG)
    return tuple(algs)


@dataclass(frozen=True, slots=True)
class ProtectedResourceVerifierContract:
    verifier_logic_id: str
    issuer: str
    accepted_issuers: tuple[str, ...]
    resource: str
    accepted_audiences: tuple[str, ...]
    accepted_token_classes: tuple[str, ...]
    allowed_algs: tuple[str, ...]
    sender_constraint_modes: tuple[str, ...]
    sender_constraint_required: bool
    required_claims: tuple[str, ...]
    replay_expectation: str
    freshness_expectation: str
    introspection_auth_methods: tuple[str, ...]

    def as_metadata_projection(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "resource": self.resource,
            "authorization_servers": list(self.accepted_issuers),
            "token_types_supported": list(self.accepted_token_classes),
            "allowed_algorithms": list(self.allowed_algs),
            "proof_modes_supported": list(self.sender_constraint_modes),
            "proof_binding_required": self.sender_constraint_required,
            "required_claims": list(self.required_claims),
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
        allowed_algs=_allowed_token_algs(),
        sender_constraint_modes=tuple(dict.fromkeys(modes)),
        sender_constraint_required=bool(policy.sender_constraint_required),
        required_claims=tuple(required_claims),
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
