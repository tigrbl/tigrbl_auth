
from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config


def test_rfc8707_resource_indicators_are_advertised_and_mapped():
    deployment = deployment_from_options(profile="hardening")
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert metadata["resource_parameter_supported"] is True
    assert "resource" in {param["name"] for param in openapi["paths"]["/authorize"]["get"]["parameters"]}
    assert "resource" in openapi["paths"]["/par"]["post"]["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]["properties"]
    assert "resource" in openapi["paths"]["/device_authorization"]["post"]["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]["properties"]
