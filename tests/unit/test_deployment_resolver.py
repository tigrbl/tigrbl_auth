from __future__ import annotations

from tigrbl_auth.config.deployment import resolve_deployment


def test_baseline_profile_filters_production_and_hardening_targets() -> None:
    deployment = resolve_deployment()
    assert deployment.profile == "baseline"
    assert "/userinfo" not in deployment.active_routes
    assert "/.well-known/oauth-protected-resource" not in deployment.active_routes
    assert "OIDC UserInfo" not in deployment.active_targets
    assert "RFC 9728" not in deployment.active_targets


def test_plugin_mode_public_only_removes_admin_and_diagnostics_surfaces() -> None:
    deployment = resolve_deployment(plugin_mode="public-only")
    assert deployment.surface_enabled("public-rest") is True
    assert deployment.surface_enabled("admin-rest") is False
    assert deployment.surface_enabled("diagnostics") is False
    assert all(not route.startswith("/system/") for route in deployment.active_routes)
