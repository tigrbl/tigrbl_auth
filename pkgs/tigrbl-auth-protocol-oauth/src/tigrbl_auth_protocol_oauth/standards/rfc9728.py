"""OAuth 2.0 Protected Resource Metadata (RFC 9728)."""

from __future__ import annotations

from typing import Final

from tigrbl_identity_runtime.deployment import ResolvedDeployment, deployment_from_app, deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_server.framework import HTTPException, Request, TigrblApp, TigrblRouter, status
from tigrbl_identity_runtime.http_standards.well_known import WELL_KNOWN_ENDPOINTS
from tigrbl_auth_protocol_oauth.standards.rfc8414_metadata import ISSUER, JWKS_PATH
from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import build_protected_resource_verifier_contract
from tigrbl_auth_protocol_oauth.standards.rfc9700 import runtime_security_profile

RFC9728_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9728"

api = TigrblRouter()
router = api


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
