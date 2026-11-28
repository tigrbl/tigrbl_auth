from __future__ import annotations

import json
from pathlib import Path

import pytest

from tba_auth.cli.main import main
from tba_auth.cli.metadata import (
    ARGUMENT_SPECS,
    GLOBAL_ARGUMENT_KEYS,
    build_cli_contract_manifest,
    build_parser,
)


ROOT = Path(__file__).resolve().parents[5]
EXTERNAL_PROFILE = (
    ROOT
    / "pkgs/120-tests/tba-tests-runtime/tests/fixtures/profiles/external-production.yaml"
)


def test_cli_profile_runtime_wiring_uses_resolved_deployment(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = main(
        [
            "discovery",
            "show",
            "--repo-root",
            str(ROOT),
            "--profile",
            str(EXTERNAL_PROFILE),
            "--format",
            "json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload["profile"] == "production"
    assert payload["profile_source"]["kind"] == "external-profile-path"


def test_cli_config_is_removed_as_duplicate_selector() -> None:
    parser = build_parser()
    contract = build_cli_contract_manifest()

    assert "config" not in ARGUMENT_SPECS
    assert "config" not in GLOBAL_ARGUMENT_KEYS
    assert "--config" not in parser.format_help()
    assert all(flag["key"] != "config" for flag in contract["global_flags"])
    with pytest.raises(SystemExit):
        parser.parse_args(["status", "--config", "profile.yaml"])


def test_profile_reference_negative_coverage() -> None:
    parser = build_parser()

    args = parser.parse_args(["serve", "--profile", str(EXTERNAL_PROFILE), "--check"])
    assert args.profile == str(EXTERNAL_PROFILE)
