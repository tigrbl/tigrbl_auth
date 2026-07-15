from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.standards.oidc.discovery_metadata import build_openid_config
from tigrbl_auth.standards.oidc.rp_initiated_logout import describe


def test_oidc_rp_initiated_logout_route_is_active_in_production():
    deployment = resolve_deployment(None, profile="production")
    assert "/logout" in deployment.active_routes


def test_oidc_rp_initiated_logout_route_is_active_in_hardening():
    deployment = resolve_deployment(None, profile="hardening")
    assert "/logout" in deployment.active_routes


def test_oidc_rp_initiated_logout_discovery_is_truthful():
    deployment = resolve_deployment(None, profile="production")
    metadata = build_openid_config(deployment)
    assert metadata["end_session_endpoint"].endswith("/logout")
    assert "check_session_iframe" not in metadata


def test_oidc_rp_initiated_logout_description_reports_validation_support():
    description = describe()
    assert description["id_token_hint_validation_supported"] is True
    assert description["post_logout_redirect_uri_validation_supported"] is True
