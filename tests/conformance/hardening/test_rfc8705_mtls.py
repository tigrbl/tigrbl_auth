
from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile


def test_rfc8705_mtls_metadata_and_contract_surface_are_active():
    deployment = deployment_from_options(profile="hardening")
    policy = runtime_security_profile(deployment)
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert policy.mtls_supported is True
    assert metadata["tls_client_certificate_bound_access_tokens"] is True
    assert "tls_client_auth" in metadata["token_endpoint_auth_methods_supported"]
    assert "self_signed_tls_client_auth" in metadata["token_endpoint_auth_methods_supported"]
    assert any(param["name"] == "X-Client-Cert-SHA256" for param in openapi["paths"]["/token"]["post"]["parameters"])
    assert any(param["name"] == "X-Client-Cert-SHA256" for param in openapi["paths"]["/token/exchange"]["post"]["parameters"])
