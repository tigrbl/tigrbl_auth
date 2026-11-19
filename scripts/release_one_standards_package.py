"""Prepare, publish externally, then verify exactly one immutable metadata release."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import re
import subprocess
import tempfile
import time

from build_standards_release import inspect_artifacts
from publish_standards_release import ReleaseIncompleteError, check
from verify_standards_installs import verify


def select_release(plan_bytes: bytes, manifest: dict, name: str) -> tuple[dict, dict]:
    if not name or name == "all":
        raise ValueError("Select exactly one package; bulk publishing is disabled")
    plan = json.loads(plan_bytes)
    if not manifest.get("passed") or manifest.get("failures"):
        raise ValueError("The source artifact batch did not pass validation")
    if manifest.get("plan_sha256") != hashlib.sha256(plan_bytes).hexdigest():
        raise ValueError("Artifact manifest does not match the committed release plan")
    if not re.fullmatch(r"[a-f0-9]{40}", manifest.get("source_commit", "")):
        raise ValueError(
            "Fresh CI artifacts must identify their immutable source commit"
        )
    planned = [row for row in plan["packages"] if row["name"] == name]
    built = [row for row in manifest["packages"] if row["name"] == name]
    if len(planned) != 1 or len(built) != 1:
        raise ValueError(f"Expected one planned and built release for {name!r}")
    row, artifact = planned[0], built[0]
    if (row["version"], row["path"]) != (artifact["version"], artifact["path"]):
        raise ValueError(
            "Selected artifact version or source path disagrees with the plan"
        )
    return row, artifact


def ensure_source_tag(row: dict, source_commit: str) -> None:
    tag = f"{row['name']}=={row['version']}"
    prior = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    if prior.returncode == 0:
        if prior.stdout.strip() != source_commit:
            raise ValueError(f"Refusing to replace an existing source tag: {tag}")
    else:
        subprocess.run(["git", "tag", tag, source_commit], check=True)
    subprocess.run(["git", "push", "origin", f"refs/tags/{tag}"], check=True)


def wait_for_pypi_release(
    artifact: dict, attempts: int = 31, interval: int = 10
) -> None:
    """Allow five minutes for PyPI metadata propagation, rejecting hash conflicts."""
    for attempt in range(attempts):
        try:
            check(artifact, required=True)
            return
        except ReleaseIncompleteError:
            if attempt == attempts - 1:
                raise
            print(
                "Waiting for both distribution files in PyPI release metadata",
                flush=True,
            )
            time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--dist", required=True, type=Path)
    parser.add_argument("--package", required=True)
    parser.add_argument("--phase", choices=("prepare", "verify"), required=True)
    parser.add_argument("--source-artifact-run", required=True, type=int)
    parser.add_argument("--out", type=Path, default=Path("prepared-dist"))
    parser.add_argument(
        "--receipt", type=Path, default=Path("trusted-release-receipt.json")
    )
    args = parser.parse_args()
    manifest = json.loads((args.dist / "manifest.json").read_text(encoding="utf-8"))
    if str(manifest.get("workflow_run")) != str(args.source_artifact_run):
        raise ValueError("Distribution manifest does not identify the selected CI run")
    row, artifact = select_release(args.plan.read_bytes(), manifest, args.package)
    directory = args.dist / row["name"]
    if inspect_artifacts(row, directory) != artifact["files"]:
        raise ValueError(
            "Selected wheel/sdist hashes disagree with the validated CI manifest"
        )
    if args.phase == "prepare":
        check(artifact)  # Reject any existing PyPI hash conflict before uploading.
        args.out.mkdir(parents=True, exist_ok=True)
        if list(args.out.iterdir()):
            raise ValueError("Selected-package staging directory must start empty")
        for file in artifact["files"]:
            shutil.copyfile(directory / file["filename"], args.out / file["filename"])
        ensure_source_tag(row, manifest["source_commit"])
        print(f"Prepared only {row['name']}=={row['version']}", flush=True)
        return
    wait_for_pypi_release(artifact)
    result = verify(
        row,
        Path("clean-install-check").resolve(),
        None,
        Path(tempfile.gettempdir()).resolve(),
    )
    receipt = dict(
        package=row["name"],
        version=row["version"],
        files=artifact["files"],
        pypi_hashes="passed",
        clean_install=result,
        publisher=dict(
            repository="tigrbl/tigrbl_auth",
            workflow=os.environ.get(
                "PUBLISHER_WORKFLOW", "monorepo-package-release.yml"
            ),
            environment=os.environ.get("PUBLISHER_ENVIRONMENT", f"pypi-{row['name']}"),
        ),
        source_artifact_run=args.source_artifact_run,
        source_commit=manifest["source_commit"],
        plan_sha256=manifest["plan_sha256"],
    )
    args.receipt.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    if not result["passed"]:
        raise RuntimeError(f"Clean PyPI install failed: {result['error']}")
    print(
        f"Verified PyPI hashes, clean install, dependencies, and import: {row['name']}=={row['version']}",
        flush=True,
    )


if __name__ == "__main__":
    main()
