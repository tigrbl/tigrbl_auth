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
def test_cli_import_export_portability_round_trip(tmp_path: Path) -> None:
    source = tmp_path / "source"
    target = tmp_path / "target"
    artifact = source / "dist" / "exports" / "export.json"
    _invoke_json(["tenant", "create", "--repo-root", str(source), "--id", "tenant-portable", "--set", "name=Portable Tenant", "--yes", "--format", "json"])
    _invoke_json(["keys", "generate", "--repo-root", str(source), "--kid", "portable-key", "--alg", "EdDSA", "--format", "json"])

    rc, payload = _invoke_json(["export", "validate", "--repo-root", str(source), "--format", "json"])
    assert rc == 0
    assert payload["valid"] is True

    rc, payload = _invoke_json(["export", "run", "--repo-root", str(source), "--format", "json"])
    assert rc == 0
    assert artifact.exists()
    export_checksum = payload["checksum"]

    rc, payload = _invoke_json(["import", "validate", "--repo-root", str(target), "--input", str(artifact), "--format", "json"])
    assert rc == 0
    assert payload["valid"] is True
    assert payload["declared_checksum"] == payload["computed_checksum"]
    assert export_checksum

    rc, payload = _invoke_json(["import", "run", "--repo-root", str(target), "--input", str(artifact), "--format", "json"])
    assert rc == 0
    assert payload["status"] == "imported"

    rc, payload = _invoke_json(["tenant", "get", "--repo-root", str(target), "--id", "tenant-portable", "--format", "json"])
    assert rc == 0
    assert payload["record"]["id"] == "tenant-portable"
