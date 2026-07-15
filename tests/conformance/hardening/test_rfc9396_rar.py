from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config


def test_rfc9396_rar_is_advertised_and_exposed_on_authorize_and_par():
    deployment = deployment_from_options(profile="hardening")
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert metadata["authorization_details_types_supported"] == ["*"]
    assert "authorization_details" in {
        param["name"] for param in openapi["paths"]["/authorize"]["get"]["parameters"]
    }
    assert (
        "authorization_details"
        in openapi["paths"]["/par"]["post"]["requestBody"]["content"][
            "application/x-www-form-urlencoded"
        ]["schema"]["properties"]
    )
