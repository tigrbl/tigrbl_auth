from tba_auth.config.feature_flags import feature_flag_registry, cli_flag_registry, flags_for_profile


def test_feature_flag_registry_contains_required_groups():
    registry = feature_flag_registry()
    assert "baseline" in registry
    assert "production" in registry
    assert "hardening" in registry
    assert "surface" in registry
    assert "alignment_only" in registry


def test_cli_flag_registry_contains_operator_groups():
    registry = cli_flag_registry()
    assert "global" in registry
    assert "serve" in registry
    assert "governance" in registry
    assert "admin" in registry


def test_flags_for_profile_includes_baseline_targets():
    flags = flags_for_profile("baseline")
    assert "enable_rfc6749" in flags
    assert "enable_rfc8414" in flags
