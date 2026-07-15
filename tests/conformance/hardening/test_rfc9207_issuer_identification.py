from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config


def test_rfc9207_issuer_identification_is_advertised_and_requires_iss_in_hardening():
    deployment = deployment_from_options(profile="hardening")
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert "RFC 9207" in set(deployment.active_targets)
    assert metadata["authorization_response_iss_parameter_supported"] is True
    schema = openapi["paths"]["/authorize"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    assert schema["allOf"][1]["required"] == ["iss"]
