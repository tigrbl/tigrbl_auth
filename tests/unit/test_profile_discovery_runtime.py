from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.standards.oauth2.rfc9700 import runtime_security_profile
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config



def test_hardening_discovery_metadata_matches_runtime_policy():
    deployment = resolve_deployment(None, profile="hardening")
    metadata = build_openid_config(profile="hardening")
    policy = runtime_security_profile(deployment)
    assert metadata["response_types_supported"] == list(policy.allowed_response_types)
    assert metadata["grant_types_supported"] == list(policy.allowed_grant_types)
    assert metadata["require_pushed_authorization_requests"] is True
    assert metadata["dpop_signing_alg_values_supported"] == ["EdDSA"]
    assert "password" not in metadata["grant_types_supported"]



def test_peer_claim_discovery_metadata_matches_runtime_policy():
    deployment = resolve_deployment(None, profile="peer-claim")
    metadata = build_openid_config(profile="peer-claim")
    policy = runtime_security_profile(deployment)
    assert metadata["response_types_supported"] == list(policy.allowed_response_types)
    assert metadata["grant_types_supported"] == list(policy.allowed_grant_types)
    assert metadata["require_pushed_authorization_requests"] is True
    assert "password" not in metadata["grant_types_supported"]



def test_hardening_openapi_contract_reflects_runtime_constraints():
    deployment = deployment_from_options(profile="hardening")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    authorize_get = openapi["paths"]["/authorize"]["get"]
    token_post = openapi["paths"]["/token"]["post"]
    assert authorize_get["parameters"][0]["schema"]["enum"] == ["code"]
    assert any(param["name"] == "request_uri" and param["required"] for param in authorize_get["parameters"])
    policy = runtime_security_profile(resolve_deployment(None, profile="hardening"))
    assert token_post["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]["properties"]["grant_type"]["enum"] == list(policy.allowed_grant_types)
    assert "password" not in token_post["requestBody"]["content"]["application/x-www-form-urlencoded"]["schema"]["properties"]["grant_type"]["enum"]
