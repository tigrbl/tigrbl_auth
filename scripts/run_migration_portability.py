from __future__ import annotations

import argparse
import asyncio
import inspect
import json
import os
import subprocess
import sys
import traceback
from contextlib import asynccontextmanager
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.certification_evidence import current_environment_identity

REVISION_0007 = "0007_browser_session_cookie_and_auth_code_linkage"
SESSION_COLUMNS = {"session_state_salt", "cookie_secret_hash", "cookie_issued_at", "cookie_rotated_at"}
AUTH_CODE_COLUMNS = {"session_id"}
TOKEN_RECORD_COLUMNS = {"refresh_family_id", "refresh_parent_hash", "refresh_successor_hash", "used_at", "reuse_detected_at"}
SUPPORTED_BACKENDS = ("sqlite", "postgres")


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=_json_default) + "\n", encoding="utf-8")


async def _column_snapshot() -> dict[str, list[str]]:
    from tigrbl_auth.migrations import column_names_async

    return {
        "sessions": sorted(await column_names_async("sessions")),
        "auth_codes": sorted(await column_names_async("auth_codes")),
        "token_records": sorted(await column_names_async("token_records")),
        "users": sorted(await column_names_async("users")),
    }


async def _schema_snapshot() -> dict[str, Any]:
    from tigrbl_auth.migrations import verify_schema_async

    verification = await verify_schema_async()
    return asdict(verification)


def _revision_inventory() -> list[dict[str, Any]]:
    from tigrbl_auth.migrations import iter_migration_modules

    inventory: list[dict[str, Any]] = []
    for module in iter_migration_modules():
        inventory.append(
            {
                "revision": getattr(module, "revision", None),
                "down_revision": getattr(module, "down_revision", None),
                "module": getattr(module, "__name__", type(module).__name__),
                "doc": (getattr(module, "__doc__", "") or "").strip(),
            }
        )
    return inventory


async def _applied_revision_snapshot(revision_order: list[str]) -> list[str]:
    from tigrbl_auth_backend_app_core.surfaces import surface_api
    from tigrbl_auth.migrations.helpers import applied_revisions
    from tigrbl_auth.runtime.engine_resolver import resolve_api_provider

    provider = resolve_api_provider(surface_api)
    if provider is None:
        return []
    raw_engine, _ = provider.ensure()
    begin_ctx = raw_engine.begin()
    if hasattr(begin_ctx, "__aenter__"):
        async with begin_ctx as conn:
            applied = await conn.run_sync(lambda sync_conn: applied_revisions(sync_conn))
    else:
        with begin_ctx as conn:
            applied = applied_revisions(conn)
    return [revision for revision in revision_order if revision in set(applied)]


async def _exercise_backend(
    backend: str,
    database_url: str,
    artifact_dir: Path,
    *,
    revision_inventory: list[dict[str, Any]],
    revision_order: list[str],
    expected_head_revision: str | None,
    downgrade_target_revision: str | None,
) -> dict[str, Any]:
    from tigrbl.engine import Engine, EngineSpec
    from tigrbl_auth.app import app
    from tigrbl_auth_backend_app_core.surfaces import surface_api
    from tigrbl_auth.migrations import apply_all_async, downgrade_one_async
    from tigrbl_auth.runtime.engine_resolver import register_api_provider, resolve_api_provider

    backend_dir = artifact_dir / backend
    backend_dir.mkdir(parents=True, exist_ok=True)

    @asynccontextmanager
    async def runtime_context():
        spec = EngineSpec.from_any(database_url)
        engine = Engine(spec)
        provider = engine.provider
        original_surface = resolve_api_provider(surface_api)
        original_app = resolve_api_provider(app)
        register_api_provider(surface_api, provider)
        register_api_provider(app, provider)
        setattr(surface_api, "_ddl_executed", False)
        await surface_api.initialize()
        try:
            yield provider
        finally:
            raw_engine, _ = provider.ensure()
            if str(database_url).startswith("postgresql"):
                try:
                    cleanup_ctx = raw_engine.begin()
                    if hasattr(cleanup_ctx, "__aenter__"):
                        async with cleanup_ctx as conn:
                            await conn.exec_driver_sql("DROP SCHEMA IF EXISTS authn CASCADE")
                    else:
                        with cleanup_ctx as conn:
                            conn.exec_driver_sql("DROP SCHEMA IF EXISTS authn CASCADE")
                except Exception:
                    pass
            dispose_result = raw_engine.dispose()
            if inspect.isawaitable(dispose_result):
                await dispose_result
            register_api_provider(surface_api, original_surface or provider)
            register_api_provider(app, original_app or provider)
            setattr(surface_api, "_ddl_executed", False)

    result: dict[str, Any] = {
        "backend": backend,
        "available": True,
        "database_url": database_url if backend == "sqlite" else "postgresql://<redacted>",
        "passed": False,
        "upgrade_passed": False,
        "downgrade_passed": False,
        "reapply_passed": False,
        "revision_inventory": revision_inventory,
        "expected_head_revision": expected_head_revision,
        "downgrade_target_revision": downgrade_target_revision,
        "downgraded_revision": None,
        "head_revision_after_upgrade": None,
        "head_revision_after_downgrade": None,
        "head_revision_after_reapply": None,
        "upgrade_applied_revisions": [],
        "reapply_applied_revisions": [],
        "applied_revisions_after_downgrade": [],
        "upgrade_pending_before": [],
        "reapply_pending_before": [],
        "artifacts": {},
    }

    try:
        async with runtime_context():
            upgrade = await apply_all_async()
            upgrade_schema = await _schema_snapshot()
            upgrade_columns = await _column_snapshot()
            upgrade_applied = await _applied_revision_snapshot(revision_order)
            head_revision_after_upgrade = upgrade_applied[-1] if upgrade_applied else None
            upgrade_payload = {
                "result": asdict(upgrade),
                "schema": upgrade_schema,
                "columns": upgrade_columns,
                "revision_inventory": revision_inventory,
                "expected_head_revision": expected_head_revision,
                "applied_revisions": upgrade_applied,
                "head_revision_after_upgrade": head_revision_after_upgrade,
            }
            _write_json(backend_dir / "upgrade.json", upgrade_payload)
            result["artifacts"]["upgrade"] = str((backend_dir / "upgrade.json").relative_to(ROOT))
            result["upgrade_pending_before"] = list(upgrade.pending_before)
            result["upgrade_applied_revisions"] = upgrade_applied
            result["head_revision_after_upgrade"] = head_revision_after_upgrade
            result["upgrade_passed"] = bool(
                upgrade.passed
                and SESSION_COLUMNS <= set(upgrade_columns["sessions"])
                and AUTH_CODE_COLUMNS <= set(upgrade_columns["auth_codes"])
                and TOKEN_RECORD_COLUMNS <= set(upgrade_columns["token_records"])
                and bool(upgrade_schema.get("passed", False))
                and head_revision_after_upgrade == expected_head_revision
            )

            downgraded = await downgrade_one_async()
            downgrade_schema = await _schema_snapshot()
            downgrade_columns = await _column_snapshot()
            applied_after_downgrade = await _applied_revision_snapshot(revision_order)
            head_revision_after_downgrade = applied_after_downgrade[-1] if applied_after_downgrade else None
            downgrade_payload = {
                "downgraded_revision": downgraded,
                "schema": downgrade_schema,
                "columns": downgrade_columns,
                "revision_inventory": revision_inventory,
                "expected_head_revision": expected_head_revision,
                "downgrade_target_revision": downgrade_target_revision,
                "applied_revisions_after_downgrade": applied_after_downgrade,
                "head_revision_after_downgrade": head_revision_after_downgrade,
            }
            _write_json(backend_dir / "downgrade.json", downgrade_payload)
            result["artifacts"]["downgrade"] = str((backend_dir / "downgrade.json").relative_to(ROOT))
            result["downgraded_revision"] = downgraded
            result["applied_revisions_after_downgrade"] = applied_after_downgrade
            result["head_revision_after_downgrade"] = head_revision_after_downgrade
            downgrade_missing_tables = set(downgrade_schema.get("missing_tables", []))
            downgrade_unexpected_tables = set(downgrade_schema.get("unexpected_tables", []))
            downgrade_actual_tables = set(downgrade_schema.get("actual_tables", []))
            upgrade_actual_tables = set(upgrade_schema.get("actual_tables", []))
            removed_head_tables = upgrade_actual_tables - downgrade_actual_tables
            result["downgrade_passed"] = bool(
                downgraded == downgrade_target_revision
                and downgrade_missing_tables == removed_head_tables
                and not downgrade_unexpected_tables
                and removed_head_tables.isdisjoint(downgrade_actual_tables)
                and SESSION_COLUMNS <= set(downgrade_columns["sessions"])
                and AUTH_CODE_COLUMNS <= set(downgrade_columns["auth_codes"])
                and TOKEN_RECORD_COLUMNS <= set(downgrade_columns["token_records"])
                and head_revision_after_downgrade == downgrade_target_revision
            )

            reapply = await apply_all_async()
            reapply_schema = await _schema_snapshot()
            reapply_columns = await _column_snapshot()
            reapply_applied = await _applied_revision_snapshot(revision_order)
            head_revision_after_reapply = reapply_applied[-1] if reapply_applied else None
            reapply_payload = {
                "result": asdict(reapply),
                "schema": reapply_schema,
                "columns": reapply_columns,
                "revision_inventory": revision_inventory,
                "expected_head_revision": expected_head_revision,
                "applied_revisions": reapply_applied,
                "head_revision_after_reapply": head_revision_after_reapply,
            }
            _write_json(backend_dir / "reapply.json", reapply_payload)
            result["artifacts"]["reapply"] = str((backend_dir / "reapply.json").relative_to(ROOT))
            result["reapply_pending_before"] = list(reapply.pending_before)
            result["reapply_applied_revisions"] = reapply_applied
            result["head_revision_after_reapply"] = head_revision_after_reapply
            result["reapply_passed"] = bool(
                reapply.passed
                and SESSION_COLUMNS <= set(reapply_columns["sessions"])
                and AUTH_CODE_COLUMNS <= set(reapply_columns["auth_codes"])
                and TOKEN_RECORD_COLUMNS <= set(reapply_columns["token_records"])
                and bool(reapply_schema.get("passed", False))
                and head_revision_after_reapply == expected_head_revision
            )

            result["passed"] = bool(result["upgrade_passed"] and result["downgrade_passed"] and result["reapply_passed"])
            return result
    except Exception as exc:  # pragma: no cover - surfaced in artifact/report
        result.update(
            {
                "passed": False,
                "failure": str(exc),
                "traceback": traceback.format_exc(),
            }
        )
        _write_json(backend_dir / "failure.json", result)
        result["artifacts"]["failure"] = str((backend_dir / "failure.json").relative_to(ROOT))
        return result


def _default_pytest_report() -> Path:
    tox_env = os.environ.get("TOX_ENV_NAME", "").strip()
    stem = tox_env or f"migration-portability-py{sys.version_info.major}{sys.version_info.minor}"
    return ROOT / "dist" / "test-reports" / f"{stem}.json"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _pytest_summary(report: dict[str, Any]) -> dict[str, int]:
    summary = report.get("summary", {}) if isinstance(report, dict) else {}

    def _count(key: str) -> int:
        value = summary.get(key, 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    return {
        "tests_collected": max(_count("collected"), _count("total")),
        "tests_passed": _count("passed"),
        "tests_failed": _count("failed"),
        "tests_skipped": _count("skipped"),
        "tests_error": max(_count("error"), _count("errors")),
    }


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Migration Portability Report",
        "",
        f"- passed: `{report.get('passed', False)}`",
        f"- python_version: `{report.get('python_version')}`",
        f"- supported_backends: `{', '.join(report.get('supported_backends', []))}`",
        f"- validated_backends: `{', '.join(report.get('validated_backends', []))}`",
        f"- pytest_exit_code: `{report.get('pytest_exit_code')}`",
        f"- expected_head_revision: `{report.get('expected_head_revision')}`",
        f"- downgrade_target_revision: `{report.get('downgrade_target_revision')}`",
        f"- revision_inventory_count: `{len(report.get('revision_inventory', []))}`",
        "",
    ]
    for backend in report.get("supported_backends", []):
        payload = report.get("backend_results", {}).get(backend, {})
        lines.extend(
            [
                f"## {backend}",
                "",
                f"- available: `{payload.get('available', False)}`",
                f"- passed: `{payload.get('passed', False)}`",
                f"- upgrade_passed: `{payload.get('upgrade_passed', False)}`",
                f"- downgrade_passed: `{payload.get('downgrade_passed', False)}`",
                f"- reapply_passed: `{payload.get('reapply_passed', False)}`",
                f"- downgraded_revision: `{payload.get('downgraded_revision')}`",
                f"- head_revision_after_upgrade: `{payload.get('head_revision_after_upgrade')}`",
                f"- head_revision_after_downgrade: `{payload.get('head_revision_after_downgrade')}`",
                f"- head_revision_after_reapply: `{payload.get('head_revision_after_reapply')}`",
            ]
        )
        if payload.get("failure"):
            lines.append(f"- failure: `{payload.get('failure')}`")
        artifacts = payload.get("artifacts", {})
        if artifacts:
            lines.append("- artifacts:")
            for name, rel in sorted(artifacts.items()):
                lines.append(f"  - `{name}`: `{rel}`")
        lines.append("")
    failures = report.get("failures", [])
    if failures:
        lines.append("## open_gaps")
        lines.append("")
        for failure in failures:
            lines.append(f"- {failure}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run migration portability validation and preserve backend artifacts.")
    parser.add_argument("--artifact-dir", default=str(ROOT / "dist" / "migration-portability"))
    parser.add_argument("--report-json", default=str(ROOT / "docs" / "compliance" / "migration_portability_report.json"))
    parser.add_argument("--report-md", default=str(ROOT / "docs" / "compliance" / "migration_portability_report.md"))
    parser.add_argument("--pytest-report", default=None)
    parser.add_argument("--postgres-url", default=os.environ.get("POSTGRES_URL", ""))
    parser.add_argument("--skip-pytest", action="store_true")
    parser.add_argument("--strict-exit", action="store_true")
    args = parser.parse_args()

    artifact_dir = Path(args.artifact_dir).resolve()
    artifact_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(artifact_dir / "operator-state"))

    revision_inventory = _revision_inventory()
    revision_order = [str(item["revision"]) for item in revision_inventory if item.get("revision")]
    expected_head_revision = revision_order[-1] if revision_order else None
    downgrade_target_revision = revision_order[-2] if len(revision_order) >= 2 else None

    sqlite_dir = artifact_dir / "sqlite"
    sqlite_dir.mkdir(parents=True, exist_ok=True)
    sqlite_db = sqlite_dir / "tigrbl_auth_migration_portability.db"
    if sqlite_db.exists():
        sqlite_db.unlink()
    sqlite_result = asyncio.run(
        _exercise_backend(
            "sqlite",
            f"sqlite+aiosqlite:///{sqlite_db}",
            artifact_dir,
            revision_inventory=revision_inventory,
            revision_order=revision_order,
            expected_head_revision=expected_head_revision,
            downgrade_target_revision=downgrade_target_revision,
        )
    )

    backend_results: dict[str, Any] = {"sqlite": sqlite_result}
    postgres_url = str(args.postgres_url or "").strip()
    if postgres_url:
        backend_results["postgres"] = asyncio.run(
            _exercise_backend(
                "postgres",
                postgres_url,
                artifact_dir,
                revision_inventory=revision_inventory,
                revision_order=revision_order,
                expected_head_revision=expected_head_revision,
                downgrade_target_revision=downgrade_target_revision,
            )
        )
    else:
        backend_results["postgres"] = {
            "backend": "postgres",
            "available": False,
            "passed": False,
            "upgrade_passed": False,
            "downgrade_passed": False,
            "reapply_passed": False,
            "revision_inventory": revision_inventory,
            "expected_head_revision": expected_head_revision,
            "downgrade_target_revision": downgrade_target_revision,
            "downgraded_revision": None,
            "artifacts": {},
            "failure": "POSTGRES_URL not set in the current environment.",
        }

    pytest_report_path = Path(args.pytest_report).resolve() if args.pytest_report else _default_pytest_report()
    pytest_exit_code: int | None = None
    pytest_summary: dict[str, Any] = {}
    if not args.skip_pytest:
        pytest_report_path.parent.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        if postgres_url:
            env["POSTGRES_URL"] = postgres_url
        else:
            env.pop("POSTGRES_URL", None)
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "tests/integration/test_migration_upgrade_downgrade_safety.py",
            "--json-report",
            f"--json-report-file={pytest_report_path}",
        ]
        result = subprocess.run(cmd, cwd=str(ROOT), env=env, check=False)
        pytest_exit_code = int(result.returncode)
        pytest_summary = _pytest_summary(_read_json(pytest_report_path))

    validated_backends = [name for name, payload in backend_results.items() if payload.get("available")]
    passed_backends = [name for name, payload in backend_results.items() if payload.get("passed")]
    failures: list[str] = []
    for backend in SUPPORTED_BACKENDS:
        payload = backend_results[backend]
        if not payload.get("available"):
            failures.append(f"{backend} backend was not available in the current environment.")
        elif not payload.get("passed"):
            failures.append(f"{backend} backend did not pass upgrade → downgrade → reapply validation.")
    if pytest_exit_code not in {None, 0}:
        failures.append("The migration portability pytest lane did not pass.")

    report = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "environment_identity": current_environment_identity(install_profile="migration-portability", repo_root=ROOT),
        "supported_backends": list(SUPPORTED_BACKENDS),
        "required_backends": list(SUPPORTED_BACKENDS),
        "validated_backends": validated_backends,
        "passed_backends": passed_backends,
        "revision_inventory": revision_inventory,
        "head_revision": expected_head_revision,
        "expected_head_revision": expected_head_revision,
        "downgrade_target_revision": downgrade_target_revision,
        "backend_results": backend_results,
        "pytest_report_artifact": str(pytest_report_path.relative_to(ROOT)) if pytest_report_path.exists() else None,
        "pytest_exit_code": pytest_exit_code,
        "pytest_summary": pytest_summary,
        "passed": len(passed_backends) == len(SUPPORTED_BACKENDS) and pytest_exit_code in {None, 0},
        "failures": failures,
    }
    report_json = Path(args.report_json).resolve()
    report_md = Path(args.report_md).resolve()
    _write_json(report_json, report)
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text(_render_markdown(report), encoding="utf-8")
    _write_json(artifact_dir / "report.json", report)

    if args.strict_exit and not report["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
