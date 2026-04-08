from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Any, Mapping

CI_ENV_NAMES = (
    "GITHUB_ACTIONS",
    "GITHUB_WORKFLOW",
    "GITHUB_JOB",
    "GITHUB_RUN_ID",
    "GITHUB_RUN_ATTEMPT",
    "GITHUB_REF",
    "GITHUB_SHA",
    "RUNNER_OS",
    "RUNNER_ARCH",
    "CI",
)


def python_version_string() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def python_tag(python_version: str | None = None) -> str:
    normalized = str(python_version or python_version_string()).strip()
    if not normalized:
        return f"py{sys.version_info.major}{sys.version_info.minor}"
    if normalized.startswith("py"):
        normalized = normalized[2:]
    parts = [part for part in normalized.split(".") if part]
    if len(parts) >= 2:
        return f"py{parts[0]}{parts[1]}"
    return f"py{normalized.replace('.', '')}"


def runtime_identity(profile: str, python_version: str | None = None) -> str:
    return f"{str(profile).strip()}@{python_tag(python_version)}"


def lane_identity(lane: str, python_version: str | None = None) -> str:
    return f"{str(lane).strip()}@{python_tag(python_version)}"


def migration_identity(name: str = "migration-portability", python_version: str | None = None) -> str:
    return f"{str(name).strip()}@{python_tag(python_version)}"


def current_environment_identity(
    *,
    matrix_profile: str | None = None,
    install_profile: str | None = None,
    test_lane: str | None = None,
    runner: str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    executable = Path(sys.executable).resolve()
    executable_str = str(executable)
    if repo_root is not None:
        try:
            executable_str = str(executable.relative_to(repo_root.resolve()))
        except ValueError:
            executable_str = str(executable)
    payload: dict[str, Any] = {
        "python_version": python_version_string(),
        "python_full_version": sys.version.split()[0],
        "python_tag": python_tag(),
        "implementation": platform.python_implementation(),
        "implementation_version": platform.python_version(),
        "executable": executable_str,
        "platform": platform.platform(),
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "tox_env": os.environ.get("TOX_ENV_NAME"),
        "matrix_profile": matrix_profile or os.environ.get("TIGRBL_AUTH_MATRIX_PROFILE"),
        "install_profile": install_profile or os.environ.get("TIGRBL_AUTH_INSTALL_PROFILE"),
        "test_lane": test_lane or os.environ.get("TIGRBL_AUTH_TEST_LANE"),
        "runner": runner or os.environ.get("TIGRBL_AUTH_RUNNER"),
    }
    ci = {name: value for name in CI_ENV_NAMES if (value := os.environ.get(name))}
    if ci:
        payload["ci"] = ci
    return payload


def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _payload_python_version(payload: Mapping[str, Any]) -> str:
    return str(payload.get("python_version", "")).strip()


def environment_identity_ready(payload: Mapping[str, Any]) -> bool:
    env_identity = _mapping(payload.get("environment_identity"))
    if not env_identity:
        return False
    payload_python_version = _payload_python_version(payload)
    env_python_version = str(env_identity.get("python_version", "")).strip()
    if not payload_python_version or not env_python_version or env_python_version != payload_python_version:
        return False
    tox_env = str(payload.get("tox_env") or "").strip()
    env_tox = str(env_identity.get("tox_env") or "").strip()
    if tox_env and env_tox and env_tox != tox_env:
        return False
    return True


def install_evidence_ready(payload: Mapping[str, Any]) -> bool:
    install_artifact = str(payload.get("install_substrate_artifact") or "").strip()
    install_sha256 = str(payload.get("install_substrate_artifact_sha256") or "").strip()
    install_identity = _mapping(payload.get("install_substrate_environment_identity"))
    payload_python_version = _payload_python_version(payload)
    return bool(
        install_artifact
        and install_sha256
        and bool(payload.get("install_substrate_static_manifest_passed", False))
        and bool(payload.get("install_substrate_current_profile_import_probe_passed", False))
        and bool(payload.get("install_substrate_runtime_surface_probe_passed", False))
        and environment_identity_ready(payload)
        and install_identity
        and str(install_identity.get("python_version", "")).strip() == payload_python_version
    )


def runtime_surface_probe_ready(payload: Mapping[str, Any]) -> bool:
    endpoint_count = _coerce_int(payload.get("surface_probe_endpoint_count")) or 0
    passed_count = _coerce_int(payload.get("surface_probe_passed_count")) or 0
    failed_count = _coerce_int(payload.get("surface_probe_failed_count")) or 0
    return bool(
        payload.get("surface_probe_passed", False)
        and endpoint_count > 0
        and passed_count >= endpoint_count
        and failed_count == 0
    )


def validated_runtime_manifest_passed(payload: Mapping[str, Any]) -> bool:
    profile = str(payload.get("matrix_profile", "")).strip()
    python_version = _payload_python_version(payload)
    if not profile or not python_version:
        return False
    if str(payload.get("identity", "")).strip() != runtime_identity(profile, python_version):
        return False
    if not install_evidence_ready(payload):
        return False
    smoke_artifact = str(payload.get("runtime_smoke_artifact") or "").strip()
    smoke_sha256 = str(payload.get("runtime_smoke_artifact_sha256") or "").strip()
    if not smoke_artifact or not smoke_sha256:
        return False
    if not bool(payload.get("runtime_smoke_passed", False)):
        return False
    if not bool(payload.get("application_probe_passed", False)):
        return False
    if not runtime_surface_probe_ready(payload):
        return False
    runner = str(payload.get("runner") or "").strip()
    if runner:
        return bool(
            bool(payload.get("runner_available", False))
            and bool(payload.get("serve_check_passed", False))
            and str(payload.get("serve_check_artifact") or "").strip()
            and str(payload.get("serve_check_artifact_sha256") or "").strip()
        )
    return True


def validated_test_lane_manifest_passed(payload: Mapping[str, Any]) -> bool:
    lane = str(payload.get("lane", "")).strip()
    python_version = _payload_python_version(payload)
    if not lane or not python_version:
        return False
    if str(payload.get("identity", "")).strip() != lane_identity(lane, python_version):
        return False
    if not install_evidence_ready(payload):
        return False
    pytest_exit_code = _coerce_int(payload.get("pytest_exit_code"))
    pytest_report_exit_code = _coerce_int(payload.get("pytest_report_exit_code"))
    collected = max(_coerce_int(payload.get("tests_collected")) or 0, _coerce_int(payload.get("tests_total")) or 0)
    report_present = bool(payload.get("pytest_report_present", False) or payload.get("pytest_report_artifact"))
    report_sha256 = str(payload.get("pytest_report_sha256") or "").strip()
    return bool(
        report_present
        and report_sha256
        and pytest_exit_code == 0
        and pytest_report_exit_code == 0
        and collected > 0
    )


def validated_migration_backend_manifest_passed(payload: Mapping[str, Any]) -> bool:
    python_version = _payload_python_version(payload)
    backend = str(payload.get("backend") or "").strip()
    if not python_version or backend not in {"sqlite", "postgres"}:
        return False
    expected_identity = migration_identity(f"migration-portability-{backend}", python_version)
    if str(payload.get("identity", "")).strip() != expected_identity:
        return False
    if not install_evidence_ready(payload):
        return False
    artifacts = _mapping(payload.get("artifacts"))
    artifact_shas = _mapping(payload.get("artifact_sha256"))
    if not {"upgrade", "downgrade", "reapply"}.issubset(set(artifacts)):
        return False
    if not {"upgrade", "downgrade", "reapply"}.issubset(set(artifact_shas)):
        return False
    if not bool(
        payload.get("available", False)
        and payload.get("passed", False)
        and payload.get("upgrade_passed", False)
        and payload.get("downgrade_passed", False)
        and payload.get("reapply_passed", False)
    ):
        return False
    expected_head_revision = str(payload.get("expected_head_revision") or "").strip()
    downgrade_target_revision = str(payload.get("downgrade_target_revision") or "").strip()
    if not expected_head_revision or not downgrade_target_revision:
        return False
    if str(payload.get("head_revision_after_upgrade") or "").strip() != expected_head_revision:
        return False
    if str(payload.get("downgraded_revision") or "").strip() != expected_head_revision:
        return False
    if str(payload.get("head_revision_after_downgrade") or "").strip() != downgrade_target_revision:
        return False
    if str(payload.get("head_revision_after_reapply") or "").strip() != expected_head_revision:
        return False
    return True


def validated_migration_manifest_passed(payload: Mapping[str, Any]) -> bool:
    python_version = _payload_python_version(payload)
    if not python_version:
        return False
    expected_identity = migration_identity("migration-portability", python_version)
    if str(payload.get("identity", "")).strip() != expected_identity:
        return False
    if not install_evidence_ready(payload):
        return False
    required_backends = {str(item) for item in (payload.get("required_backends") or ["sqlite", "postgres"]) if str(item)}
    backends = {str(item) for item in (payload.get("backends") or []) if str(item)}
    passed_backends = {str(item) for item in (payload.get("passed_backends") or []) if str(item)}
    if not required_backends or not required_backends.issubset(backends) or not required_backends.issubset(passed_backends):
        return False
    backend_manifests = payload.get("backend_manifests") or []
    manifest_backends = {str(item.get("backend")) for item in backend_manifests if isinstance(item, Mapping)}
    if not required_backends.issubset(manifest_backends):
        return False
    for item in backend_manifests:
        if not isinstance(item, Mapping):
            return False
        if not str(item.get("path") or "").strip():
            return False
        if not str(item.get("sha256") or "").strip():
            return False
    revision_inventory = payload.get("revision_inventory") or []
    expected_head_revision = str(payload.get("expected_head_revision") or payload.get("head_revision") or "").strip()
    downgrade_target_revision = str(payload.get("downgrade_target_revision") or "").strip()
    if not revision_inventory or not expected_head_revision or not downgrade_target_revision:
        return False
    backend_results = _mapping(payload.get("backend_results"))
    for backend in sorted(required_backends):
        result = _mapping(backend_results.get(backend))
        if not result:
            return False
        artifacts = _mapping(result.get("artifacts"))
        if not {"upgrade", "downgrade", "reapply"}.issubset(set(artifacts)):
            return False
        if not bool(
            result.get("available", False)
            and result.get("passed", False)
            and result.get("upgrade_passed", False)
            and result.get("downgrade_passed", False)
            and result.get("reapply_passed", False)
        ):
            return False
        if str(result.get("expected_head_revision") or expected_head_revision).strip() != expected_head_revision:
            return False
        if str(result.get("head_revision_after_upgrade") or "").strip() != expected_head_revision:
            return False
        if str(result.get("downgraded_revision") or "").strip() != expected_head_revision:
            return False
        if str(result.get("head_revision_after_downgrade") or "").strip() != downgrade_target_revision:
            return False
        if str(result.get("head_revision_after_reapply") or "").strip() != expected_head_revision:
            return False
    pytest_exit_code = _coerce_int(payload.get("pytest_exit_code"))
    pytest_report_sha256 = str(payload.get("pytest_report_sha256") or "").strip()
    pytest_report_present = bool(payload.get("pytest_report_artifact")) and bool(pytest_report_sha256)
    report_passed = bool(payload.get("report_passed", payload.get("passed", False)))
    return bool(
        report_passed
        and pytest_exit_code in {None, 0}
        and pytest_report_present
    )


__all__ = [
    "current_environment_identity",
    "environment_identity_ready",
    "install_evidence_ready",
    "lane_identity",
    "migration_identity",
    "python_tag",
    "python_version_string",
    "runtime_identity",
    "runtime_surface_probe_ready",
    "validated_migration_backend_manifest_passed",
    "validated_migration_manifest_passed",
    "validated_runtime_manifest_passed",
    "validated_test_lane_manifest_passed",
]
