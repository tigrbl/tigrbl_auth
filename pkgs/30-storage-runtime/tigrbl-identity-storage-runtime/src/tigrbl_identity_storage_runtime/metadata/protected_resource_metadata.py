"""OAuth 2.0 Protected Resource Metadata (RFC 9728)."""

from __future__ import annotations

from typing import Final

from tigrbl_identity_runtime.deployment import ResolvedDeployment, deployment_from_app, deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl import Request, TigrblApp, TigrblRouter
from tigrbl.runtime.status import HTTPException, status
from tigrbl_identity_runtime.http_standards.well_known import WELL_KNOWN_ENDPOINTS
from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import ISSUER, JWKS_PATH
from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import build_protected_resource_verifier_contract
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile

RFC9728_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9728"
ML_DSA_65_ALG: Final[str] = "ML-DSA-65"

api = TigrblRouter()
router = api


def _pqc_jose_enabled() -> bool:
    configured = str(getattr(settings, "jwt_signing_alg", "") or "").replace("_", "-").upper()
    return bool(getattr(settings, "enable_pqc_jose", False)) or configured in {"ML-DSA-65", "MLDSA65"}


def _access_token_signing_algs() -> list[str]:
    algs = ["EdDSA"]
    if _pqc_jose_enabled():
        algs.append(ML_DSA_65_ALG)
    return algs


def build_protected_resource_metadata(deployment: ResolvedDeployment | None = None) -> dict[str, object]:
    active_deployment = deployment or resolve_deployment(settings)
    policy = runtime_security_profile(active_deployment)
    verifier_contract = build_protected_resource_verifier_contract(active_deployment)
    methods = ["header"]
    if bool(active_deployment.flags.get("enable_rfc6750_form", getattr(settings, "enable_rfc6750_form", False))):
        methods.append("body")
    if bool(active_deployment.flags.get("enable_rfc6750_query", getattr(settings, "enable_rfc6750_query", False))):
        methods.append("query")

    issuer = verifier_contract.issuer or ISSUER
    metadata = {
        "resource": verifier_contract.resource,
        "authorization_servers": list(verifier_contract.accepted_issuers),
        "jwks_uri": f"{issuer}{JWKS_PATH}",
        "bearer_methods_supported": methods,
        "dpop_signing_alg_values_supported": ["EdDSA"] if policy.dpop_supported else [],
        "tls_client_certificate_bound_access_tokens": bool(policy.mtls_supported or policy.sender_constraint_required),
        "fapi_profiles_supported": ["fapi2-security"] if policy.fapi_mode else [],
        "resource_documentation": f"{issuer}/docs/resource-metadata",
        "scopes_supported": ["openid", "profile", "email"],
        "access_token_signing_alg_values_supported": _access_token_signing_algs(),
        "active_targets": list(active_deployment.active_targets),
        **verifier_contract.as_metadata_projection(),
    }
    return metadata


@api.route(WELL_KNOWN_ENDPOINTS["oauth_protected_resource"], methods=["GET"], include_in_schema=True, tags=[".well-known"])
async def oauth_protected_resource_metadata(request: Request):
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled(WELL_KNOWN_ENDPOINTS["oauth_protected_resource"]):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"RFC 9728 disabled: {RFC9728_SPEC_URL}",
        )
    return build_protected_resource_metadata(deployment)


def include_rfc9728(app: TigrblApp) -> None:
    path = WELL_KNOWN_ENDPOINTS["oauth_protected_resource"]
    deployment = deployment_from_app(app, settings)
    if deployment.route_enabled(path) and not any((getattr(route, "path", None) or getattr(route, "path_template", None)) == path for route in app.router.routes):
        app.include_router(api)


__all__ = [
    "RFC9728_SPEC_URL",
    "api",
    "router",
    "build_protected_resource_metadata",
    "include_rfc9728",
]
