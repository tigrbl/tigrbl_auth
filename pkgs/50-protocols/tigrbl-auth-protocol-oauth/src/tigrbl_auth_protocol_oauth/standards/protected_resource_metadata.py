"""OAuth 2.0 Protected Resource Metadata semantics (RFC 9728)."""

from __future__ import annotations

from typing import Final, Protocol

from tigrbl_identity_core.standards import StandardOwner, describe_owner

from .authorization_server_metadata import ISSUER, JWKS_PATH
from .oauth_security_bcp import runtime_security_profile
from .resource_verifier_contract import build_protected_resource_verifier_contract


RFC9728_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9728"
PROTECTED_RESOURCE_METADATA_PATH: Final[str] = "/.well-known/oauth-protected-resource"
ML_DSA_65_ALG: Final[str] = "ML-DSA-65"
OWNER = StandardOwner(
    label="RFC 9728",
    title="OAuth 2.0 Protected Resource Metadata",
    runtime_status="profile-aware-protected-resource-metadata",
    public_surface=(PROTECTED_RESOURCE_METADATA_PATH,),
    notes=("HTTP publication is composed above the protocol layer.",),
)


class ProtectedResourceDeployment(Protocol):
    profile: str
    issuer: str
    flags: dict[str, bool | str]
    active_targets: tuple[str, ...]

    def flag_enabled(self, name: str) -> bool: ...


def _pqc_jose_enabled(deployment: ProtectedResourceDeployment) -> bool:
    configured = (
        str(deployment.flags.get("jwt_signing_alg", "") or "").replace("_", "-").upper()
    )
    return deployment.flag_enabled("enable_pqc_jose") or configured in {
        "ML-DSA-65",
        "MLDSA65",
    }


def _access_token_signing_algs(
    deployment: ProtectedResourceDeployment,
) -> list[str]:
    algs = ["EdDSA"]
    if _pqc_jose_enabled(deployment):
        algs.append(ML_DSA_65_ALG)
    return algs


def build_protected_resource_metadata(
    deployment: ProtectedResourceDeployment,
) -> dict[str, object]:
    policy = runtime_security_profile(deployment)
    verifier_contract = build_protected_resource_verifier_contract(deployment)
    methods = ["header"]
    if bool(deployment.flags.get("enable_rfc6750_form", False)):
        methods.append("body")
    if bool(deployment.flags.get("enable_rfc6750_query", False)):
        methods.append("query")

    issuer = verifier_contract.issuer or ISSUER
    return {
        "resource": verifier_contract.resource,
        "authorization_servers": list(verifier_contract.accepted_issuers),
        "jwks_uri": f"{issuer}{JWKS_PATH}",
        "bearer_methods_supported": methods,
        "dpop_signing_alg_values_supported": ["EdDSA"] if policy.dpop_supported else [],
        "tls_client_certificate_bound_access_tokens": bool(
            policy.mtls_supported or policy.sender_constraint_required
        ),
        "fapi_profiles_supported": ["fapi2-security"] if policy.fapi_mode else [],
        "resource_documentation": f"{issuer}/docs/resource-metadata",
        "scopes_supported": ["openid", "profile", "email"],
        "access_token_signing_alg_values_supported": _access_token_signing_algs(
            deployment
        ),
        "active_targets": list(deployment.active_targets),
        **verifier_contract.as_metadata_projection(),
    }


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        specification_version="RFC 9728",
        metadata_path=PROTECTED_RESOURCE_METADATA_PATH,
        spec_url=RFC9728_SPEC_URL,
    )


__all__ = [
    "ML_DSA_65_ALG",
    "OWNER",
    "PROTECTED_RESOURCE_METADATA_PATH",
    "RFC9728_SPEC_URL",
    "ProtectedResourceDeployment",
    "build_protected_resource_metadata",
    "describe",
]
