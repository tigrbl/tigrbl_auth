from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config


def test_rfc9700_hardening_contract_and_metadata_are_fail_closed() -> None:
    deployment = deployment_from_options(profile="hardening")
    policy = runtime_security_profile(deployment)
    metadata = build_openid_config(profile="hardening")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")

    assert policy.require_tls is True
    assert policy.pkce_required is True
    assert policy.password_grant_allowed is False
    assert policy.implicit_hybrid_allowed is False
    assert metadata["require_pushed_authorization_requests"] is True
    assert "password" not in metadata["grant_types_supported"]
    assert openapi["paths"]["/authorize"]["get"]["parameters"][0]["schema"]["enum"] == ["code"]
