from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_no_plaintext_bootstrap_keys_remain_in_preserved_reports() -> None:
    offenders: list[str] = []
    for path in (
        ROOT / "docs" / "compliance",
        ROOT / "compliance" / "evidence",
    ):
        for report in path.rglob("*.json"):
            text = report.read_text(encoding="utf-8", errors="ignore")
            if "bootstrap_key=" in text:
                offenders.append(report.relative_to(ROOT).as_posix())

    assert offenders == []
