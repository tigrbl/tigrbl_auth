from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


def package_src(name: str) -> Path:
    matches = sorted(PKGS.glob(f"**/{name}/src"))
    assert matches, f"missing package src for {name}"
    return matches[0]


OAUTH_ROOT = package_src("tigrbl-auth-protocol-oauth")


def test_oauth_protocol_modules_do_not_use_raw_table_mutation_handlers() -> None:
    offenders: list[str] = []
    forbidden = ("handlers.create.core", "handlers.update.core", "handlers.delete.core", "handlers.clear.core")
    for path in OAUTH_ROOT.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in source:
                offenders.append(f"{path.relative_to(ROOT).as_posix()} uses {token}")

    assert offenders == []
