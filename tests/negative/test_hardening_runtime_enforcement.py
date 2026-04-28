import pytest

from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.standards.oauth2.rfc9700 import (
    OAuthPolicyViolation,
    assert_authorization_request_allowed,
    assert_token_request_allowed,
)


def test_hardening_profile_rejects_password_grant():
    deployment = resolve_deployment(None, profile="hardening")
    with pytest.raises(OAuthPolicyViolation) as exc:
        assert_token_request_allowed({"grant_type": "password"}, deployment)
    assert exc.value.error == "unsupported_grant_type"


def test_hardening_profile_rejects_implicit_flow():
    deployment = resolve_deployment(None, profile="hardening")
    with pytest.raises(OAuthPolicyViolation) as exc:
        assert_authorization_request_allowed(
            {
                "response_type": "token",
                "client_id": "client",
                "redirect_uri": "https://client.example/callback",
                "scope": "openid",
                "code_challenge": "abc",
            },
            deployment,
        )
    assert exc.value.error == "unsupported_response_type"


def test_hardening_profile_requires_par_when_enabled():
    deployment = resolve_deployment(None, profile="hardening")
    with pytest.raises(OAuthPolicyViolation) as exc:
        assert_authorization_request_allowed(
            {
                "response_type": "code",
                "client_id": "client",
                "redirect_uri": "https://client.example/callback",
                "scope": "openid",
                "code_challenge": "abc",
            },
            deployment,
        )
    assert exc.value.error == "invalid_request"
