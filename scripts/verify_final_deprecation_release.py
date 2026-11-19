"""Verify a final PyPI release and archive its source only after recording proof."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen
import zipfile

from deprecated_lifecycle import ROOT, ensure_release_allowed


def validate_receipt(row: dict, artifact: dict, manifest: dict, receipt: dict) -> None:
    if (
        receipt["package"] != row["name"]
        or receipt["version"] != row["version"]
        or receipt["files"] != artifact["files"]
        or receipt["source_commit"] != manifest["source_commit"]
        or receipt["plan_sha256"] != manifest["plan_sha256"]
        or int(receipt["source_artifact_run"]) != int(manifest["workflow_run"])
        or receipt["pypi_hashes"] != "passed"
        or (artifact["name"], artifact["version"], artifact["path"])
        != (row["name"], row["version"], row["path"])
        or receipt["publisher"].get("repository") != "tigrbl/tigrbl_auth"
        or receipt["publisher"].get("workflow") != "monorepo-package-release.yml"
        or receipt["publisher"].get("environment")
        not in {"pypi", f"pypi-{row['name']}"}
    ):
        raise ValueError("Release receipt does not match the immutable CI artifacts")
    install = receipt["clean_install"]
    migration = install.get("migration_check", {})
    expected = {(m["legacy"], m["replacement"]) for m in row["migration_modules"]}
    actual = {(m["legacy"], m["replacement"]) for m in migration.get("modules", [])}
    if (
        install.get("passed") is not True
        or install.get("mode") != "pypi-only"
        or (install.get("name"), install.get("version"))
        != (row["name"], row["version"])
        or install.get("dependency_check") != "passed"
        or migration.get("passed") is not True
        or migration.get("module_count") != len(expected)
        or actual != expected
        or not all(
            m.get("warning_verified") is True
            and m.get("exports_verified") is True
            and m.get("isolated") is True
            for m in migration.get("modules", [])
        )
    ):
        raise ValueError("Final release requires complete PyPI-only migration checks")


def dump(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    temporary.replace(path)


def payload(folder: Path) -> dict:
    return {
        p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in folder.rglob("*")
        if p.is_file()
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--package", required=True)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--archive", action="store_true")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    assert manifest["passed"] and not manifest["failures"]
    assert manifest["plan_sha256"] == hashlib.sha256(args.plan.read_bytes()).hexdigest()
    row = next(r for r in plan["packages"] if r["name"] == args.package)
    artifact = next(r for r in manifest["packages"] if r["name"] == args.package)
    validate_receipt(row, artifact, manifest, receipt)
    ensure_release_allowed(row["path"])
    with urlopen(
        f"https://pypi.org/pypi/{row['name']}/{row['version']}/json", timeout=60
    ) as response:
        remote = json.load(response)
    assert remote["info"]["version"] == row["version"]
    description = remote["info"]["description"]
    assert "**Deprecated:**" in description and "### Migration" in description
    assert "Development Status :: 7 - Inactive" in remote["info"]["classifiers"]
    assert (
        remote["info"]["project_urls"]["Replacement"]
        == f"https://pypi.org/project/{row['primary_replacement']}/"
    )
    files = []
    for file in artifact["files"]:
        published = next(f for f in remote["urls"] if f["filename"] == file["filename"])
        assert published["digests"]["sha256"] == file["sha256"]
        assert published["url"].startswith("https://files.pythonhosted.org/")
        with urlopen(published["url"], timeout=60) as response:
            data = response.read()
        assert hashlib.sha256(data).hexdigest() == file["sha256"]
        if file["filename"].endswith(".whl"):
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for module in row["migration_modules"]:
                    assert f"`{module['legacy']}`" in description
                    assert f"`{module['replacement']}`" in description
                    path = module["legacy"].replace(".", "/")
                    source = archive.read(
                        next(
                            p
                            for p in (path + ".py", path + "/__init__.py")
                            if p in archive.namelist()
                        )
                    ).decode()
                    assert "DeprecationWarning" in source
                    assert f'_CANONICAL_MODULE = "{module["replacement"]}"' in source
        files.append(
            dict(filename=file["filename"], sha256=file["sha256"], url=published["url"])
        )
    proof = dict(
        version=row["version"],
        verified=True,
        notice_verified=True,
        migration_verified=True,
        warning_verified=True,
        hashes_verified=True,
        clean_install_verified=True,
        files=files,
        checked_at=datetime.now(timezone.utc).isoformat(),
        receipt=args.receipt.as_posix(),
        source_commit=manifest["source_commit"],
        source_artifact_run=receipt["source_artifact_run"],
        migration_module_count=len(row["migration_modules"]),
    )
    dump(args.evidence, proof)
    if args.archive:
        # Both endpoints must resolve within this checkout's explicit lifecycle
        # directories; never move a computed directory without checking them.
        base = (ROOT / "pkgs/deprecated").resolve()
        source = (ROOT / row["path"]).resolve()
        target = (base / "dead" / row["name"]).resolve()
        assert source.parent == base / "undead" and target.parent == base / "dead"
        assert not target.exists()
        ledger = ROOT / "pkgs/deprecated/lifecycle.json"
        state = json.loads(ledger.read_text(encoding="utf-8"))
        entry = next(r for r in state["packages"] if r["name"] == row["name"])
        assert entry["stage"] == "undead" and entry["path"] == row["path"]
        entry["deprecation_release"] = proof
        entry["pypi"].update(
            latest_version=row["version"], checked_at=proof["checked_at"]
        )
        state["checked_at"] = proof["checked_at"]
        dump(ledger, state)  # Published proof is durable before the move.
        before = payload(source)
        source.rename(target)
        assert payload(target) == before
        entry.update(stage="dead", path=target.relative_to(ROOT).as_posix())
        dump(ledger, state)
    print(
        json.dumps(
            dict(verified=row["name"], version=row["version"], archived=args.archive)
        )
    )


if __name__ == "__main__":
    main()
