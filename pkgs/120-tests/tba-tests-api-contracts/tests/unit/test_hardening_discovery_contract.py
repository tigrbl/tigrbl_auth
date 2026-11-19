from __future__ import annotations

import pytest

from tba_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tba_auth.config.settings import settings
from tba_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile
from tba_protocol_oidc.standards.discovery_metadata import build_openid_config


def test_hardening_discovery_and_contract_are_truthful_for_sender_constraints_and_logout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc8705", True)
    monkeypatch.setattr(settings, "enable_rfc9449", True)
    monkeypatch.setattr(settings, "enable_rfc9700", True)
    monkeypatch.setattr(settings, "enable_oidc_frontchannel_logout", True)
    monkeypatch.setattr(settings, "enable_oidc_backchannel_logout", True)
    deployment = deployment_from_options(profile="hardening")
    policy = runtime_security_profile(deployment)
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-capability")

    assert policy.sender_constraint_required is True
    assert metadata["dpop_signing_alg_values_supported"] == ["EdDSA"]
    assert metadata["tls_client_certificate_bound_access_tokens"] is True
    assert metadata["frontchannel_logout_supported"] is True
    assert metadata["backchannel_logout_supported"] is True
    runtime_meta = openapi["paths"]["/token"]["post"]["x-runtime-profile"]
    assert runtime_meta["query_bearer_disabled"] is True
    assert runtime_meta["form_bearer_disabled"] is True
    logout_schema = openapi["components"]["schemas"]["LogoutResponse"]["properties"]
    assert "frontchannel_delivery" in logout_schema
    assert "backchannel_delivery" in logout_schema
