from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _default_report_path(lane: str) -> Path:
    tox_env = os.environ.get("TOX_ENV_NAME", "").strip()
    if tox_env:
        stem = tox_env
    else:
        stem = f"test-{lane}-py{sys.version_info.major}{sys.version_info.minor}"
    return ROOT / "dist" / "test-reports" / f"{stem}.json"


def _prepare_lane_artifacts(lane: str) -> None:
    if lane != "interop":
        return
    from scripts.materialize_tier4_peer_evidence import (
        load_counterparts,
        load_peer_profiles,
        materialize_external_handoff_templates,
    )

    materialize_external_handoff_templates(load_peer_profiles(), load_counterparts())


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a certification lane with a preserved pytest JSON report and validated-run manifest.")
    parser.add_argument("--lane", required=True)
    parser.add_argument("--report", default=None, help="Override the pytest JSON report path.")
    parser.add_argument("pytest_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    report_path = Path(args.report).resolve() if args.report else _default_report_path(args.lane)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    pytest_args = list(args.pytest_args)
    if pytest_args[:1] == ["--"]:
        pytest_args = pytest_args[1:]

    _prepare_lane_artifacts(args.lane)

    install_env = dict(os.environ)
    install_env.setdefault("TIGRBL_AUTH_INSTALL_PROFILE", f"test-{args.lane}")
    install_cmd = [
        sys.executable,
        str(ROOT / "scripts" / "verify_clean_room_install_substrate.py"),
        "--profile",
        f"test-{args.lane}",
    ]
    subprocess.run(install_cmd, cwd=str(ROOT), env=install_env, check=False)

    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--certification-lane",
        args.lane,
        "--json-report",
        f"--json-report-file={report_path}",
        *pytest_args,
    ]
    result = subprocess.run(pytest_cmd, cwd=str(ROOT), check=False)

    manifest_cmd = [
        sys.executable,
        str(ROOT / "scripts" / "record_validated_run.py"),
        "test-lane",
        "--lane",
        args.lane,
        "--report",
        str(report_path),
        "--pytest-exit-code",
        str(int(result.returncode)),
    ]
    manifest_result = subprocess.run(manifest_cmd, cwd=str(ROOT), check=False)
    if result.returncode != 0:
        return int(result.returncode)
    return int(manifest_result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
