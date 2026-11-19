"""Publish the inspected release batch and verify PyPI file digests."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import time
from urllib.error import HTTPError
from urllib.request import urlopen

from build_standards_release import inspect_artifacts


class ReleaseIncompleteError(ValueError):
    """PyPI has not exposed both uploaded distribution files yet."""


def remote_files(row: dict) -> dict:
    try:
        with urlopen(
            f"https://pypi.org/pypi/{row['name']}/{row['version']}/json", timeout=60
        ) as response:
            return {
                f["filename"]: f["digests"]["sha256"]
                for f in json.load(response)["urls"]
            }
    except HTTPError as error:
        if error.code == 404:
            return {}
        raise


def check(row: dict, required: bool = False) -> bool:
    files = remote_files(row)
    for file in row["files"]:
        digest = files.get(file["filename"])
        if digest is not None and digest != file["sha256"]:
            raise ValueError(f"PyPI hash conflict: {file['filename']}")
    complete = all(file["filename"] in files for file in row["files"])
    if required and not complete:
        raise ReleaseIncompleteError(
            f"PyPI release incomplete: {row['name']}=={row['version']}"
        )
    return complete


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--dist", required=True, type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    manifest = json.loads((args.dist / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["passed"] and not manifest["failures"]
    assert manifest["plan_sha256"] == hashlib.sha256(args.plan.read_bytes()).hexdigest()
    rows = {row["name"]: row for row in manifest["packages"]}
    assert len(rows) == len(plan["packages"])
    for row in plan["packages"]:
        assert rows[row["name"]]["version"] == row["version"]
        assert (
            inspect_artifacts(row, args.dist / row["name"])
            == rows[row["name"]]["files"]
        )
    # Reject every existing hash conflict before starting any upload.
    with ThreadPoolExecutor(max_workers=8) as pool:
        existing = dict(zip(rows, pool.map(check, rows.values()), strict=True))
    if not args.verify_only:
        for index, row in enumerate(rows.values(), 1):
            if not existing[row["name"]]:
                files = [
                    str(args.dist / row["name"] / file["filename"])
                    for file in row["files"]
                ]
                subprocess.run(
                    [
                        "uv",
                        "publish",
                        "--check-url",
                        "https://pypi.org/simple/",
                        *files,
                    ],
                    check=True,
                )
            print(
                f"Published {index}/{len(rows)}: {row['name']}=={row['version']}",
                flush=True,
            )
    for attempt in range(6):
        try:
            with ThreadPoolExecutor(max_workers=8) as pool:
                list(pool.map(lambda row: check(row, required=True), rows.values()))
            break
        except (ValueError, HTTPError):
            if attempt == 5:
                raise
            time.sleep(10)
    receipt = dict(
        passed=True,
        package_count=len(rows),
        file_count=sum(len(r["files"]) for r in rows.values()),
        plan_sha256=manifest["plan_sha256"],
        verification="All PyPI wheel and sdist SHA256 hashes match the inspected artifacts",
        packages=list(rows.values()),
    )
    (args.dist / "pypi-verification.json").write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    print(f"Verified {len(rows)} PyPI releases and their exact file hashes", flush=True)


if __name__ == "__main__":
    main()
