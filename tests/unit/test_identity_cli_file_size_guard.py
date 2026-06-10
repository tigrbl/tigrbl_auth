from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLI_ROOT = ROOT / "pkgs" / "tigrbl-identity-cli" / "src" / "tigrbl_identity_cli"


def test_identity_cli_python_files_stay_under_400_loc() -> None:
    oversized = []
    for path in sorted(CLI_ROOT.rglob("*.py")):
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 400:
            oversized.append(f"{path.relative_to(ROOT).as_posix()} has {len(lines)} LoC")

    assert oversized == []
