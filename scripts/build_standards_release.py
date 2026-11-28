"""Build and inspect every artifact in the committed package standards release plan."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def inspect_artifacts(row: dict, directory: Path) -> list[dict]:
    wheels = list(directory.glob("*.whl"))
    sdists = list(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError(f"{row['name']}: expected exactly one wheel and one sdist")
    source = ROOT / row["path"]
    with zipfile.ZipFile(wheels[0]) as archive:
        metadata_path = next(
            n for n in archive.namelist() if n.endswith(".dist-info/METADATA")
        )
        metadata = BytesParser().parsebytes(archive.read(metadata_path))
        assert metadata["Name"] == row["name"]
        assert metadata["Version"] == row["version"]
        assert metadata["License-Expression"] == "Apache-2.0"
        assert set(metadata.get_all("License-File", [])) == {"LICENSE", "NOTICE"}
        assert metadata["Author"] or metadata["Author-email"]
        description = metadata.get_payload()
        assert f"https://static.pepy.tech/badge/{row['name']}/month" in description
        assert f"{row['path']}/README.md.svg" in description
        assert "docs/assets/tba-brand.png" in description
        base = metadata_path.removesuffix("METADATA") + "licenses/"
        for name in ("LICENSE", "NOTICE"):
            assert archive.read(base + name) == (source / name).read_bytes()
    with tarfile.open(sdists[0]) as archive:
        for name in ("LICENSE", "NOTICE", "README.md", "pyproject.toml"):
            member = next(
                m
                for m in archive.getmembers()
                if m.name.count("/") == 1 and m.name.endswith("/" + name)
            )
            archived = archive.extractfile(member).read()
            original = (source / name).read_bytes()
            if name == "pyproject.toml":
                # uv_build canonicalizes the sdist manifest, including newlines.
                assert tomllib.loads(archived.decode()) == tomllib.loads(
                    original.decode()
                )
            else:
                assert archived == original
    return [
        dict(
            filename=p.name,
            sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            size=p.stat().st_size,
        )
        for p in sorted(wheels + sdists)
    ]


def build(row: dict, destination: Path) -> dict:
    directory = destination / row["name"]
    directory.mkdir(parents=True, exist_ok=True)
    project = tomllib.loads(
        (ROOT / row["path"] / "pyproject.toml").read_text(encoding="utf-8")
    )["project"]
    if (project["name"], project["version"]) != (row["name"], row["version"]):
        raise ValueError(f"Release plan disagrees with {row['path']}")
    if not list(directory.glob("*.whl")) or not list(directory.glob("*.tar.gz")):
        process = subprocess.run(
            [
                "uv",
                "build",
                "--python",
                "3.12",
                "--no-sources",
                "--sdist",
                "--wheel",
                "--out-dir",
                str(directory),
                str(ROOT / row["path"]),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        (directory / "build.log").write_text(process.stdout, encoding="utf-8")
        if process.returncode:
            raise RuntimeError(
                f"{row['name']}: build failed; see {directory / 'build.log'}"
            )
    return dict(
        name=row["name"],
        version=row["version"],
        path=row["path"],
        files=inspect_artifacts(row, directory),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1794952800")
    rows, failures = [], []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(build, row, args.out): row for row in plan["packages"]}
        for future in as_completed(futures):
            try:
                rows.append(future.result())
            except Exception as error:
                failures.append(f"{futures[future]['name']}: {error}")
            count = len(rows) + len(failures)
            if count % 25 == 0 or count == len(futures):
                print(
                    f"Inspected {count}/{len(futures)} packages; {len(failures)} failures",
                    flush=True,
                )
    report = dict(
        passed=not failures,
        packages=sorted(rows, key=lambda r: r["name"]),
        failures=failures,
        plan_sha256=hashlib.sha256(args.plan.read_bytes()).hexdigest(),
        source_date_epoch=os.environ["SOURCE_DATE_EPOCH"],
    )
    (args.out / "manifest.json").write_text(
        json.dumps(report, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    for failure in failures:
        print(failure, flush=True)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
