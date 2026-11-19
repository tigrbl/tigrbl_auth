"""Install every planned distribution in a separate, clean Python environment."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import subprocess
import tempfile
import time


MIGRATION_PROBE = """
import importlib, json, pathlib, sys, warnings
rows = json.loads(sys.argv[1])
environment = pathlib.Path(sys.prefix).resolve()
checks = []
for row in rows:
    # A parent may have imported a child; execute each shim again to observe
    # its own warning, without replacing or copying the canonical objects.
    sys.modules.pop(row['legacy'], None)
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter('always', DeprecationWarning)
        legacy = importlib.import_module(row['legacy'])
    canonical = importlib.import_module(row['replacement'])
    expected = f"{row['legacy']} is deprecated; import {row['replacement']} instead."
    assert any(issubclass(w.category, DeprecationWarning) and str(w.message) == expected
               for w in observed), f"Missing migration warning: {expected}"
    for module in (legacy, canonical):
        origin = pathlib.Path(module.__file__).resolve()
        assert origin.is_relative_to(environment), f'Non-isolated module: {origin}'
    exports = getattr(canonical, '__all__', [n for n in vars(canonical) if not n.startswith('_')])
    for name in exports:
        assert getattr(legacy, name) is getattr(canonical, name), f"Changed public object: {row['legacy']}.{name}"
    checks.append(dict(legacy=row['legacy'], replacement=row['replacement'],
                       warning_verified=True, exports_verified=True, isolated=True))
print(json.dumps(dict(passed=True, module_count=len(checks), modules=checks)))
"""


FUNCTIONAL_PROBES = {
    "identity-auth-context": """
import json
from types import SimpleNamespace
from tigrbl.config.constants import TIGRBL_AUTH_CONTEXT_ATTR
from tba_server_identity.security.authn_adapters.context import set_auth_context
request = SimpleNamespace(state=SimpleNamespace())
for principal, expected in [({'tid': 'tenant', 'sub': 'user'}, {'tenant_id': 'tenant', 'user_id': 'user'}),
                            ({'tenant_id': 'tenant', 'user_id': 'user'}, {'tenant_id': 'tenant', 'user_id': 'user'}),
                            (None, {})]:
    set_auth_context(request, principal)
    assert getattr(request.state, TIGRBL_AUTH_CONTEXT_ATTR) == expected
print(json.dumps({'passed': True, 'cases': 3}))
"""
}


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
            and (
                not row.get("migration_modules")
                or prior.get("migration_check", {}).get("module_count")
                == len(row["migration_modules"])
            )
            and set(prior.get("functional_checks", {}))
            == set(row.get("functional_checks", []))
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
            if row.get("migration_modules"):
                result["migration_check"] = json.loads(
                    run(
                        [
                            str(python),
                            "-I",
                            "-c",
                            MIGRATION_PROBE,
                            json.dumps(row["migration_modules"]),
                        ]
                    ).splitlines()[-1]
                )
            if row.get("functional_checks"):
                result["functional_checks"] = {
                    name: json.loads(
                        run(
                            [str(python), "-I", "-c", FUNCTIONAL_PROBES[name]]
                        ).splitlines()[-1]
                    )
                    for name in row["functional_checks"]
                }
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
