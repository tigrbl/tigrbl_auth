from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config


def test_production_contract_exposes_registration_management_and_jwt_access_token_metadata():
    deployment = deployment_from_options(profile="production")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    metadata = build_openid_config(profile="production")
    assert "/register/{client_id}" in deployment.active_routes
    assert "/register/{client_id}" in openapi["paths"]
    assert metadata["access_token_signing_alg_values_supported"] == ["EdDSA"]


def test_hardening_contract_exposes_capability_hardening_surfaces_and_metadata():
    deployment = deployment_from_options(profile="hardening")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    metadata = build_openid_config(profile="hardening")
    assert metadata["request_parameter_supported"] is True
    assert metadata["resource_parameter_supported"] is True
    assert metadata["authorization_details_types_supported"] == ["*"]
    assert "/register/{client_id}" in openapi["paths"]
