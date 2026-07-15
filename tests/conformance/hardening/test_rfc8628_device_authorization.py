
from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config


def test_rfc8628_device_authorization_is_published():
    deployment = deployment_from_options(profile="hardening")
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert "/device_authorization" in deployment.active_routes
    assert metadata["device_authorization_endpoint"].endswith("/device_authorization")
    assert "/device_authorization" in openapi["paths"]
