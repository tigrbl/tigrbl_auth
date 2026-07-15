
from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config


def test_rfc9101_jar_is_advertised_on_authorize_and_par_surfaces():
    deployment = deployment_from_options(profile="hardening")
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert metadata["request_parameter_supported"] is True
    assert metadata["request_object_signing_alg_values_supported"] == ["HS256", "HS384", "HS512"]
    assert "request" in {param["name"] for param in openapi["paths"]["/authorize"]["get"]["parameters"]}
    assert "request" in openapi["paths"]["/par"]["post"]["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]["properties"]
