from __future__ import annotations

import json
from pathlib import Path

import pytest
try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 dependency path
    import tomli as tomllib

from tigrbl_auth.config.deployment import VALID_PROFILES, resolve_deployment
from tigrbl_auth.config.profile_loader import (
    RuntimeProfileError,
    load_packaged_runtime_profiles,
    load_runtime_profile,
    validate_profile_data,
)


ROOT = Path(__file__).resolve().parents[2]


def test_packaged_runtime_profiles_load_and_validate() -> None:
    """Every packaged tigrbl_auth/profiles/*.yaml file loads and validates."""
    profiles = load_packaged_runtime_profiles()

    assert set(profiles) == set(VALID_PROFILES)
    assert profiles["baseline-development"].ssot_profile_id == "prf:baseline-development"
    assert profiles["baseline-development"].feature_id == "feat:profile-baseline-development"


def test_runtime_profile_yaml_files_are_included_in_build_config() -> None:
    """Runtime profiles are package resources, not checkout-only fixtures."""
    pyproject = tomllib.loads(
        (ROOT / "pkgs" / "tigrbl-auth" / "pyproject.toml").read_text(encoding="utf-8")
    )
    includes = pyproject["tool"]["poetry"]["include"]

    assert "src/tigrbl_auth/profiles/*.yaml" in includes


def test_development_profile_is_active_in_ssot_registry() -> None:
    """The packaged development profile is an active certifiable deployment profile."""
    registry = json.loads((ROOT / ".ssot" / "registry.json").read_text(encoding="utf-8"))
    profile_rows = {row["id"]: row for row in registry["profiles"]}

    assert profile_rows["prf:baseline-development"]["status"] == "active"


def test_runtime_profile_loader_fails_closed_for_invalid_profiles() -> None:
    """Malformed, duplicate, missing, or inconsistent profile files fail closed."""
    with pytest.raises(RuntimeProfileError, match="unknown profile id"):
        validate_profile_data(
            {
                "schema_version": "0.1.0",
                "id": "unknown",
                "title": "unknown",
                "ssot_profile_id": "prf:unknown",
                "feature_id": "feat:profile-unknown",
                "description": "Invalid test profile.",
                "surface_plugin_mode": "public-only",
                "surface_sets": ["public-rest"],
                "flags": {"enabled": []},
                "protocol_slices": [],
                "extensions": [],
            }
        )

    with pytest.raises(RuntimeProfileError, match="not packaged"):
        load_runtime_profile("missing")


def test_runtime_profile_resolver_applies_operator_overrides() -> None:
    """Profile files compose with environment and CLI overrides through the resolver."""
    deployment = load_runtime_profile("baseline-development").resolve()
    narrowed = resolve_deployment(
        profile="baseline-development",
        surface_sets=("public-rest",),
        plugin_mode="mixed",
    )

    assert deployment.profile == "baseline-development"
    assert deployment.surface_enabled("public-rest")
    assert deployment.surface_enabled("admin-rest")
    assert deployment.surface_enabled("diagnostics")
    assert narrowed.surface_sets == ("public-rest",)
    assert narrowed.surface_enabled("public-rest")
    assert not narrowed.surface_enabled("admin-rest")
    assert not narrowed.surface_enabled("diagnostics")


def test_runtime_profile_outputs_drive_contracts_and_surfaces() -> None:
    """Routes, diagnostics, OpenAPI, and evidence derive from ResolvedDeployment."""
    deployment = load_runtime_profile("baseline-development").resolve()

    assert "/.well-known/openid-configuration" in deployment.active_contract_routes
    assert "OpenAPI 3.1 / 3.2 compatible public contract" in deployment.active_targets
    assert "OpenRPC 1.4.x admin/control-plane contract" not in deployment.active_targets
    assert deployment.surfaces["surface_diagnostics_enabled"] is True
