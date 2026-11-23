from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from tba_auth.cli.main import main


def _invoke_json(argv: list[str]) -> tuple[int, dict[str, object]]:
    stream = io.StringIO()
    with redirect_stdout(stream):
        rc = main(argv)
    return rc, json.loads(stream.getvalue())


@pytest.mark.conformance
def test_cli_keys_lifecycle_and_jwks_publication_are_stateful(tmp_path: Path) -> None:
    repo_root = tmp_path
    rc, payload = _invoke_json([
        "keys", "generate", "--repo-root", str(repo_root), "--kid", "kid-primary", "--alg", "EdDSA", "--publish", "--format", "json"
    ])
    assert rc == 0
    assert payload["record"]["id"] == "kid-primary"

    rc, payload = _invoke_json([
        "keys", "rotate", "--repo-root", str(repo_root), "--id", "kid-primary", "--publish", "--format", "json"
    ])
    assert rc == 0
    rotated_id = payload["record"]["id"]
    assert rotated_id == "kid-primary"
    assert payload["record"]["status"] == "active"
    assert payload["record"]["data"]["rotated_at"]

    rc, payload = _invoke_json([
        "keys", "retire", "--repo-root", str(repo_root), "--id", rotated_id, "--publish", "--format", "json"
    ])
    assert rc == 0
    assert payload["record"]["status"] == "retired"

    rc, payload = _invoke_json([
        "keys", "publish-jwks", "--repo-root", str(repo_root), "--format", "json"
    ])
    assert rc == 0
    assert payload["summary"]["keys"] >= 1

    jwks_path = repo_root / "dist" / "jwks" / "jwks.json"
    assert jwks_path.exists()
