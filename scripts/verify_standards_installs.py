"""Install every planned distribution in a separate, clean Python environment."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import subprocess
import tempfile
import time


def run(command: list[str]) -> str:
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
    )
    if process.returncode:
        raise RuntimeError(process.stdout + process.stderr)
    return process.stdout


def install_release(
    command: list[str], row: dict, attempts: int = 31, interval: int = 10
) -> str:
    """Wait only for the selected new version to reach PyPI's install index."""
    unavailable = f"there is no version of {row['name']}=={row['version']}"
    for attempt in range(attempts):
        try:
            return run(command)
        except RuntimeError as error:
            if unavailable not in str(error) or attempt == attempts - 1:
                raise
            print(
                f"Waiting for {row['name']}=={row['version']} in PyPI's install index",
                flush=True,
            )
            time.sleep(interval)
    raise AssertionError("Install attempts must be positive")


def verify(
    row: dict, output: Path, wheels: Path | None, environment_root: Path
) -> dict:
    destination = output / row["name"]
    destination.mkdir(parents=True, exist_ok=True)
    receipt = destination / "receipt.json"
    mode = "local-wheel-preflight" if wheels else "pypi-only"
    if receipt.exists():
        prior = json.loads(receipt.read_text())
        if (
            prior["version"] == row["version"]
            and prior["mode"] == mode
            and prior["passed"]
        ):
            return prior
    try:
        with tempfile.TemporaryDirectory(
            prefix="install-", dir=environment_root
        ) as temporary:
            environment = Path(temporary)
            run(["uv", "venv", "--python", "3.12", str(environment / "venv")])
            python = (
                environment
                / "venv"
                / (
                    "Scripts/python.exe"
                    if __import__("os").name == "nt"
                    else "bin/python"
                )
            )
            command = [
                "uv",
                "pip",
                "install",
                "--refresh",
                "--python",
                str(python),
                "--no-config",
                "--index-url",
                "https://pypi.org/simple/",
            ]
            if wheels:
                command += ["--find-links", str(wheels)]
            command.append(f"{row['name']}=={row['version']}")
            installed = run(command) if wheels else install_release(command, row)
            (destination / "install.log").write_text(installed, encoding="utf-8")
            run(["uv", "pip", "check", "--python", str(python)])
            code = (
                "import importlib,importlib.metadata,json;"
                f"assert importlib.metadata.version({row['name']!r})=={row['version']!r};"
                f"m=importlib.import_module({row['import_root']!r});"
                "print(json.dumps({'module':m.__name__,'origin':m.__file__}))"
            )
            imported = json.loads(
                run(
                    [
                        "uv",
                        "run",
                        "--no-project",
                        "--python",
                        str(python),
                        "python",
                        "-I",
                        "-c",
                        code,
                    ]
                ).splitlines()[-1]
            )
            if str(environment).lower() not in str(imported["origin"]).lower():
                raise ValueError(
                    f"Import did not come from isolated installation: {imported}"
                )
            result = dict(
                name=row["name"],
                version=row["version"],
                passed=True,
                mode=mode,
                imported=imported,
                dependency_check="passed",
            )
    except Exception as error:
        result = dict(
            name=row["name"],
            version=row["version"],
            passed=False,
            mode=mode,
            error=str(error),
        )
    receipt.write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--wheels", type=Path)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--environment-root", type=Path)
    args = parser.parse_args()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    environment_root = (args.environment_root or args.out / "environments").resolve()
    environment_root.mkdir(parents=True, exist_ok=True)
    rows = json.loads(args.plan.read_text(encoding="utf-8"))["packages"]
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(verify, row, args.out, args.wheels, environment_root)
            for row in rows
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if not result["passed"]:
                print(f"FAILED {result['name']}: {result['error'][-1200:]}", flush=True)
            if len(results) % 25 == 0 or len(results) == len(rows):
                print(
                    f"Clean installs {len(results)}/{len(rows)}; failures {sum(not r['passed'] for r in results)}",
                    flush=True,
                )
    report = dict(
        passed=all(r["passed"] for r in results),
        packages=sorted(results, key=lambda r: r["name"]),
    )
    (args.out / "report.json").write_text(
        json.dumps(report, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    return int(not report["passed"])


if __name__ == "__main__":
    raise SystemExit(main())
