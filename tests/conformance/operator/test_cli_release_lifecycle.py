from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from tba_auth.cli.main import main


ROOT = Path(__file__).resolve().parents[3]


def _invoke_json(argv: list[str]) -> tuple[int, dict[str, object] | None]:
    stream = io.StringIO()
    with redirect_stdout(stream):
        rc = main(argv)
    raw = stream.getvalue().strip()
    payload = json.loads(raw) if raw.startswith("{") else None
    return rc, payload


@pytest.mark.conformance
def test_cli_release_bundle_sign_verify_round_trip(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"

    rc, payload = _invoke_json([
        "release",
        "bundle",
        "--repo-root",
        str(ROOT),
        "--bundle-dir",
        str(bundle_dir),
        "--format",
        "json",
    ])
    assert rc == 0
    assert payload and payload["command"] == "release.bundle"
    assert bundle_dir.exists()
    assert (bundle_dir / "release-bundle.json").exists()

    rc, payload = _invoke_json([
        "release",
        "sign",
        "--repo-root",
        str(ROOT),
        "--bundle-dir",
        str(bundle_dir),
        "--signing-key",
        "test-key",
        "--format",
        "json",
    ])
    assert rc == 0
    assert payload and payload["command"] == "release.sign"
    assert payload["verification"]["passed"] is True
    assert (bundle_dir / "signature.json").exists()

    rc, payload = _invoke_json([
        "release",
        "verify",
        "--repo-root",
        str(ROOT),
        "--bundle-dir",
        str(bundle_dir),
        "--format",
        "json",
    ])
    assert rc == 0
    assert payload and payload["command"] == "release.verify"
    assert payload["bundle_present"] is True
    assert payload["verification"]["passed"] is True
    assert (bundle_dir / "verification.md").exists()


@pytest.mark.conformance
def test_cli_release_verify_fails_closed_when_bundle_missing(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "missing-bundle"
    rc, payload = _invoke_json([
        "release",
        "verify",
        "--repo-root",
        str(ROOT),
        "--bundle-dir",
        str(bundle_dir),
        "--format",
        "json",
    ])
    assert rc == 1
    assert payload and payload["command"] == "release.verify"
    assert payload["bundle_present"] is False
    assert payload["verification"]["passed"] is False
    assert any("release bundle not found" in failure for failure in payload["verification"]["failures"])
