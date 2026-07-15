from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config


def test_rfc9126_par_route_is_active_and_required_in_hardening():
    deployment = deployment_from_options(profile="hardening")
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert "/par" in deployment.active_routes
    assert metadata["require_pushed_authorization_requests"] is True
    assert "/par" in openapi["paths"]
