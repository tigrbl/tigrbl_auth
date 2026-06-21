from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import runtime_security_profile, security_bcp_profile


def test_rfc9700_security_bcp_profile_exposes_requirements():
    profile = security_bcp_profile()
    assert "require_tls" in profile
    assert "pkce_required" in profile


def test_hardening_profile_is_fail_closed_for_implicit_and_password():
    profile = runtime_security_profile(profile="hardening")
    assert profile.require_tls is True
    assert profile.pkce_required is True
    assert profile.password_grant_allowed is False
    assert profile.implicit_hybrid_allowed is False
    assert profile.sender_constraint_required is True
