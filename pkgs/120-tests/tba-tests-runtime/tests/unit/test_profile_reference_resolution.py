from __future__ import annotations

from pathlib import Path

import pytest

from tba_auth.config.profile_loader import RuntimeProfileError, load_profile_reference


ROOT = Path(__file__).resolve().parents[5]
EXTERNAL_PROFILE = (
    ROOT
    / "pkgs/120-tests/tba-tests-runtime/tests/fixtures/profiles/external-production.yaml"
)


def test_profile_reference_union_accepts_packaged_profile_ids() -> None:
    profile = load_profile_reference("production")
    deployment = profile.resolve()

    assert profile.source_kind == "packaged-profile-id"
    assert deployment.profile == "production"
    assert deployment.profile_source["kind"] == "packaged-profile-id"


def test_profile_reference_union_accepts_external_yaml_paths() -> None:
    profile = load_profile_reference(str(EXTERNAL_PROFILE))
    deployment = profile.resolve()

    assert profile.id == "external-production"
    assert profile.base_profile == "production"
    assert deployment.profile == "production"
    assert deployment.profile_source["kind"] == "external-profile-path"
    assert deployment.profile_source["path"].endswith("external-production.yaml")


def test_external_profile_yaml_validation_fails_closed(tmp_path: Path) -> None:
    missing = tmp_path / "missing.yaml"
    directory = tmp_path / "profiles"
    directory.mkdir()
    bad_extension = tmp_path / "external.json"
    bad_extension.write_text("{}", encoding="utf-8")
    malformed = tmp_path / "bad.yaml"
    malformed.write_text(":", encoding="utf-8")
    bad_base = tmp_path / "bad-base.yaml"
    bad_base.write_text(
        """
schema_version: "0.1.0"
id: "external"
title: "External"
base_profile: "unknown"
description: "Bad profile"
surface_plugin_mode: "public-only"
surfaces: {}
surface_sets: []
flags: {enabled: []}
protocol_slices: []
extensions: []
security: {}
contracts: {}
""",
        encoding="utf-8",
    )
    unknown_field = tmp_path / "unknown-field.yaml"
    unknown_field.write_text(
        """
schema_version: "0.1.0"
id: "external"
title: "External"
base_profile: "baseline"
description: "Bad profile"
surface_plugin_mode: "public-only"
surfaces: {}
surface_sets: []
flags: {enabled: []}
protocol_slices: []
extensions: []
security: {}
contracts: {}
unexpected: true
""",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeProfileError, match="does not exist"):
        load_profile_reference(str(missing))
    with pytest.raises(RuntimeProfileError, match="not a file"):
        load_profile_reference(str(directory))
    with pytest.raises(RuntimeProfileError, match="must end in"):
        load_profile_reference(str(bad_extension))
    with pytest.raises(RuntimeProfileError, match="must contain a YAML mapping"):
        load_profile_reference(str(malformed))
    with pytest.raises(RuntimeProfileError, match="unknown profile id"):
        load_profile_reference(str(bad_base))
    with pytest.raises(RuntimeProfileError, match="unknown top-level fields"):
        load_profile_reference(str(unknown_field))


def test_profile_reference_fail_closed_errors_are_actionable() -> None:
    with pytest.raises(
        RuntimeProfileError, match="unknown packaged runtime profile id"
    ):
        load_profile_reference("unknown-profile")


def test_profile_provenance_output_reports_source_and_overrides() -> None:
    deployment = load_profile_reference(str(EXTERNAL_PROFILE)).resolve()

    assert deployment.profile_source["kind"] == "external-profile-path"
    assert deployment.profile_source["base_profile"] == "production"
    assert "enable_rfc6749" in deployment.profile_source["applied_override_keys"]
    assert deployment.profile_source["redaction"] == "no-secret-values-emitted"
