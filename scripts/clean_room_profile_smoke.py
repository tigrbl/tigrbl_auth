from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from tigrbl_auth.cli.certification_evidence import current_environment_identity, runtime_identity

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _artifact_stem(*, matrix_profile: str, runner: str | None) -> str:
    tox_env = os.environ.get("TOX_ENV_NAME", "").strip()
    if tox_env:
        return tox_env
    py_tag = f"py{sys.version_info.major}{sys.version_info.minor}"
    return f"{matrix_profile}-{py_tag}-{runner or 'base'}"


def _write_artifact(artifact_dir: Path, payload: dict[str, Any]) -> Path:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / f"{_artifact_stem(matrix_profile=str(payload.get('matrix_profile', 'unknown')), runner=payload.get('runner') or None)}.json"
    artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return artifact_path


def _relative_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean-room install and runtime-path smoke for a certification profile.")
    parser.add_argument("--runner", default=os.environ.get("TIGRBL_AUTH_RUNNER", ""), help="Runner profile to materialize in the runtime plan.")
    parser.add_argument(
        "--require-runner-installed",
        action="store_true",
        default=_env_bool("TIGRBL_AUTH_EXPECT_RUNNER_INSTALLED"),
        help="Fail if the selected runner adapter is not backed by an installed module.",
    )
    parser.add_argument(
        "--probe-surfaces",
        action="store_true",
        default=_env_bool("TIGRBL_AUTH_PROBE_SURFACES"),
        help="Probe discovery, JWKS, and public contract endpoints against the built ASGI app.",
    )
    parser.add_argument(
        "--require-surface-probes",
        action="store_true",
        default=_env_bool("TIGRBL_AUTH_REQUIRE_SURFACE_PROBES"),
        help="Fail if the runtime surface probes do not pass.",
    )
    parser.add_argument(
        "--artifact-dir",
        default=os.environ.get("TIGRBL_AUTH_SMOKE_ARTIFACT_DIR", str(ROOT / "dist" / "runtime-smoke")),
        help="Directory where the runtime smoke artifact should be written.",
    )
    args = parser.parse_args()

    matrix_profile = os.environ.get("TIGRBL_AUTH_MATRIX_PROFILE", "unknown")
    runner = args.runner.strip() or None
    install_profile = os.environ.get("TIGRBL_AUTH_INSTALL_PROFILE", matrix_profile)
    payload: dict[str, Any] = {
        "schema_version": 3,
        "identity": runtime_identity(matrix_profile),
        "matrix_profile": matrix_profile,
        "install_profile": install_profile,
        "tox_env": os.environ.get("TOX_ENV_NAME"),
        "python": sys.version.split()[0],
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "runner": runner,
        "runner_required": bool(args.require_runner_installed),
        "surface_probe_requested": bool(args.probe_surfaces),
        "surface_probe_required": bool(args.require_surface_probes),
        "application_probe_passed": False,
        "runner_check_passed": runner is None,
        "runner_available": None,
        "runner_available_module": None,
        "surface_probe_passed": None,
        "environment_identity": current_environment_identity(matrix_profile=matrix_profile, install_profile=install_profile, runner=runner, repo_root=ROOT),
        "passed": False,
    }
    rc = 0

    try:
        import tigrbl_auth  # noqa: F401
        from tigrbl_auth_backend_app_core import build_app, build_application_runtime_plan
        from tigrbl_auth.cli.runtime import probe_http_surface_endpoints
        from tigrbl_auth.config.deployment import resolve_deployment
        from tigrbl_auth.config.settings import settings
        from tigrbl_auth.runtime import get_runner_adapter
        from tigrbl_auth.tables.engine import dsn

        deployment = resolve_deployment(settings)
        app = build_app(deployment=deployment)
        payload.update(
            {
                "dsn": dsn,
                "deployment_profile": deployment.profile,
                "active_target_count": len(deployment.active_targets),
                "active_route_count": len(deployment.active_routes),
                "application_type": type(app).__name__,
                "application_probe_passed": True,
                "application_probe_message": (
                    f"Application factory materialized successfully with {len(deployment.active_routes)} active routes "
                    f"and {len(deployment.active_targets)} active targets."
                ),
            }
        )

        if runner is not None:
            plan = build_application_runtime_plan(deployment=deployment, runner=runner)
            adapter = get_runner_adapter(runner)
            runner_available = bool(adapter.is_available())
            payload.update(
                {
                    "runtime_plan_runner": plan.runner,
                    "runtime_plan_diagnostics": [item.to_manifest() for item in plan.diagnostics_report],
                    "application_hash": plan.application_hash,
                    "runtime_hash": plan.runtime_hash,
                    "runner_available": runner_available,
                    "runner_available_module": adapter.available_module_name(),
                    "runner_check_passed": runner_available or not args.require_runner_installed,
                }
            )
            if args.require_runner_installed and not runner_available:
                rc = 1
                payload.setdefault("error_type", "ModuleNotFoundError")
                payload.setdefault("error_message", f"Runner '{runner}' is not installed in this environment.")

        if args.probe_surfaces:
            surface_probe = probe_http_surface_endpoints(app=app, deployment=deployment)
            payload["surface_probe"] = surface_probe
            payload["surface_probe_passed"] = bool(surface_probe.get("passed", False))
            if args.require_surface_probes and not payload["surface_probe_passed"]:
                rc = 1
        else:
            payload["surface_probe_passed"] = None

        payload["passed"] = bool(
            rc == 0
            and payload.get("application_probe_passed", False)
            and payload.get("runner_check_passed", True)
            and (
                (not args.require_surface_probes)
                or bool(payload.get("surface_probe_passed", False))
            )
        )
        if not payload["passed"] and rc == 0:
            rc = 1
    except SystemExit as exc:  # pragma: no cover - exercised indirectly via CLI invocations
        code = exc.code if isinstance(exc.code, int) else 1
        rc = int(code)
        payload["passed"] = rc == 0
        payload["error_type"] = "SystemExit"
        payload["error_message"] = str(exc)
    except Exception as exc:  # pragma: no cover - depends on clean-room install state
        rc = 1
        payload["passed"] = False
        payload["error_type"] = exc.__class__.__name__
        payload["error_message"] = str(exc)

    artifact_dir = Path(args.artifact_dir).resolve()
    artifact_path = _write_artifact(artifact_dir, payload)
    payload["artifact_path"] = _relative_to_root(artifact_path)
    artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(payload, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
