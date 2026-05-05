from __future__ import annotations

from pathlib import Path

from tigrbl_auth.cli.truth import _hash_file


def test_truth_chain_text_artifact_hash_ignores_line_endings(tmp_path: Path) -> None:
    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    lf.write_text('{\n  "passed": true\n}\n', encoding="utf-8", newline="\n")
    crlf.write_text('{\n  "passed": true\n}\n', encoding="utf-8", newline="\r\n")

    assert _hash_file(lf) == _hash_file(crlf)
