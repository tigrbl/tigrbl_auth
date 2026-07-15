from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    runtime_security_profile,
)


def test_rfc9449_dpop_is_advertised_and_exposed_on_token_surfaces():
    deployment = deployment_from_options(profile="hardening")
    metadata = build_openid_config(deployment)
    policy = runtime_security_profile(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert policy.dpop_supported is True
    assert metadata["dpop_signing_alg_values_supported"] == ["EdDSA"]
    assert any(
        param["name"] == "DPoP"
        for param in openapi["paths"]["/token"]["post"]["parameters"]
    )
    assert any(
        param["name"] == "DPoP"
        for param in openapi["paths"]["/token/exchange"]["post"]["parameters"]
    )
