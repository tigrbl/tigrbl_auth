"""Publication eligibility and evidence requirements for retired distributions."""

from __future__ import annotations

import json
from pathlib import Path
import re

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 release tooling
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
STAGES = ("never-lived", "undead", "dead")


def inventory(root: Path = ROOT) -> list[dict]:
    return json.loads(
        (root / "pkgs/deprecated/lifecycle.json").read_text(encoding="utf-8")
    )["packages"]


def ensure_release_allowed(path: str | Path, root: Path = ROOT) -> None:
    parts = Path(path).parts
    if parts[:2] != ("pkgs", "deprecated"):
        return
    if len(parts) != 4 or parts[2] != "undead":
        raise ValueError(
            "Deprecated releases require an explicitly selected undead package; never-lived and dead packages must not be published"
        )
    matches = [row for row in inventory(root) if row["path"] == Path(path).as_posix()]
    if (
        len(matches) != 1
        or matches[0]["stage"] != "undead"
        or matches[0]["pypi"]["published"] is not True
    ):
        raise ValueError(
            "An undead release requires evidence of a previously published package"
        )


def verify(root: Path = ROOT) -> dict:
    base = root / "pkgs/deprecated"
    failures = []
    rows = inventory(root)
    counts = {stage: 0 for stage in STAGES}
    if {p.name for p in base.iterdir() if p.is_dir()} != set(STAGES):
        failures.append(
            "Deprecated packages must live in exactly never-lived, undead, or dead"
        )
    physical = {
        p.parent.relative_to(root).as_posix() for p in base.glob("*/*/pyproject.toml")
    }
    if {r["path"] for r in rows} != physical or len({r["name"] for r in rows}) != len(
        rows
    ):
        failures.append(
            "Lifecycle inventory must cover every retired package exactly once"
        )
    for row in rows:
        name, stage = row["name"], row["stage"]
        if stage not in STAGES:
            failures.append(f"{name}: unknown lifecycle stage")
            continue
        counts[stage] += 1
        expected = f"pkgs/deprecated/{stage}/{name}"
        if row["path"] != expected:
            failures.append(f"{name}: stage and physical path disagree")
        manifest = root / expected / "pyproject.toml"
        if not manifest.is_file():
            failures.append(f"{name}: missing package manifest")
            continue
        if (
            tomllib.loads(manifest.read_text(encoding="utf-8"))["project"]["name"]
            != name
        ):
            failures.append(f"{name}: distribution name changed")
        if not row["pypi"].get("checked_at"):
            failures.append(f"{name}: missing publication verification time")
        published = row["pypi"].get("published")
        if published is not (stage != "never-lived"):
            failures.append(f"{name}: publication evidence disagrees with lifecycle")
        if stage == "dead":
            proof = row.get("deprecation_release", {})
            checks = (
                "verified",
                "notice_verified",
                "migration_verified",
                "warning_verified",
                "hashes_verified",
            )
            files = proof.get("files", [])
            if (
                not all(proof.get(k) is True for k in checks)
                or not proof.get("version")
                or not files
            ):
                failures.append(
                    f"{name}: graveyard requires a verified published deprecation and migration release"
                )
            if any(
                not re.fullmatch(r"[a-f0-9]{64}", f.get("sha256", ""))
                or not f.get("url", "").startswith("https://files.pythonhosted.org/")
                for f in files
            ):
                failures.append(f"{name}: invalid published artifact receipt")
    return dict(passed=not failures, counts=counts, failures=failures)
