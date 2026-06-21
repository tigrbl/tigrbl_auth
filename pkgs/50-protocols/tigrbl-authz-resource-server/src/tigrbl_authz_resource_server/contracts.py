"""Executable verifier-grade protected-resource contracts."""

from __future__ import annotations

from tigrbl_identity_runtime.deployment import ResolvedDeployment, deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile
from tigrbl_identity_contracts.resource_server import ProtectedResourceVerifierContract



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
