from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAX_LOC = 400
CHECK_ROOTS = ("pkgs", "tigrbl_auth")
IGNORED_PARTS = {"__pycache__", "build", "dist"}


def test_identity_package_python_files_stay_under_400_loc() -> None:
    oversized: list[str] = []
    for root_name in CHECK_ROOTS:
        root = ROOT / root_name
        for path in sorted(root.rglob("*.py")):
            if IGNORED_PARTS.intersection(path.parts):
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            if len(lines) > MAX_LOC:
                oversized.append(
                    f"{path.relative_to(ROOT).as_posix()} has {len(lines)} LoC"
                )

    assert not oversized, "Python files must stay at or below 400 LoC:\n" + "\n".join(
        oversized
    )
