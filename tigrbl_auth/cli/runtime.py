from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import signal
import subprocess
import sys

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib
from contextlib import suppress
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tigrbl_auth.api.app import build_app
from tigrbl_auth.cli.certification_evidence import (
    environment_identity_ready,
    install_evidence_ready,
    runtime_surface_probe_ready,
    validated_runtime_manifest_passed,
)
from tigrbl_auth.repo_truth import workflow_role_text
from tigrbl_auth.runtime import build_runtime_hash_matrix, build_runtime_plan, get_runner_adapter, iter_runner_adapters
from tigrbl_auth.runtime.types import ApplicationProbeResult, CommandProbeResult, HttpEndpointProbeResult

FORBIDDEN_IMPORT_PATTERNS = [
    re.compile(r"^\s*from\s+fastapi\b", re.MULTILINE),
    re.compile(r"^\s*import\s+fastapi\b", re.MULTILINE),
    re.compile(r"^\s*from\s+starlette\b", re.MULTILINE),
    re.compile(r"^\s*import\s+starlette\b", re.MULTILINE),
]
FORBIDDEN_RUNTIME_IMPORT_PATTERNS = [
    re.compile(r"^\s*from\s+tigrbl_core\b", re.MULTILINE),
    re.compile(r"^\s*import\s+tigrbl_core\b", re.MULTILINE),
    re.compile(r"^\s*from\s+tigrbl\._", re.MULTILINE),
    re.compile(r"^\s*import\s+tigrbl\._", re.MULTILINE),
    re.compile(r"^\s*from\s+tigrbl\.security\.dependencies\b", re.MULTILINE),
    re.compile(
        r"^\s*from\s+tigrbl\.types\s+import\s+.*\b(HTTPException|Request|Response|Depends|Security)\b",
        re.MULTILINE,
    ),
]
FORBIDDEN_FALLBACK_PATTERNS = [
    re.compile(r"pragma:\s*no\s*cover\s*-\s*import-safety fallback"),
    re.compile(r"^\s*if\s+hasattr\(", re.MULTILINE),
    re.compile(r"^\s*except\s+Exception:\s*$", re.MULTILINE),
]
FORBIDDEN_DEPENDENCY_NAMES = {"fastapi", "starlette"}
RUNNER_CERTIFICATION_MATRIX = {
    "uvicorn": {
        "profile_name": "sqlite-uvicorn",
        "supported_python_versions": ["3.10", "3.11", "3.12"],
        "constraints": ["constraints/base.txt", "constraints/runner-uvicorn.txt"],
        "ci_install_job": "sqlite-uvicorn",
        "required_extra": "uvicorn",
        "required_release_probe": "--runner uvicorn",
    },
    "hypercorn": {
        "profile_name": "postgres-hypercorn",
        "supported_python_versions": ["3.10", "3.11", "3.12"],
        "constraints": ["constraints/base.txt", "constraints/runner-hypercorn.txt"],
        "ci_install_job": "postgres-hypercorn",
        "required_extra": "hypercorn",
        "required_release_probe": "--runner hypercorn",
    },
    "tigrcorn": {
        "profile_name": "tigrcorn",
        "supported_python_versions": ["3.11", "3.12"],
        "constraints": ["constraints/base.txt", "constraints/runner-tigrcorn.txt"],
        "ci_install_job": "tigrcorn",
        "required_extra": "tigrcorn",
        "required_release_probe": "--runner tigrcorn",
    },
}

RUNTIME_VALIDATION_GROUPS = {
    "base": {"supported_python_versions": ["3.10", "3.11", "3.12"]},
    "sqlite-uvicorn": {"supported_python_versions": ["3.10", "3.11", "3.12"]},
    "postgres-hypercorn": {"supported_python_versions": ["3.10", "3.11", "3.12"]},
    "tigrcorn": {"supported_python_versions": ["3.11", "3.12"]},
    "devtest": {"supported_python_versions": ["3.10", "3.11", "3.12"]},
}


_RUNTIME_HTTP_SURFACE_TARGETS = (
    {"name": "openid-configuration", "path": "/.well-known/openid-configuration"},
    {"name": "oauth-authorization-server", "path": "/.well-known/oauth-authorization-server"},
    {"name": "oauth-protected-resource", "path": "/.well-known/oauth-protected-resource"},
    {"name": "jwks", "path": "/.well-known/jwks.json"},
    {"name": "public-contract", "path": "/openapi.json"},
)


def _deployment_from_app_state(app: Any) -> Any | None:
    state = getattr(app, "state", None)
    if state is None:
        return None
    return getattr(state, "tigrbl_auth_deployment", None)


def _surface_probe_targets(*, app: Any, deployment: Any | None = None) -> tuple[dict[str, str], ...]:
    active_deployment = deployment or _deployment_from_app_state(app)
    if active_deployment is None or not hasattr(active_deployment, "active_routes"):
        return _RUNTIME_HTTP_SURFACE_TARGETS

    active_routes = set(getattr(active_deployment, "active_routes", ()) or ())
    surface_enabled = getattr(active_deployment, "surface_enabled", None)
    public_surface_enabled = bool(surface_enabled("public-rest")) if callable(surface_enabled) else True

    filtered_targets: list[dict[str, str]] = []
    for item in _RUNTIME_HTTP_SURFACE_TARGETS:
        path = str(item["path"])
        if path == "/openapi.json":
            if public_surface_enabled:
                filtered_targets.append(item)
            continue
        if path in active_routes:
            filtered_targets.append(item)
    return tuple(filtered_targets) or _RUNTIME_HTTP_SURFACE_TARGETS


RUNTIME_FALLBACK_PATHS = [
    "tigrbl_auth/framework.py",
    "tigrbl_auth/plugin.py",
    "tigrbl_auth/api/app.py",
    "tigrbl_auth/api/lifecycle.py",
    "tigrbl_auth/app.py",
    "tigrbl_auth/gateway.py",
]


def _scan_patterns(
    base: Path,
    patterns: list[re.Pattern[str]],
    *,
    rel_root: Path,
) -> list[dict[str, str | int]]:
    hits: list[dict[str, str | int]] = []
    if not base.exists():
        return hits
    paths = [base] if base.is_file() else list(base.rglob("*.py"))
    for path in paths:
        if path.is_dir():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                hits.append(
                    {
                        "path": str(path.relative_to(rel_root)),
                        "line": line,
                        "match": match.group(0).strip(),
                    }
                )
    return hits



def _load_pyproject_runtime_manifest(repo_root: Path) -> dict[str, Any]:
    pyproject_path = repo_root / "pyproject.toml"
    if not pyproject_path.exists():
        return {}
    return tomllib.loads(pyproject_path.read_text(encoding="utf-8"))



def _build_runner_support_manifest(repo_root: Path) -> dict[str, Any]:
    pyproject = _load_pyproject_runtime_manifest(repo_root)
    project = pyproject.get("project", {}) if isinstance(pyproject, dict) else {}
    optional_dependencies = project.get("optional-dependencies", {}) or {}
    requires_python = str(project.get("requires-python", "unspecified"))
    tox_text = (repo_root / "tox.ini").read_text(encoding="utf-8") if (repo_root / "tox.ini").exists() else ""
    install_workflow_text = workflow_role_text(repo_root, "install-matrix")
    release_workflow_text = workflow_role_text(repo_root, "release-gates")

    profiles: dict[str, Any] = {}
    for runner, config in RUNNER_CERTIFICATION_MATRIX.items():
        supported_python_versions = list(config["supported_python_versions"])
        expected_tox_envs = [f"py{version.replace('.', '')}-{config['profile_name']}" for version in supported_python_versions]
        extra_values = list(optional_dependencies.get(config["required_extra"], []) or [])
        servers_extra_values = list(optional_dependencies.get("servers", []) or [])
        constraint_files = list(config["constraints"])
        constraints_present = [item for item in constraint_files if (repo_root / item).exists()]
        tox_envs_present = [env for env in expected_tox_envs if env in tox_text]
        release_probe_present = config["required_release_probe"] in tox_text or config["required_release_probe"] in release_workflow_text
        ci_install_job_present = config["ci_install_job"] in install_workflow_text
        placeholder_supported = len(extra_values) == 0
        aggregate_runner_extra_present = any(runner in value for value in servers_extra_values)
        profiles[runner] = {
            "required_extra": config["required_extra"],
            "profile_name": config["profile_name"],
            "supported_python_versions": supported_python_versions,
            "pyproject_extra_present": not placeholder_supported,
            "pyproject_extra_values": extra_values,
            "aggregate_runner_extra_present": aggregate_runner_extra_present,
            "constraints": constraint_files,
            "constraints_present": constraints_present,
            "tox_envs": expected_tox_envs,
            "tox_envs_present": tox_envs_present,
            "ci_install_job": config["ci_install_job"],
            "ci_install_job_present": ci_install_job_present,
            "ci_release_gate_probe_present": release_probe_present,
            "placeholder_supported": placeholder_supported,
            "declared_installable_from_repository": (not placeholder_supported)
            and len(constraints_present) == len(constraint_files)
            and len(tox_envs_present) == len(expected_tox_envs)
            and ci_install_job_present
            and release_probe_present,
        }
    return {
        "requires_python": requires_python,
        "supported_python_versions": ["3.10", "3.11", "3.12"],
        "profiles": profiles,
    }


def _scan_pyproject_forbidden_dependencies(pyproject_path: Path) -> list[str]:
    if not pyproject_path.exists():
        return []
    text = pyproject_path.read_text(encoding="utf-8").lower()
    hits: list[str] = []
    for dep in sorted(FORBIDDEN_DEPENDENCY_NAMES):
        if f'"{dep}' in text or f"'{dep}" in text:
            hits.append(dep)
    return hits



def _read_json_if_exists(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}



def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None



def _runtime_manifest_counts_as_passed(payload: dict[str, Any]) -> bool:
    return validated_runtime_manifest_passed(payload)



def _runtime_manifest_failure_reasons(payload: dict[str, Any]) -> list[str]:
    if not payload:
        return ["manifest is missing"]
    reasons: list[str] = []
    if not environment_identity_ready(payload):
        reasons.append("environment identity is missing or does not match the manifest python version")
    if not install_evidence_ready(payload):
        reasons.append("install substrate evidence is missing or incomplete")
    if not payload.get("runtime_smoke_passed", False):
        reasons.append("runtime smoke did not pass")
    if not payload.get("application_probe_passed", False):
        reasons.append("application-factory probe did not pass")
    if not runtime_surface_probe_ready(payload):
        reasons.append("HTTP surface probe evidence is missing or failed")
    runner = str(payload.get("runner") or "").strip()
    if runner and not payload.get("runner_available", False):
        reasons.append(f"runner package '{runner}' was not available in the validated environment")
    if runner and not payload.get("serve_check_passed", False):
        reasons.append("serve-check evidence is missing or failed")
    if not payload.get("passed", False):
        reasons.append("manifest pass bit is false")
    return reasons or ["manifest did not satisfy the certification runtime criteria"]



def _validated_artifact_inventory_present(repo_root: Path) -> bool:
    validated_root = repo_root / "dist" / "validated-runs"
    if not validated_root.exists():
        return False
    if (validated_root / "collected-artifact-downloads.json").exists():
        return True
    recognized_kinds = {"runtime-profile", "test-lane", "migration-portability", "tier3-evidence"}
    for path in sorted(validated_root.glob("*.json")):
        payload = _read_json_if_exists(path)
        if str(payload.get("kind", "")) in recognized_kinds:
            return True
    return False



def _runtime_report_mode(repo_root: Path, report_mode: str | None) -> str:
    requested = (report_mode or os.environ.get("TIGRBL_AUTH_RUNTIME_REPORT_MODE", "auto")).strip().lower() or "auto"
    if requested in {"validated-runs", "live-probe"}:
        return requested
    return "validated-runs" if _validated_artifact_inventory_present(repo_root) else "live-probe"



def _validated_runtime_manifest_map(repo_root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    manifests: dict[tuple[str, str], dict[str, Any]] = {}
    validated_root = repo_root / "dist" / "validated-runs"
    if not validated_root.exists():
        return manifests
    for path in sorted(validated_root.glob("*.json")):
        payload = _read_json_if_exists(path)
        if payload.get("kind") != "runtime-profile":
            continue
        profile = str(payload.get("matrix_profile", "unknown"))
        python_version = str(payload.get("python_version", ""))
        if not profile or not python_version:
            continue
        payload["_path"] = str(path.relative_to(repo_root))
        manifests[(profile, python_version)] = payload
    return manifests



def _matrix_identities(profile: str, versions: list[str]) -> list[str]:
    return [f"{profile}@py{version}" for version in versions]



def _runtime_summary_from_manifests(manifests: list[dict[str, Any]]) -> dict[str, int]:
    endpoint_count = 0
    passed_count = 0
    failed_count = 0
    for manifest in manifests:
        endpoint_count = max(
            endpoint_count,
            _coerce_int(manifest.get("surface_probe_endpoint_count"))
            or _coerce_int((manifest.get("surface_probe") or {}).get("endpoint_count"))
            or 0,
        )
        passed_count = max(
            passed_count,
            _coerce_int(manifest.get("surface_probe_passed_count"))
            or _coerce_int((manifest.get("surface_probe") or {}).get("passed_count"))
            or 0,
        )
        failed_count = max(
            failed_count,
            _coerce_int(manifest.get("surface_probe_failed_count"))
            or _coerce_int((manifest.get("surface_probe") or {}).get("failed_count"))
            or 0,
        )
    return {
        "endpoint_count": endpoint_count,
        "passed_count": passed_count,
        "failed_count": failed_count,
    }



def build_validated_runner_profile_report(repo_root: Path, *, deployment: Any) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    support_manifest = _build_runner_support_manifest(repo_root)
    manifests_by_key = _validated_runtime_manifest_map(repo_root)
    all_expected_keys = [
        (profile, version)
        for profile, cfg in RUNTIME_VALIDATION_GROUPS.items()
        for version in cfg["supported_python_versions"]
    ]
    base_versions = list(RUNTIME_VALIDATION_GROUPS["base"]["supported_python_versions"])
    base_expected = [("base", version) for version in base_versions]
    base_manifests = [manifests_by_key[key] for key in base_expected if key in manifests_by_key]
    base_missing = [f"base@py{version}" for version in base_versions if ("base", version) not in manifests_by_key]
    base_failed = [
        f"base@py{version}"
        for version in base_versions
        if ("base", version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[("base", version)])
    ]
    application_probe_passed = bool(base_manifests) and not base_missing and not base_failed and all(bool(item.get("application_probe_passed", False)) for item in base_manifests)
    surface_probe_passed = bool(base_manifests) and not base_missing and not base_failed and all(runtime_surface_probe_ready(item) for item in base_manifests)
    surface_summary = _runtime_summary_from_manifests(base_manifests)
    application_message = (
        f"Validated runtime manifests confirm application-factory materialization for {len(base_manifests)}/{len(base_expected)} base environments."
        if application_probe_passed
        else (
            "Validated runtime manifests are missing or failing for the base application-factory environments: "
            + ", ".join(base_missing + base_failed)
            if (base_missing or base_failed)
            else "Validated runtime manifests do not yet prove base application-factory materialization."
        )
    )
    surface_message = (
        f"Validated runtime manifests confirm surface probes for {len(base_manifests)}/{len(base_expected)} base environments."
        if surface_probe_passed
        else (
            "Validated runtime manifests are missing or failing for the base surface-probe environments: "
            + ", ".join(base_missing + base_failed)
            if (base_missing or base_failed)
            else "Validated runtime manifests do not yet prove surface probes for the base environments."
        )
    )

    ready_count = 0
    missing_count = 0
    invalid_count = 0
    profiles: list[dict[str, Any]] = []
    application_hashes = {str(item.get("application_hash")) for item in manifests_by_key.values() if item.get("application_hash")}
    for adapter in iter_runner_adapters():
        support = dict((support_manifest.get("profiles") or {}).get(adapter.name, {}))
        matrix_profile = str(support.get("profile_name") or RUNNER_CERTIFICATION_MATRIX[adapter.name]["profile_name"])
        versions = list(RUNTIME_VALIDATION_GROUPS[matrix_profile]["supported_python_versions"])
        expected_keys = [(matrix_profile, version) for version in versions]
        expected_ids = _matrix_identities(matrix_profile, versions)
        present_ids = [f"{profile}@py{version}" for profile, version in expected_keys if (profile, version) in manifests_by_key]
        passed_ids = [
            f"{profile}@py{version}"
            for profile, version in expected_keys
            if _runtime_manifest_counts_as_passed(manifests_by_key.get((profile, version), {}))
        ]
        failed_ids = [
            f"{profile}@py{version}"
            for profile, version in expected_keys
            if (profile, version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[(profile, version)])
        ]
        missing_ids = [identity for identity in expected_ids if identity not in present_ids]
        present_manifests = [manifests_by_key[key] for key in expected_keys if key in manifests_by_key]
        installed = bool(present_manifests) and not missing_ids and all(bool(item.get("runner_available", False)) for item in present_manifests)
        serve_check_passed = bool(present_manifests) and not missing_ids and all(bool(item.get("serve_check_passed", False)) for item in present_manifests)
        if len(present_manifests) == 0:
            status = "missing"
            missing_count += 1
        elif not missing_ids and not failed_ids:
            status = "ready"
            ready_count += 1
        else:
            status = "invalid"
            invalid_count += 1
        diagnostics: list[dict[str, Any]] = []
        if missing_ids:
            diagnostics.append({
                "level": "warning",
                "code": "validated-manifest-missing",
                "message": "Validated runtime manifests are missing for one or more required matrix cells.",
                "identities": missing_ids,
            })
        if failed_ids:
            diagnostics.append({
                "level": "error",
                "code": "validated-execution-failed",
                "message": "One or more preserved runtime manifests did not satisfy the certification runtime criteria.",
                "identities": failed_ids,
                "reasons": {
                    f"{profile}@py{version}": _runtime_manifest_failure_reasons(manifests_by_key[(profile, version)])
                    for profile, version in expected_keys
                    if (profile, version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[(profile, version)])
                },
            })
        application_hash = None
        runtime_hash = None
        if present_manifests:
            app_hashes = {str(item.get("application_hash")) for item in present_manifests if item.get("application_hash")}
            run_hashes = {str(item.get("runtime_hash")) for item in present_manifests if item.get("runtime_hash")}
            if len(app_hashes) == 1:
                application_hash = next(iter(app_hashes))
            if len(run_hashes) == 1:
                runtime_hash = next(iter(run_hashes))
        serve_check_message = (
            f"Validated manifests confirm serve-check success for {len(passed_ids)}/{len(expected_ids)} required cells."
            if serve_check_passed
            else (
                "Validated runtime manifests are missing or failing serve-check evidence for required cells: "
                + ", ".join(missing_ids + failed_ids)
                if (missing_ids or failed_ids)
                else "Validated runtime manifests do not yet prove serve-check success for this runner."
            )
        )
        profiles.append(
            {
                "name": adapter.name,
                "display_name": adapter.display_name,
                "status": status,
                "installed": installed,
                "available_module": adapter.available_module_name(),
                "capabilities": [item.to_manifest() for item in adapter.capabilities],
                "flag_metadata": [item.to_manifest() for item in adapter.flag_metadata],
                "diagnostics": diagnostics,
                "application_hash": application_hash,
                "runtime_hash": runtime_hash,
                "serve_check": {
                    "executed": bool(present_manifests),
                    "passed": serve_check_passed,
                    "command": f"tigrbl-auth serve --check --server {adapter.name} --format json",
                    "message": serve_check_message,
                    "exit_code": 0 if serve_check_passed else None,
                },
                "validated_matrix": {
                    "matrix_profile": matrix_profile,
                    "expected_identities": expected_ids,
                    "present_identities": present_ids,
                    "passed_identities": passed_ids,
                    "missing_identities": missing_ids,
                    "failed_identities": failed_ids,
                    "identity_ready_count": sum(1 for item in present_manifests if environment_identity_ready(item)),
                    "install_evidence_ready_count": sum(1 for item in present_manifests if install_evidence_ready(item)),
                    "failure_reasons": {
                        f"{profile}@py{version}": _runtime_manifest_failure_reasons(manifests_by_key[(profile, version)])
                        for profile, version in expected_keys
                        if (profile, version) in manifests_by_key and not _runtime_manifest_counts_as_passed(manifests_by_key[(profile, version)])
                    },
                },
                **support,
            }
        )

    placeholder_supported_runner_names = [item["name"] for item in profiles if item.get("placeholder_supported")]
    declared_ci_installable_runner_names = [item["name"] for item in profiles if item.get("declared_installable_from_repository")]
    runtime_present_count = sum(1 for key in all_expected_keys if key in manifests_by_key)
    runtime_passed_count = sum(1 for key in all_expected_keys if _runtime_manifest_counts_as_passed(manifests_by_key.get(key, {})))
    validated_source = repo_root / "dist" / "validated-runs" / "collected-artifact-downloads.json"
    return {
        "generated_at": _utc_timestamp(),
        "deployment_profile": getattr(deployment, "profile", "baseline"),
        "report_mode": "validated-runs",
        "validated_artifact_source": str(validated_source.relative_to(repo_root)) if validated_source.exists() else None,
        "application_probe": {
            "passed": application_probe_passed,
            "app_factory": "tigrbl_auth.api.app.build_app",
            "message": application_message,
            "error_type": None if application_probe_passed else "ValidatedRuntimeEvidenceMissing",
        },
        "surface_probe": {
            "executed": bool(base_manifests),
            "passed": surface_probe_passed,
            "message": surface_message,
            "endpoint_count": surface_summary["endpoint_count"],
            "passed_count": surface_summary["passed_count"],
            "failed_count": surface_summary["failed_count"],
            "probes": [],
        },
        "summary": {
            "runner_count": len(profiles),
            "ready_count": ready_count,
            "missing_count": missing_count,
            "invalid_count": invalid_count,
            "application_hash_invariant": len(application_hashes) == 1 if application_hashes else False,
            "pyproject_requires_python": support_manifest.get("requires_python"),
            "supported_python_versions": support_manifest.get("supported_python_versions", []),
            "placeholder_supported_runner_count": len(placeholder_supported_runner_names),
            "placeholder_supported_runner_names": placeholder_supported_runner_names,
            "declared_ci_installable_runner_count": len(declared_ci_installable_runner_names),
            "declared_ci_installable_runner_names": declared_ci_installable_runner_names,
            "declared_ci_install_probe_complete": len(declared_ci_installable_runner_names) == len(profiles),
            "execution_probes_enabled": True,
            "surface_probe_passed": surface_probe_passed,
            "surface_probe_endpoint_count": surface_summary["endpoint_count"],
            "surface_probe_passed_count": surface_summary["passed_count"],
            "surface_probe_failed_count": surface_summary["failed_count"],
            "serve_check_passed_count": sum(1 for item in profiles if item.get("serve_check", {}).get("passed")),
            "execution_probe_complete": runtime_present_count == len(all_expected_keys) and runtime_passed_count == len(all_expected_keys),
            "source_mode": "validated-runs",
            "required_runtime_cell_count": len(all_expected_keys),
            "validated_runtime_cell_count": runtime_present_count,
            "validated_runtime_cell_passed_count": runtime_passed_count,
            "validated_runtime_matrix_green": runtime_passed_count == len(all_expected_keys),
            "validated_runtime_identity_ready_count": sum(1 for item in manifests_by_key.values() if environment_identity_ready(item)),
            "validated_runtime_install_evidence_ready_count": sum(1 for item in manifests_by_key.values() if install_evidence_ready(item)),
            "validated_download_collection_present": validated_source.exists(),
        },
        "profiles": profiles,
    }


def run_runtime_foundation_check(
    repo_root: Path,
    *,
    strict: bool = True,
    report_dir: Path | None = None,
) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)

    runtime_pkg = repo_root / "tigrbl_auth"
    tests_dir = repo_root / "tests"
    scripts_dir = repo_root / "scripts"
    pyproject_path = repo_root / "pyproject.toml"

    import_hits = {
        "runtime_package": _scan_patterns(
            runtime_pkg, FORBIDDEN_IMPORT_PATTERNS, rel_root=repo_root
        ),
        "tests": _scan_patterns(
            tests_dir, FORBIDDEN_IMPORT_PATTERNS, rel_root=repo_root
        ),
        "scripts": _scan_patterns(
            scripts_dir, FORBIDDEN_IMPORT_PATTERNS, rel_root=repo_root
        ),
    }
    runtime_private_hits = _scan_patterns(
        runtime_pkg, FORBIDDEN_RUNTIME_IMPORT_PATTERNS, rel_root=repo_root
    )

    fallback_hits: list[dict[str, str | int]] = []
    for rel in RUNTIME_FALLBACK_PATHS:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_FALLBACK_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                fallback_hits.append(
                    {
                        "path": str(path.relative_to(repo_root)),
                        "line": line,
                        "match": match.group(0).strip(),
                    }
                )

    dependency_hits = _scan_pyproject_forbidden_dependencies(pyproject_path)

    failures: list[str] = []
    if any(import_hits.values()):
        failures.append("FastAPI/Starlette imports remain in runtime, tests, or scripts.")
    if runtime_private_hits:
        failures.append(
            "Non-public Tigrbl imports remain in the active runtime package."
        )
    if dependency_hits:
        failures.append(
            "Forbidden FastAPI/Starlette dependencies remain in packaging metadata."
        )
    if fallback_hits:
        failures.append("Release-path framework fallbacks remain in active runtime files.")

    report: dict[str, Any] = {
        "scope": "phase-1-tigrbl-runtime-foundation",
        "strict": strict,
        "passed": not failures,
        "summary": {
            "runtime_fastapi_starlette_hits": len(import_hits["runtime_package"]),
            "tests_fastapi_starlette_hits": len(import_hits["tests"]),
            "scripts_fastapi_starlette_hits": len(import_hits["scripts"]),
            "runtime_non_public_tigrbl_hits": len(runtime_private_hits),
            "pyproject_forbidden_dependency_hits": len(dependency_hits),
            "release_path_fallback_hits": len(fallback_hits),
        },
        "hits": {
            "fastapi_starlette": import_hits,
            "runtime_non_public_tigrbl": runtime_private_hits,
            "pyproject_forbidden_dependencies": dependency_hits,
            "release_path_fallbacks": fallback_hits,
        },
        "failures": failures,
    }

    json_path = report_dir / "tigrbl_runtime_foundation_report.json"
    md_path = report_dir / "tigrbl_runtime_foundation_report.md"
    nofs_json = report_dir / "no_fastapi_starlette_report.json"
    nofs_md = report_dir / "no_fastapi_starlette_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Tigrbl Runtime Foundation Report",
        "",
        f"- Scope: `{report['scope']}`",
        f"- Strict: `{strict}`",
        f"- Passed: `{report['passed']}`",
        f"- Runtime FastAPI/Starlette hits: `{report['summary']['runtime_fastapi_starlette_hits']}`",
        f"- Test FastAPI/Starlette hits: `{report['summary']['tests_fastapi_starlette_hits']}`",
        f"- Script FastAPI/Starlette hits: `{report['summary']['scripts_fastapi_starlette_hits']}`",
        f"- Runtime non-public Tigrbl hits: `{report['summary']['runtime_non_public_tigrbl_hits']}`",
        f"- Pyproject forbidden dependency hits: `{report['summary']['pyproject_forbidden_dependency_hits']}`",
        f"- Release-path fallback hits: `{report['summary']['release_path_fallback_hits']}`",
        "",
    ]
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in failures])
        lines.append("")
    else:
        lines.extend(
            [
                "## Result",
                "",
                "The active runtime package is Tigrbl-only, release-path framework fallbacks were not detected, and no direct FastAPI/Starlette imports or metadata dependencies were found in runtime, tests, scripts, or packaging metadata.",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    nofs_report = {
        "scope": "runtime package, tests, scripts, and packaging metadata",
        "root": {
            "runtime": str(runtime_pkg.relative_to(repo_root)),
            "tests": str(tests_dir.relative_to(repo_root)),
            "scripts": str(scripts_dir.relative_to(repo_root)),
            "metadata": str(pyproject_path.relative_to(repo_root)),
        },
        "direct_fastapi_starlette_imports_found": sum(
            len(v) for v in import_hits.values()
        ),
        "pyproject_forbidden_dependencies_found": dependency_hits,
        "hits": import_hits,
    }
    nofs_json.write_text(json.dumps(nofs_report, indent=2) + "\n", encoding="utf-8")
    nofs_lines = [
        "# No FastAPI / Starlette Import and Metadata Report",
        "",
        f"- Scope: `{nofs_report['scope']}`",
        f"- Runtime root: `{nofs_report['root']['runtime']}`",
        f"- Tests root: `{nofs_report['root']['tests']}`",
        f"- Scripts root: `{nofs_report['root']['scripts']}`",
        f"- Metadata file: `{nofs_report['root']['metadata']}`",
        f"- Direct import hits: `{nofs_report['direct_fastapi_starlette_imports_found']}`",
        f"- Forbidden metadata dependencies: `{len(dependency_hits)}`",
        "",
    ]
    if nofs_report["direct_fastapi_starlette_imports_found"] or dependency_hits:
        nofs_lines.extend(["## Findings", ""])
        for scope_name, scope_hits in import_hits.items():
            for hit in scope_hits:
                nofs_lines.append(
                    f"- `{scope_name}` → `{hit['path']}:{hit['line']}` — `{hit['match']}`"
                )
        for dep in dependency_hits:
            nofs_lines.append(
                f"- `pyproject.toml` declares forbidden dependency `{dep}`"
            )
        nofs_lines.append("")
    else:
        nofs_lines.extend(
            [
                "## Result",
                "",
                "No direct `fastapi` or `starlette` imports were found in the runtime package, tests, or scripts, and no forbidden `fastapi` or `starlette` dependencies were found in `pyproject.toml`.",
                "",
            ]
        )
    nofs_md.write_text("\n".join(nofs_lines), encoding="utf-8")

    return 1 if failures and strict else 0



def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _error_manifest(exc: BaseException) -> dict[str, str]:
    return {"type": exc.__class__.__name__, "message": str(exc)}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _trim_probe_output(value: str | None, *, limit: int = 1000) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1] + "…"


def _extract_json_payload(text: str | None) -> dict[str, Any] | None:
    if not text:
        return None
    cleaned = text.strip()
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            return None


def _surface_probe_skipped(message: str) -> dict[str, Any]:
    return {
        "executed": False,
        "passed": False,
        "message": message,
        "endpoint_count": 0,
        "passed_count": 0,
        "failed_count": 0,
        "probes": [],
    }


def _command_probe_skipped(command: str, message: str) -> dict[str, Any]:
    return {
        "passed": False,
        "executed": False,
        "command": command,
        "message": message,
    }


def _validate_surface_response(name: str, path: str, status_code: int, payload: Any) -> tuple[bool, str]:
    if status_code != 200:
        return False, f"Expected HTTP 200 from `{path}`, received `{status_code}`."
    if name == "openid-configuration":
        if not isinstance(payload, dict):
            return False, "OpenID configuration response is not a JSON object."
        if not payload.get("issuer") or not payload.get("jwks_uri"):
            return False, "OpenID configuration is missing `issuer` or `jwks_uri`."
        return True, "OpenID discovery document is available."
    if name == "oauth-authorization-server":
        if not isinstance(payload, dict):
            return False, "Authorization-server metadata response is not a JSON object."
        if not payload.get("issuer") or not payload.get("jwks_uri"):
            return False, "Authorization-server metadata is missing `issuer` or `jwks_uri`."
        return True, "OAuth authorization-server metadata is available."
    if name == "oauth-protected-resource":
        if not isinstance(payload, dict):
            return False, "Protected-resource metadata response is not a JSON object."
        if not payload.get("authorization_servers") and not payload.get("resource") and not payload.get("jwks_uri"):
            return False, "Protected-resource metadata is missing expected identifying fields."
        return True, "OAuth protected-resource metadata is available."
    if name == "jwks":
        keys = payload.get("keys") if isinstance(payload, dict) else None
        if not isinstance(keys, list):
            return False, "JWKS response does not contain a `keys` array."
        return True, "JWKS document is available."
    if name == "public-contract":
        if not isinstance(payload, dict):
            return False, "OpenAPI response is not a JSON object."
        if not payload.get("openapi"):
            return False, "OpenAPI document is missing the `openapi` version field."
        paths = payload.get("paths") if isinstance(payload.get("paths"), dict) else {}
        required_paths = {"/.well-known/openid-configuration", "/.well-known/jwks.json"}
        if not required_paths.issubset(set(paths)):
            return False, "OpenAPI document is missing the public discovery/JWKS routes."
        return True, "Public contract endpoint is available."
    return True, f"Probe for `{path}` succeeded."


async def _probe_http_surface_endpoints_async(app: Any, deployment: Any | None = None) -> dict[str, Any]:
    try:
        from httpx import ASGITransport, AsyncClient
    except Exception as exc:  # pragma: no cover - optional import safety
        return _surface_probe_skipped(f"HTTP probe transport unavailable: {exc}")

    probes: list[dict[str, Any]] = []
    targets = _surface_probe_targets(app=app, deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://runtime-probe") as client:
        for item in targets:
            name = str(item["name"])
            path = str(item["path"])
            try:
                response = await client.get(path)
                try:
                    payload = response.json()
                except ValueError:
                    payload = None
                passed, message = _validate_surface_response(name, path, int(response.status_code), payload)
                probes.append(
                    HttpEndpointProbeResult(
                        name=name,
                        path=path,
                        passed=passed,
                        message=message,
                        status_code=int(response.status_code),
                    ).to_manifest()
                )
            except Exception as exc:  # pragma: no cover - depends on runtime stack availability
                probes.append(
                    HttpEndpointProbeResult(
                        name=name,
                        path=path,
                        passed=False,
                        message=str(exc),
                        status_code=None,
                        error_type=exc.__class__.__name__,
                    ).to_manifest()
                )
    passed_count = sum(1 for item in probes if item.get("passed"))
    failed_count = len(probes) - passed_count
    return {
        "executed": True,
        "passed": failed_count == 0,
        "message": "Runtime HTTP surface probes completed successfully." if failed_count == 0 else "One or more runtime HTTP surface probes failed.",
        "endpoint_count": len(probes),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "probes": probes,
    }


def probe_http_surface_endpoints(*, app: Any, deployment: Any | None = None) -> dict[str, Any]:
    return asyncio.run(_probe_http_surface_endpoints_async(app, deployment=deployment))


def probe_runner_serve_check(
    repo_root: Path,
    runner: str,
    *,
    timeout_seconds: int = 120,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    display_command = f"tigrbl-auth serve --repo-root {repo_root} --server {runner} --format json --check"
    script = shutil.which("tigrbl-auth")
    if script:
        argv = [script, "serve", "--repo-root", str(repo_root), "--server", runner, "--format", "json", "--check"]
    else:
        argv = [sys.executable, "-m", "tigrbl_auth.cli.main", "serve", "--repo-root", str(repo_root), "--server", runner, "--format", "json", "--check"]
    env = os.environ.copy()
    env["TIGRBL_AUTH_SKIP_EXECUTION_PROBES"] = "1"
    try:
        result = subprocess.run(
            argv,
            cwd=repo_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - subprocess environment dependent
        return CommandProbeResult(
            passed=False,
            executed=True,
            command=display_command,
            message=str(exc),
            error_type=exc.__class__.__name__,
        ).to_manifest()

    payload = _extract_json_payload(result.stdout)
    launch_ready = None
    message = "serve --check completed."
    if payload is not None:
        launch_ready = payload.get("launch_ready")
        message = str(
            payload.get("launch_blocked_reason")
            or payload.get("application_probe", {}).get("message")
            or payload.get("selected_runner_profile", {}).get("status")
            or message
        )
    passed = bool(result.returncode == 0 and launch_ready is True)
    return CommandProbeResult(
        passed=passed,
        executed=True,
        command=display_command,
        message=message,
        exit_code=int(result.returncode),
        launch_ready=bool(launch_ready) if launch_ready is not None else None,
        stdout=_trim_probe_output(result.stdout),
        stderr=_trim_probe_output(result.stderr),
    ).to_manifest()


def probe_application_factory(*, deployment: Any, settings_obj: object | None = None) -> tuple[ApplicationProbeResult, Any | None]:
    try:
        app = build_app(settings_obj, deployment=deployment)
    except Exception as exc:  # pragma: no cover - exercised via checkpoint environment and monkeypatched tests
        return (
            ApplicationProbeResult(
                passed=False,
                app_factory="tigrbl_auth.api.app.build_app",
                message=str(exc),
                error_type=exc.__class__.__name__,
            ),
            None,
        )
    active_targets = len(getattr(deployment, "active_targets", []) or [])
    active_routes = len(getattr(deployment, "active_routes", []) or [])
    return (
        ApplicationProbeResult(
            passed=True,
            app_factory="tigrbl_auth.api.app.build_app",
            message=f"Application factory materialized successfully with {active_routes} active routes and {active_targets} active targets.",
            error_type=None,
        ),
        app,
    )


def build_runner_profile_report(
    repo_root: Path,
    *,
    deployment: Any,
    environment: str = "development",
    host: str = "127.0.0.1",
    port: int = 8000,
    workers: int = 1,
    access_log: bool = True,
    lifespan: str = "auto",
    graceful_timeout: int = 30,
    enable_execution_probes: bool | None = None,
    report_mode: str | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    resolved_report_mode = _runtime_report_mode(repo_root, report_mode)
    if resolved_report_mode == "validated-runs":
        return build_validated_runner_profile_report(repo_root, deployment=deployment)
    if enable_execution_probes is None:
        enable_execution_probes = os.environ.get("TIGRBL_AUTH_SKIP_EXECUTION_PROBES", "").strip().lower() not in {"1", "true", "yes", "on"}
    app_probe, app = probe_application_factory(deployment=deployment)
    if app_probe.passed and enable_execution_probes:
        surface_probe = probe_http_surface_endpoints(app=app, deployment=deployment)
    elif not app_probe.passed:
        surface_probe = _surface_probe_skipped("Skipped because the application factory did not materialize in this environment.")
    else:
        surface_probe = _surface_probe_skipped("Execution probes were disabled for this invocation.")
    support_manifest = _build_runner_support_manifest(repo_root)
    hash_matrix = build_runtime_hash_matrix(
        deployment=deployment,
        environment=environment,
        host=host,
        port=port,
        workers=workers,
        access_log=access_log,
        lifespan=lifespan,
        graceful_timeout=graceful_timeout,
    )
    profiles: list[dict[str, Any]] = []
    ready_count = 0
    missing_count = 0
    invalid_count = 0
    for adapter in iter_runner_adapters():
        plan = build_runtime_plan(
            deployment=deployment,
            runner=adapter.name,
            environment=environment,
            host=host,
            port=port,
            workers=workers,
            access_log=access_log,
            lifespan=lifespan,
            graceful_timeout=graceful_timeout,
        )
        diagnostics = [item.to_manifest() for item in plan.diagnostics_report]
        installed = adapter.is_available()
        support = dict((support_manifest.get("profiles") or {}).get(adapter.name, {}))
        serve_command = f"tigrbl-auth serve --repo-root {repo_root} --server {adapter.name} --format json --check"
        if enable_execution_probes and installed and app_probe.passed and surface_probe.get("passed", False):
            serve_check = probe_runner_serve_check(repo_root, adapter.name)
        elif not enable_execution_probes:
            serve_check = _command_probe_skipped(serve_command, "Execution probes were disabled for this invocation.")
        elif not installed:
            serve_check = _command_probe_skipped(serve_command, "Skipped because the runner is not installed in this environment.")
        elif not app_probe.passed:
            serve_check = _command_probe_skipped(serve_command, "Skipped because the application factory did not materialize in this environment.")
        else:
            serve_check = _command_probe_skipped(serve_command, "Skipped because runtime HTTP surface probes failed.")

        if not installed:
            status = "missing"
            missing_count += 1
        elif (
            not app_probe.passed
            or any(item["level"] == "error" for item in diagnostics)
            or (enable_execution_probes and not surface_probe.get("passed", False))
            or (enable_execution_probes and not serve_check.get("passed", False))
        ):
            status = "invalid"
            invalid_count += 1
        else:
            status = "ready"
            ready_count += 1
        profiles.append(
            {
                "name": adapter.name,
                "display_name": adapter.display_name,
                "status": status,
                "installed": installed,
                "available_module": adapter.available_module_name(),
                "capabilities": [item.to_manifest() for item in adapter.capabilities],
                "flag_metadata": [item.to_manifest() for item in adapter.flag_metadata],
                "diagnostics": diagnostics,
                "application_hash": hash_matrix[adapter.name]["application_hash"],
                "runtime_hash": hash_matrix[adapter.name]["runtime_hash"],
                "serve_check": serve_check,
                **support,
            }
        )
    placeholder_supported_runner_names = [item["name"] for item in profiles if item.get("placeholder_supported")]
    declared_ci_installable_runner_names = [item["name"] for item in profiles if item.get("declared_installable_from_repository")]
    serve_check_passed_count = sum(1 for item in profiles if item.get("serve_check", {}).get("passed"))
    execution_probe_complete = bool(
        enable_execution_probes
        and app_probe.passed
        and surface_probe.get("executed", False)
        and all(item.get("serve_check", {}).get("executed", False) for item in profiles if item.get("installed"))
    )
    return {
        "generated_at": _utc_timestamp(),
        "deployment_profile": deployment.profile,
        "report_mode": "live-probe",
        "application_probe": app_probe.to_manifest(),
        "surface_probe": surface_probe,
        "summary": {
            "runner_count": len(profiles),
            "ready_count": ready_count,
            "missing_count": missing_count,
            "invalid_count": invalid_count,
            "application_hash_invariant": len({item["application_hash"] for item in profiles}) == 1 if profiles else False,
            "pyproject_requires_python": support_manifest.get("requires_python"),
            "supported_python_versions": support_manifest.get("supported_python_versions", []),
            "placeholder_supported_runner_count": len(placeholder_supported_runner_names),
            "placeholder_supported_runner_names": placeholder_supported_runner_names,
            "declared_ci_installable_runner_count": len(declared_ci_installable_runner_names),
            "declared_ci_installable_runner_names": declared_ci_installable_runner_names,
            "declared_ci_install_probe_complete": len(declared_ci_installable_runner_names) == len(profiles),
            "execution_probes_enabled": bool(enable_execution_probes),
            "surface_probe_passed": bool(surface_probe.get("passed", False)),
            "surface_probe_endpoint_count": int(surface_probe.get("endpoint_count", 0)),
            "surface_probe_passed_count": int(surface_probe.get("passed_count", 0)),
            "surface_probe_failed_count": int(surface_probe.get("failed_count", 0)),
            "serve_check_passed_count": serve_check_passed_count,
            "execution_probe_complete": execution_probe_complete,
            "source_mode": "live-probe",
            "required_runtime_cell_count": len([version for cfg in RUNTIME_VALIDATION_GROUPS.values() for version in cfg["supported_python_versions"]]),
            "validated_runtime_cell_count": 0,
            "validated_runtime_cell_passed_count": 0,
            "validated_runtime_matrix_green": False,
            "validated_download_collection_present": False,
        },
        "profiles": profiles,
    }


def write_runtime_profile_report(
    repo_root: Path,
    *,
    deployment: Any,
    environment: str = "development",
    host: str = "127.0.0.1",
    port: int = 8000,
    workers: int = 1,
    access_log: bool = True,
    lifespan: str = "auto",
    graceful_timeout: int = 30,
    report_dir: Path | None = None,
    enable_execution_probes: bool | None = None,
    report_mode: str | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)
    payload = build_runner_profile_report(
        repo_root,
        deployment=deployment,
        environment=environment,
        host=host,
        port=port,
        workers=workers,
        access_log=access_log,
        lifespan=lifespan,
        graceful_timeout=graceful_timeout,
        enable_execution_probes=enable_execution_probes,
        report_mode=report_mode,
    )
    _write_json(report_dir / "runtime_profile_report.json", payload)
    lines = [
        "# Runtime Profile Report",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Deployment profile: `{payload['deployment_profile']}`",
        f"- Report mode: `{payload.get('report_mode', payload.get('summary', {}).get('source_mode', 'live-probe'))}`",
        f"- Validated artifact source: `{payload.get('validated_artifact_source')}`",
        f"- Application factory probe passed: `{payload['application_probe']['passed']}`",
        f"- Ready profiles: `{payload['summary']['ready_count']}`",
        f"- Missing profiles: `{payload['summary']['missing_count']}`",
        f"- Invalid profiles: `{payload['summary']['invalid_count']}`",
        f"- Application hash invariant: `{payload['summary']['application_hash_invariant']}`",
        f"- Pyproject requires-python: `{payload['summary']['pyproject_requires_python']}`",
        f"- Supported Python versions: `{', '.join(payload['summary']['supported_python_versions'])}`",
        f"- Placeholder-supported runners: `{payload['summary']['placeholder_supported_runner_count']}`",
        f"- Declared CI-installable runners: `{payload['summary']['declared_ci_installable_runner_count']}`",
        f"- Declared CI install/probe complete: `{payload['summary']['declared_ci_install_probe_complete']}`",
        f"- Execution probes enabled: `{payload['summary']['execution_probes_enabled']}`",
        f"- Surface probe passed: `{payload['summary']['surface_probe_passed']}`",
        f"- Surface probe endpoints: `{payload['summary']['surface_probe_endpoint_count']}`",
        f"- Serve-check passes: `{payload['summary']['serve_check_passed_count']}`",
        f"- Execution probe complete: `{payload['summary']['execution_probe_complete']}`",
        f"- Required runtime cells: `{payload['summary'].get('required_runtime_cell_count')}`",
        f"- Validated runtime cells present: `{payload['summary'].get('validated_runtime_cell_count')}`",
        f"- Validated runtime cells passed: `{payload['summary'].get('validated_runtime_cell_passed_count')}`",
        f"- Validated runtime matrix green: `{payload['summary'].get('validated_runtime_matrix_green')}`",
        "",
        "## Application Probe",
        "",
        f"- App factory: `{payload['application_probe'].get('app_factory', 'tigrbl_auth.api.app.build_app')}`",
        f"- Message: {payload['application_probe']['message']}",
        "",
        "## Surface Probe",
        "",
        f"- Executed: `{payload['surface_probe']['executed']}`",
        f"- Passed: `{payload['surface_probe']['passed']}`",
        f"- Message: {payload['surface_probe']['message']}",
        f"- Endpoint count: `{payload['surface_probe']['endpoint_count']}`",
        f"- Passed endpoints: `{payload['surface_probe']['passed_count']}`",
        f"- Failed endpoints: `{payload['surface_probe']['failed_count']}`",
        "",
        "## Runner Profiles",
        "",
    ]
    for item in payload["profiles"]:
        lines.extend(
            [
                f"### {item['display_name']} (`{item['name']}`)",
                "",
                f"- Status: `{item['status']}`",
                f"- Installed: `{item['installed']}`",
                f"- Module: `{item['available_module']}`",
                f"- Placeholder-supported: `{item.get('placeholder_supported')}`",
                f"- Declared CI-installable: `{item.get('declared_installable_from_repository')}`",
                f"- Serve check passed: `{item.get('serve_check', {}).get('passed')}`",
                f"- Serve check message: {item.get('serve_check', {}).get('message', '')}",
            ]
        )
        validated_matrix = item.get("validated_matrix") or {}
        if validated_matrix:
            lines.extend(
                [
                    f"- Validated matrix profile: `{validated_matrix.get('matrix_profile')}`",
                    f"- Expected identities: `{', '.join(validated_matrix.get('expected_identities', []))}`",
                    f"- Present identities: `{', '.join(validated_matrix.get('present_identities', []))}`",
                    f"- Passed identities: `{', '.join(validated_matrix.get('passed_identities', []))}`",
                    f"- Missing identities: `{', '.join(validated_matrix.get('missing_identities', []))}`",
                    f"- Failed identities: `{', '.join(validated_matrix.get('failed_identities', []))}`",
                ]
            )
        lines.append("")
    (report_dir / "runtime_profile_report.md").write_text("\n".join(lines), encoding="utf-8")
    return payload



def runtime_evidence_paths(repo_root: Path, runner: str) -> dict[str, Path]:
    stamp = _utc_timestamp()
    root = repo_root.resolve() / "dist" / "runtime-profiles" / runner
    root.mkdir(parents=True, exist_ok=True)
    return {
        "root": root,
        "startup": root / f"{stamp}-startup.json",
        "shutdown": root / f"{stamp}-shutdown.json",
    }


async def _serve_with_signal_handlers(
    *,
    adapter: Any,
    app: Any,
    plan: Any,
    startup_path: Path,
    shutdown_path: Path,
    startup_payload: dict[str, Any],
) -> int:
    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()
    signal_state: dict[str, Any] = {"received": []}
    startup_details: dict[str, Any] = {}

    def _request_shutdown(signame: str) -> None:
        signal_state["received"].append(signame)
        shutdown_event.set()

    registered: list[signal.Signals] = []
    for sig in (signal.SIGINT, signal.SIGTERM):
        with suppress(NotImplementedError, RuntimeError, ValueError):
            loop.add_signal_handler(sig, _request_shutdown, sig.name)
            registered.append(sig)

    def _startup_callback(details: dict[str, Any]) -> None:
        startup_details.update(details)
        payload = dict(startup_payload)
        payload["adapter_startup"] = dict(startup_details)
        payload["event"] = "runtime-starting"
        _write_json(startup_path, payload)

    if not startup_path.exists():
        _write_json(startup_path, dict(startup_payload, event="runtime-starting"))

    exit_code = 1
    failure: dict[str, str] | None = None
    try:
        exit_code = await adapter.serve(app, plan, shutdown_event=shutdown_event, startup_callback=_startup_callback)
    except KeyboardInterrupt:
        shutdown_event.set()
        exit_code = 130
    except Exception as exc:  # pragma: no cover - depends on selected runner runtime
        failure = _error_manifest(exc)
        exit_code = 1
    finally:
        for sig in registered:
            with suppress(NotImplementedError, RuntimeError, ValueError):
                loop.remove_signal_handler(sig)
        shutdown_payload = {
            "event": "runtime-stopped",
            "runner": plan.runner,
            "application_hash": plan.application_hash,
            "runtime_hash": plan.runtime_hash,
            "exit_code": exit_code,
            "signals": signal_state["received"],
            "adapter_startup": dict(startup_details),
        }
        if failure is not None:
            shutdown_payload["failure"] = failure
        _write_json(shutdown_path, shutdown_payload)
    return exit_code


def launch_runtime_profile(
    repo_root: Path,
    *,
    app: Any,
    plan: Any,
    adapter: Any,
    startup_payload: dict[str, Any],
    evidence_paths: dict[str, Path] | None = None,
) -> int:
    repo_root = repo_root.resolve()
    evidence_paths = evidence_paths or runtime_evidence_paths(repo_root, plan.runner)
    payload = dict(startup_payload)
    payload.setdefault(
        "runtime_evidence",
        {
            "startup": str(evidence_paths["startup"].relative_to(repo_root)),
            "shutdown": str(evidence_paths["shutdown"].relative_to(repo_root)),
        },
    )
    pid_path: Path | None = None
    if plan.pid_file:
        pid_path = Path(plan.pid_file).resolve()
        pid_path.parent.mkdir(parents=True, exist_ok=True)
        pid_path.write_text(f"{os.getpid()}\n", encoding="utf-8")
    try:
        return asyncio.run(
            _serve_with_signal_handlers(
                adapter=adapter,
                app=app,
                plan=plan,
                startup_path=evidence_paths["startup"],
                shutdown_path=evidence_paths["shutdown"],
                startup_payload=payload,
            )
        )
    finally:
        if pid_path is not None and pid_path.exists():
            pid_path.unlink()


__all__ = [
    "build_runner_profile_report",
    "launch_runtime_profile",
    "probe_application_factory",
    "probe_http_surface_endpoints",
    "probe_runner_serve_check",
    "run_runtime_foundation_check",
    "runtime_evidence_paths",
    "write_runtime_profile_report",
]
