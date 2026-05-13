from __future__ import annotations

import configparser
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tigrbl_auth.cli.certification_evidence import current_environment_identity, runtime_identity
from tigrbl_auth.path_safety import sanitize_local_paths
from tigrbl_auth.repo_truth import has_install_matrix_workflow, has_release_gate_workflow, workflow_role_text

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]

SUPPORTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12")
RUNTIME_MATRIX_ENVS = (
    "py310-base",
    "py311-base",
    "py312-base",
    "py310-sqlite-uvicorn",
    "py311-sqlite-uvicorn",
    "py312-sqlite-uvicorn",
    "py310-postgres-hypercorn",
    "py311-postgres-hypercorn",
    "py312-postgres-hypercorn",
    "py311-tigrcorn",
    "py312-tigrcorn",
    "py310-devtest",
    "py311-devtest",
    "py312-devtest",
)
TEST_LANE_ENVS = (
    "py310-test-core",
    "py311-test-core",
    "py312-test-core",
    "py310-test-integration",
    "py311-test-integration",
    "py312-test-integration",
    "py310-test-conformance",
    "py311-test-conformance",
    "py312-test-conformance",
    "py310-test-security-negative",
    "py311-test-security-negative",
    "py312-test-security-negative",
    "py310-test-interop",
    "py311-test-interop",
    "py312-test-interop",
)
ADDITIONAL_CERTIFICATION_ENVS = (
    "py311-gates",
    "py311-test-extension",
    "py311-migration-portability",
    "py311-final-certification",
)
CERTIFICATION_TOX_ENVS = RUNTIME_MATRIX_ENVS + TEST_LANE_ENVS + ADDITIONAL_CERTIFICATION_ENVS
RUNTIME_IMPORT_SURFACES = (
    "tigrbl_auth.api.app",
    "tigrbl_auth.app",
    "tigrbl_auth.plugin",
    "tigrbl_auth.gateway",
)

REQUIREMENT_FORBIDDEN_PATTERNS = (
    "-e ",
    " @ file:",
    " @ git+",
    "git+https://",
    "git+ssh://",
    "../",
    "./",
    "\\",
)

_BASE_MODULES: tuple[dict[str, Any], ...] = (
    {"module": "tigrbl", "package": "tigrbl", "category": "runtime"},
    {"module": "swarmauri_core", "package": "swarmauri_core", "category": "runtime"},
    {"module": "swarmauri_base", "package": "swarmauri_base", "category": "runtime"},
    {"module": "swarmauri_standard", "package": "swarmauri_standard", "category": "runtime"},
    {"module": "swarmauri_tokens_jwt", "package": "swarmauri_tokens_jwt", "category": "runtime"},
    {"module": "swarmauri_signing_jws", "package": "swarmauri_signing_jws", "category": "runtime"},
    {"module": "swarmauri_signing_ed25519", "package": "swarmauri_signing_ed25519", "category": "runtime"},
    {"module": "swarmauri_signing_dpop", "package": "swarmauri_signing_dpop", "category": "runtime"},
    {"module": "swarmauri_crypto_jwe", "package": "swarmauri_crypto_jwe", "category": "runtime"},
    {"module": "swarmauri_crypto_paramiko", "package": "swarmauri_crypto_paramiko", "category": "runtime"},
    {"module": "swarmauri_keyprovider_file", "package": "swarmauri_keyprovider_file", "category": "runtime"},
    {"module": "swarmauri_keyprovider_local", "package": "swarmauri_keyprovider_local", "category": "runtime"},
    {"module": "sqlalchemy", "package": "sqlalchemy", "category": "runtime"},
    {"module": "bcrypt", "package": "bcrypt", "category": "runtime"},
    {"module": "httpx", "package": "httpx", "category": "runtime"},
    {"module": "yaml", "package": "PyYAML", "category": "runtime"},
    {"module": "pydantic", "package": "pydantic", "category": "runtime"},
    {"module": "pydantic_settings", "package": "pydantic-settings", "category": "runtime"},
    {"module": "dotenv", "package": "python-dotenv", "category": "runtime"},
    {"module": "multipart", "package": "python-multipart", "category": "runtime"},
    {"module": "aiosqlite", "package": "aiosqlite", "category": "runtime"},
)
_TEST_MODULES: tuple[dict[str, Any], ...] = (
    {"module": "pytest", "package": "pytest", "category": "test"},
    {"module": "xdist", "package": "pytest-xdist", "category": "test"},
    {"module": "pytest_jsonreport", "package": "pytest-json-report", "category": "test"},
    {"module": "pytest_timeout", "package": "pytest-timeout", "category": "test"},
    {"module": "pytest_benchmark", "package": "pytest-benchmark", "category": "test"},
    {"module": "requests", "package": "requests", "category": "test"},
)
_SQLITE_MODULES: tuple[dict[str, Any], ...] = ()
_POSTGRES_MODULES: tuple[dict[str, Any], ...] = (
    {"module": "asyncpg", "package": "asyncpg", "category": "storage"},
)
_UVICORN_MODULES: tuple[dict[str, Any], ...] = (
    {"module": "uvicorn", "package": "uvicorn", "category": "runner"},
)
_HYPERCORN_MODULES: tuple[dict[str, Any], ...] = (
    {"module": "hypercorn", "package": "hypercorn", "category": "runner"},
)
_TIGRCORN_MODULES: tuple[dict[str, Any], ...] = (
    {
        "module": "tigrcorn",
        "package": "tigrcorn",
        "category": "runner",
        "python_min": (3, 11),
        "python_max_exclusive": (3, 13),
    },
)

PROFILE_IMPORT_GROUPS: dict[str, tuple[tuple[dict[str, Any], ...], ...]] = {
    "base": (_BASE_MODULES,),
    "sqlite-uvicorn": (_BASE_MODULES, _SQLITE_MODULES, _UVICORN_MODULES),
    "postgres-hypercorn": (_BASE_MODULES, _POSTGRES_MODULES, _HYPERCORN_MODULES),
    "tigrcorn": (_BASE_MODULES, _TIGRCORN_MODULES),
    "devtest": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _UVICORN_MODULES),
    "release-gates": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-core": (_BASE_MODULES, _TEST_MODULES),
    "test-integration": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-conformance": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-security-negative": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-interop": (_BASE_MODULES, _TEST_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-extension": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "migration-portability": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "final-certification": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
}

PROFILE_TOGGLES: dict[str, dict[str, Any]] = {
    "base": {"constraints": ["constraints/base.txt"], "extras": []},
    "sqlite-uvicorn": {"constraints": ["constraints/base.txt", "constraints/runner-uvicorn.txt"], "extras": ["sqlite", "uvicorn"]},
    "postgres-hypercorn": {"constraints": ["constraints/base.txt", "constraints/runner-hypercorn.txt"], "extras": ["postgres", "hypercorn"]},
    "tigrcorn": {"constraints": ["constraints/base.txt", "constraints/runner-tigrcorn.txt"], "extras": ["tigrcorn"]},
    "devtest": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt"], "extras": ["test", "sqlite", "uvicorn"]},
    "release-gates": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-core": {"constraints": ["constraints/base.txt", "constraints/test.txt"], "extras": ["test"]},
    "test-integration": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-conformance": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-security-negative": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-interop": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "servers"]},
    "test-extension": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "migration-portability": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "final-certification": {"constraints": ["constraints/base.txt", "constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
}

INSTALL_WORKFLOW_RUNTIME_ENVS = set(RUNTIME_MATRIX_ENVS)
RELEASE_WORKFLOW_RUNTIME_ENVS = set(RUNTIME_MATRIX_ENVS)
RELEASE_WORKFLOW_TEST_LANE_ENVS = set(TEST_LANE_ENVS)
RELEASE_WORKFLOW_EXTRA_ENVS = {"py311-migration-portability", "py311-final-certification"}

TOX_PROFILE_SECTION_EXPECTATIONS = {
    "[testenv]": "base",
    "[testenv:py{310,311,312}-sqlite-uvicorn]": "sqlite-uvicorn",
    "[testenv:py{310,311,312}-postgres-hypercorn]": "postgres-hypercorn",
    "[testenv:py{311,312}-tigrcorn]": "tigrcorn",
    "[testenv:py{310,311,312}-devtest]": "devtest",
    "[testenv:py311-gates]": "release-gates",
    "[testenv:py{310,311,312}-test-core]": "test-core",
    "[testenv:py{310,311,312}-test-integration]": "test-integration",
    "[testenv:py{310,311,312}-test-conformance]": "test-conformance",
    "[testenv:py{310,311,312}-test-security-negative]": "test-security-negative",
    "[testenv:py{310,311,312}-test-interop]": "test-interop",
    "[testenv:py311-test-extension]": "test-extension",
    "[testenv:py311-migration-portability]": "migration-portability",
    "[testenv:py311-final-certification]": "final-certification",
}


@dataclass(slots=True)
class ModuleProbeResult:
    module: str
    package: str
    category: str
    passed: bool
    message: str
    error_type: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "module": self.module,
            "package": self.package,
            "passed": self.passed,
            "category": self.category,
            "message": self.message,
            "error_type": self.error_type,
        }


def _normalize_requirement(specifier: str) -> str:
    cleaned = re.sub(r"\s+", " ", specifier.strip())
    cleaned = re.sub(r"\s*;\s*", "; ", cleaned)
    cleaned = re.sub(r"\s*,\s*", ",", cleaned)
    cleaned = re.sub(r"\s*([<>=!~]{1,2})\s*", r"\1", cleaned)
    return cleaned


def _is_exact_pin(specifier: str) -> bool:
    cleaned = _normalize_requirement(specifier)
    return "==" in cleaned and all(token not in cleaned for token in (">=", "<=", "~=", "!=", " @ "))




_EXTRAS_NAME_PATTERN = re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)\[[^\]]+\](?P<rest>.*)$")


def _constraint_safe_requirement(specifier: str) -> str:
    cleaned = _normalize_requirement(specifier)
    match = _EXTRAS_NAME_PATTERN.match(cleaned)
    if not match:
        return cleaned
    return f"{match.group('name')}{match.group('rest')}"


def _constraint_lines_with_extras(path: Path) -> list[str]:
    return [item for item in _parse_constraints(path) if _EXTRAS_NAME_PATTERN.match(item)]
def _load_pyproject(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "pyproject.toml"
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_constraints(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(_normalize_requirement(line))
    return lines


def _requirements_have_forbidden_sources(requirements: list[str]) -> list[str]:
    hits: list[str] = []
    for item in requirements:
        normalized = _normalize_requirement(item)
        if any(pattern in normalized for pattern in REQUIREMENT_FORBIDDEN_PATTERNS):
            hits.append(normalized)
    return hits


def _read_tox(repo_root: Path) -> tuple[configparser.ConfigParser, str]:
    tox_path = repo_root / "tox.ini"
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read(tox_path, encoding="utf-8")
    return parser, tox_path.read_text(encoding="utf-8")


def _extract_tox_envlist(parser: configparser.ConfigParser) -> list[str]:
    raw = parser.get("tox", "envlist", fallback="")
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _section_block(text: str, header: str) -> str:
    pattern = rf"{re.escape(header)}\n(.*?)(?=\n\[[^\n]+\]|\Z)"
    match = re.search(pattern, text, flags=re.DOTALL)
    return match.group(1) if match else ""


def _tox_section_checks(text: str) -> dict[str, Any]:
    section_results: dict[str, dict[str, Any]] = {}
    pip_check_ok_count = 0
    install_probe_ok_count = 0
    for header, profile in TOX_PROFILE_SECTION_EXPECTATIONS.items():
        block = _section_block(text, header)
        pip_check_present = "python -I -m pip check" in block
        install_probe_present = "scripts/verify_clean_room_install_substrate.py" in block
        profile_present = f"TIGRBL_AUTH_INSTALL_PROFILE = {profile}" in block
        constraints = PROFILE_TOGGLES.get(profile, {}).get("constraints", [])
        constraints_present = all(path in block or header == "[testenv]" for path in constraints)
        section_results[header] = {
            "profile": profile,
            "pip_check_present": pip_check_present,
            "install_probe_present": install_probe_present,
            "install_profile_variable_present": profile_present,
            "constraints_present": constraints_present,
        }
        if pip_check_present:
            pip_check_ok_count += 1
        if install_probe_present and profile_present:
            install_probe_ok_count += 1
    return {
        "envlist": [],
        "sections": section_results,
        "pip_check_ok_count": pip_check_ok_count,
        "install_probe_ok_count": install_probe_ok_count,
        "section_count": len(section_results),
        "passed": all(
            item["pip_check_present"]
            and item["install_probe_present"]
            and item["install_profile_variable_present"]
            and item["constraints_present"]
            for item in section_results.values()
        ),
    }


def _workflow_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _envs_present_in_text(envs: set[str], text: str) -> tuple[list[str], list[str]]:
    present = sorted(env for env in envs if env in text)
    missing = sorted(env for env in envs if env not in text)
    return present, missing


def _build_workflow_coverage(repo_root: Path) -> dict[str, Any]:
    install_workflow = workflow_role_text(repo_root, "install-matrix")
    release_workflow = workflow_role_text(repo_root, "release-gates")

    install_present, install_missing = _envs_present_in_text(INSTALL_WORKFLOW_RUNTIME_ENVS, install_workflow)
    release_runtime_present, release_runtime_missing = _envs_present_in_text(RELEASE_WORKFLOW_RUNTIME_ENVS, release_workflow)
    release_lane_present, release_lane_missing = _envs_present_in_text(RELEASE_WORKFLOW_TEST_LANE_ENVS, release_workflow)
    release_extra_present, release_extra_missing = _envs_present_in_text(RELEASE_WORKFLOW_EXTRA_ENVS, release_workflow)

    return {
        "install_profiles_workflow_present": has_install_matrix_workflow(repo_root),
        "release_gates_workflow_present": has_release_gate_workflow(repo_root),
        "install_profiles_artifact_upload_present": "dist/install-substrate" in install_workflow,
        "release_gates_artifact_upload_present": "dist/install-substrate" in release_workflow,
        "install_profiles_runtime_env_present_count": len(install_present),
        "install_profiles_runtime_env_missing": install_missing,
        "release_gates_runtime_env_present_count": len(release_runtime_present),
        "release_gates_runtime_env_missing": release_runtime_missing,
        "release_gates_test_lane_env_present_count": len(release_lane_present),
        "release_gates_test_lane_env_missing": release_lane_missing,
        "release_gates_extra_env_present_count": len(release_extra_present),
        "release_gates_extra_env_missing": release_extra_missing,
        "install_profiles_workflow_passed": not install_missing and has_install_matrix_workflow(repo_root) and "dist/install-substrate" in install_workflow,
        "release_gates_workflow_passed": not release_runtime_missing and not release_lane_missing and not release_extra_missing and has_release_gate_workflow(repo_root) and "dist/install-substrate" in release_workflow,
    }


def _pyproject_dependency_manifest(repo_root: Path) -> dict[str, Any]:
    manifest = _load_pyproject(repo_root)
    project = manifest.get("project", {}) if isinstance(manifest, dict) else {}
    dependencies = [_normalize_requirement(str(item)) for item in (project.get("dependencies") or [])]
    optional = {
        str(name): [_normalize_requirement(str(item)) for item in values]
        for name, values in (project.get("optional-dependencies") or {}).items()
    }
    workspace_sources = (((manifest.get("tool", {}) or {}).get("uv", {}) or {}).get("sources", {}) or {}) if isinstance(manifest, dict) else {}
    forbidden = _requirements_have_forbidden_sources(dependencies)
    for values in optional.values():
        forbidden.extend(_requirements_have_forbidden_sources(values))
    return {
        "requires_python": str(project.get("requires-python", "")),
        "dependencies": dependencies,
        "optional_dependencies": optional,
        "workspace_sources_present": bool(workspace_sources),
        "forbidden_dependency_references": sorted(set(forbidden)),
        "exact_pinned_dependency_count": sum(1 for item in dependencies if _is_exact_pin(item)),
        "dependency_count": len(dependencies),
    }


def _constraint_consistency(repo_root: Path, dependency_manifest: dict[str, Any]) -> dict[str, Any]:
    base_path = repo_root / "constraints" / "base.txt"
    test_path = repo_root / "constraints" / "test.txt"
    uvicorn_path = repo_root / "constraints" / "runner-uvicorn.txt"
    hypercorn_path = repo_root / "constraints" / "runner-hypercorn.txt"
    tigrcorn_path = repo_root / "constraints" / "runner-tigrcorn.txt"

    base_constraints = _parse_constraints(base_path)
    test_constraints = _parse_constraints(test_path)
    uvicorn_constraints = _parse_constraints(uvicorn_path)
    hypercorn_constraints = _parse_constraints(hypercorn_path)
    tigrcorn_constraints = _parse_constraints(tigrcorn_path)
    optional = dependency_manifest["optional_dependencies"]
    mismatches: list[str] = []

    illegal_constraint_extras = {
        "base": _constraint_lines_with_extras(base_path),
        "test": _constraint_lines_with_extras(test_path),
        "uvicorn": _constraint_lines_with_extras(uvicorn_path),
        "hypercorn": _constraint_lines_with_extras(hypercorn_path),
        "tigrcorn": _constraint_lines_with_extras(tigrcorn_path),
    }
    for scope, items in illegal_constraint_extras.items():
        if items:
            mismatches.append(f"constraints/{'runner-' + scope if scope in {'uvicorn', 'hypercorn', 'tigrcorn'} else scope}.txt contains extras syntax that pip constraints mode does not accept")

    if set(base_constraints) != {_constraint_safe_requirement(item) for item in dependency_manifest["dependencies"]}:
        mismatches.append("constraints/base.txt does not match pyproject runtime dependencies when normalized to pip-legal constraint form")
    if set(test_constraints) != {_constraint_safe_requirement(item) for item in optional.get("test", [])}:
        mismatches.append("constraints/test.txt does not match pyproject optional-dependencies.test")
    if set(uvicorn_constraints) != {_constraint_safe_requirement(item) for item in optional.get("uvicorn", [])}:
        mismatches.append("constraints/runner-uvicorn.txt does not match pyproject optional-dependencies.uvicorn when normalized to pip-legal constraint form")
    if set(hypercorn_constraints) != {_constraint_safe_requirement(item) for item in optional.get("hypercorn", [])}:
        mismatches.append("constraints/runner-hypercorn.txt does not match pyproject optional-dependencies.hypercorn")
    if set(tigrcorn_constraints) != {_constraint_safe_requirement(item) for item in optional.get("tigrcorn", [])}:
        mismatches.append("constraints/runner-tigrcorn.txt does not match pyproject optional-dependencies.tigrcorn")
    return {
        "passed": not mismatches,
        "mismatches": mismatches,
        "illegal_constraint_extras": illegal_constraint_extras,
        "base_count": len(base_constraints),
        "test_count": len(test_constraints),
        "uvicorn_count": len(uvicorn_constraints),
        "hypercorn_count": len(hypercorn_constraints),
        "tigrcorn_count": len(tigrcorn_constraints),
    }


def _dependency_lock_consistency(repo_root: Path, dependency_manifest: dict[str, Any]) -> dict[str, Any]:
    payload = _load_json(repo_root / "constraints" / "dependency-lock.json") or {}
    install_profiles = payload.get("install_profiles", {}) if isinstance(payload, dict) else {}
    failures: list[str] = []
    if not payload:
        failures.append("constraints/dependency-lock.json is missing")
        return {
            "passed": False,
            "failures": failures,
            "install_profile_count": 0,
            "missing_profiles": sorted(PROFILE_TOGGLES),
        }
    if set(_normalize_requirement(str(item)) for item in payload.get("base", [])) != set(dependency_manifest["dependencies"]):
        failures.append("dependency lock base set drifts from pyproject runtime dependencies")
    lock_extras = {
        str(name): [_normalize_requirement(str(item)) for item in values]
        for name, values in (payload.get("extras") or {}).items()
    }
    for extra_name in ("test", "sqlite", "postgres", "uvicorn", "hypercorn", "tigrcorn", "servers"):
        if set(lock_extras.get(extra_name, [])) != set(dependency_manifest["optional_dependencies"].get(extra_name, [])):
            failures.append(f"dependency lock extra '{extra_name}' drifts from pyproject optional dependencies")
    missing_profiles: list[str] = []
    for profile_name, expected in PROFILE_TOGGLES.items():
        actual = install_profiles.get(profile_name)
        if actual is None:
            missing_profiles.append(profile_name)
            continue
        actual_constraints = [_normalize_requirement(str(item)) for item in actual.get("constraints", [])]
        actual_extras = [str(item) for item in actual.get("extras", [])]
        if actual_constraints != expected["constraints"]:
            failures.append(f"dependency lock install profile '{profile_name}' has unexpected constraints")
        if actual_extras != expected["extras"]:
            failures.append(f"dependency lock install profile '{profile_name}' has unexpected extras")
    if missing_profiles:
        failures.append("dependency lock install profiles are incomplete")
    return {
        "passed": not failures,
        "failures": failures,
        "missing_profiles": missing_profiles,
        "install_profile_count": len(install_profiles),
    }


def _current_python_supported() -> bool:
    current = sys.version_info[:3]
    return (3, 10, 0) <= current < (3, 13, 0)


def _probe_python_version(executable: list[str]) -> tuple[str | None, str | None]:
    try:
        completed = subprocess.run(
            [*executable, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    if completed.returncode != 0:
        return None, (completed.stderr or completed.stdout or "python probe failed").strip()
    return completed.stdout.strip(), None


def _detect_supported_pythons() -> list[dict[str, Any]]:
    detections: dict[str, dict[str, Any]] = {}
    if _current_python_supported():
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        detections[current_version] = {
            "version": current_version,
            "available": True,
            "path": sys.executable,
            "source": "current-interpreter",
        }
    for version in SUPPORTED_PYTHON_VERSIONS:
        for executable, source in (
            ([f"python{version}"], "path"),
            (["py", f"-{version}"], "py-launcher"),
        ):
            if version in detections:
                break
            candidate = shutil.which(executable[0])
            if not candidate:
                continue
            detected_version, error = _probe_python_version(executable)
            if detected_version == version:
                detections[version] = {
                    "version": version,
                    "available": True,
                    "path": candidate if source == "path" else " ".join(executable),
                    "source": source,
                }
            elif error:
                detections.setdefault(
                    version,
                    {
                        "version": version,
                        "available": False,
                        "path": None,
                        "source": source,
                        "message": error,
                    },
                )

    results: list[dict[str, Any]] = []
    for version in SUPPORTED_PYTHON_VERSIONS:
        results.append(
            detections.get(
                version,
                {
                    "version": version,
                    "available": False,
                    "path": None,
                    "source": None,
                },
            )
        )
    return results




def _module_supported(module: dict[str, Any]) -> bool:
    current = sys.version_info[:2]
    python_min = tuple(module.get("python_min", (0, 0)))
    python_max_exclusive = tuple(module.get("python_max_exclusive", (99, 99)))
    return python_min <= current < python_max_exclusive


def _expected_modules_for_profile(profile: str) -> list[dict[str, Any]]:
    groups = PROFILE_IMPORT_GROUPS.get(profile, PROFILE_IMPORT_GROUPS["base"])
    expected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            if not _module_supported(item):
                continue
            module = str(item["module"])
            if module in seen:
                continue
            seen.add(module)
            expected.append(dict(item))
    return expected


def _probe_modules(expected_modules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not expected_modules:
        return []
    code = (
        "import importlib, json, sys\n"
        "if sys.version_info < (3, 11):\n"
        "    try:\n"
        "        import tomllib  # noqa: F401\n"
        "    except ModuleNotFoundError:\n"
        "        import tomli as tomllib\n"
        "        sys.modules['tomllib'] = tomllib\n"
        "payload = json.loads(sys.argv[1])\n"
        "results = []\n"
        "for item in payload:\n"
        "    try:\n"
        "        importlib.import_module(item['module'])\n"
        "        results.append({'module': item['module'], 'package': item['package'], 'passed': True, 'category': item['category'], 'message': 'import ok', 'error_type': None})\n"
        "    except Exception as exc:\n"
        "        results.append({'module': item['module'], 'package': item['package'], 'passed': False, 'category': item['category'], 'message': str(exc), 'error_type': exc.__class__.__name__})\n"
        "print(json.dumps(results))\n"
    )
    completed = subprocess.run(
        [sys.executable, "-I", "-c", code, json.dumps(expected_modules)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        message = (completed.stderr or completed.stdout or "subprocess probe failed").strip()
        return [
            ModuleProbeResult(
                module=str(item["module"]),
                package=str(item["package"]),
                category=str(item["category"]),
                passed=False,
                message=message,
                error_type="SubprocessProbeFailure",
            ).as_dict()
            for item in expected_modules
        ]
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return [
            ModuleProbeResult(
                module=str(item["module"]),
                package=str(item["package"]),
                category=str(item["category"]),
                passed=False,
                message="invalid module probe payload",
                error_type="JSONDecodeError",
            ).as_dict()
            for item in expected_modules
        ]
    return payload


def _runtime_surface_probe(repo_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for module in RUNTIME_IMPORT_SURFACES:
        module_path = repo_root.joinpath(*module.split(".")).with_suffix(".py")
        package_path = repo_root.joinpath(*module.split("."), "__init__.py")
        passed = module_path.exists() or package_path.exists()
        results.append(
            {
                "module": module,
                "passed": passed,
                "message": "import surface resolvable" if passed else "module source missing",
            }
        )
    return results


def build_install_substrate_report(
    repo_root: Path,
    *,
    profile: str | None = None,
    execute_import_probes: bool = True,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    current_profile = profile or "base"
    environment_identity = current_environment_identity(install_profile=current_profile, repo_root=repo_root)
    detected_pythons = _detect_supported_pythons()
    dependency_manifest = _pyproject_dependency_manifest(repo_root)
    constraint_consistency = _constraint_consistency(repo_root, dependency_manifest)
    dependency_lock_consistency = _dependency_lock_consistency(repo_root, dependency_manifest)
    tox_parser, tox_text = _read_tox(repo_root)
    tox_envlist = _extract_tox_envlist(tox_parser)
    tox_checks = _tox_section_checks(tox_text)
    tox_checks["envlist"] = tox_envlist
    workflow = _build_workflow_coverage(repo_root)

    static_failures: list[str] = []
    if dependency_manifest["workspace_sources_present"]:
        static_failures.append("pyproject.toml still declares workspace-only dependency sources")
    if dependency_manifest["forbidden_dependency_references"]:
        static_failures.append("One or more dependency declarations still use forbidden local/editable sources")
    static_failures.extend(constraint_consistency["mismatches"])
    static_failures.extend(dependency_lock_consistency["failures"])
    if len(tox_envlist) != len(CERTIFICATION_TOX_ENVS):
        static_failures.append("tox envlist does not match the retained certification tox matrix")
    if set(tox_envlist) != set(CERTIFICATION_TOX_ENVS):
        static_failures.append("tox envlist membership drifts from the retained certification tox matrix")
    if not tox_checks["passed"]:
        static_failures.append("tox install-substrate commands are incomplete")
    if not workflow["install_profiles_workflow_passed"]:
        static_failures.append("ci-install-profiles workflow does not cover the full retained runtime matrix")
    if not workflow["release_gates_workflow_passed"]:
        static_failures.append("ci-release-gates workflow does not cover the retained certification lanes and promotion jobs")

    expected_modules = _expected_modules_for_profile(current_profile)
    module_results = _probe_modules(expected_modules) if execute_import_probes else []
    runtime_surface_results = _runtime_surface_probe(repo_root) if execute_import_probes else []
    import_failures = [item for item in module_results if not item.get("passed")]
    runtime_surface_failures = [item for item in runtime_surface_results if not item.get("passed")]

    warnings: list[str] = []
    if not _current_python_supported():
        warnings.append("Current container Python is outside the declared certification support range (>=3.10,<3.13).")
    unavailable_supported = [item["version"] for item in detected_pythons if not item["available"]]
    if unavailable_supported:
        warnings.append(
            f"The current container does not provide supported interpreter binaries for: {', '.join(unavailable_supported)}."
        )

    failures = list(static_failures)
    if not _current_python_supported():
        failures.append("The current environment is outside the declared certification interpreter support range.")
    if unavailable_supported:
        failures.append("The current environment does not provide the full supported interpreter matrix required for clean-room certification.")
    if execute_import_probes and import_failures:
        failures.append("The current environment is missing one or more modules required by the selected install profile.")
    if execute_import_probes and runtime_surface_failures:
        failures.append("One or more runtime import surfaces could not be resolved from the source tree.")

    summary = {
        "static_manifest_passed": not static_failures,
        "passed": not failures,
        "profile": current_profile,
        "current_profile_identity": runtime_identity(current_profile),
        "environment_identity_present": True,
        "current_python": sys.version.split()[0],
        "current_python_supported": _current_python_supported(),
        "expected_supported_python_versions": list(SUPPORTED_PYTHON_VERSIONS),
        "expected_supported_python_count": len(SUPPORTED_PYTHON_VERSIONS),
        "detected_supported_python_count": sum(1 for item in detected_pythons if item["available"]),
        "declared_runtime_matrix_env_count": len(RUNTIME_MATRIX_ENVS),
        "declared_test_lane_env_count": len(TEST_LANE_ENVS),
        "declared_certification_tox_env_count": len(CERTIFICATION_TOX_ENVS),
        "tox_env_count": len(tox_envlist),
        "tox_envs_with_pip_check_count": tox_checks["pip_check_ok_count"],
        "tox_envs_with_install_probe_count": tox_checks["install_probe_ok_count"],
        "tox_section_template_count": tox_checks["section_count"],
        "tox_envs_declare_pip_check": tox_checks["pip_check_ok_count"] == tox_checks["section_count"],
        "tox_envs_declare_install_probe": tox_checks["install_probe_ok_count"] == tox_checks["section_count"],
        "workspace_sources_present": dependency_manifest["workspace_sources_present"],
        "forbidden_dependency_reference_count": len(dependency_manifest["forbidden_dependency_references"]),
        "base_dependency_count": dependency_manifest["dependency_count"],
        "base_exact_pinned_dependency_count": dependency_manifest["exact_pinned_dependency_count"],
        "dependency_lock_manifest_present": (repo_root / "constraints" / "dependency-lock.json").exists(),
        "dependency_lock_install_profile_count": dependency_lock_consistency["install_profile_count"],
        "install_profiles_workflow_present": workflow["install_profiles_workflow_present"],
        "release_gates_workflow_present": workflow["release_gates_workflow_present"],
        "install_profiles_runtime_env_present_count": workflow["install_profiles_runtime_env_present_count"],
        "release_gates_runtime_env_present_count": workflow["release_gates_runtime_env_present_count"],
        "release_gates_test_lane_env_present_count": workflow["release_gates_test_lane_env_present_count"],
        "release_gates_extra_env_present_count": workflow["release_gates_extra_env_present_count"],
        "install_profiles_artifact_upload_present": workflow["install_profiles_artifact_upload_present"],
        "release_gates_artifact_upload_present": workflow["release_gates_artifact_upload_present"],
        "current_profile_expected_module_count": len(expected_modules),
        "current_profile_import_probe_passed_count": sum(1 for item in module_results if item.get("passed")),
        "current_profile_import_probe_failed_count": sum(1 for item in module_results if not item.get("passed")),
        "current_profile_import_probe_passed": not import_failures,
        "runtime_surface_probe_count": len(runtime_surface_results),
        "runtime_surface_probe_failed_count": len(runtime_surface_failures),
        "runtime_surface_probe_passed": not runtime_surface_failures,
    }

    profiles = {
        name: {
            "constraints": list(details["constraints"]),
            "extras": list(details["extras"]),
            "expected_modules": [item["module"] for item in _expected_modules_for_profile(name)],
        }
        for name, details in PROFILE_TOGGLES.items()
    }

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "passed": not failures,
        "summary": summary,
        "failures": failures,
        "warnings": warnings,
        "detected_supported_pythons": detected_pythons,
        "dependency_manifest": dependency_manifest,
        "constraints_consistency": constraint_consistency,
        "dependency_lock_consistency": dependency_lock_consistency,
        "tox": tox_checks,
        "workflow": workflow,
        "profiles": profiles,
        "identity": runtime_identity(current_profile),
        "environment_identity": environment_identity,
        "current_environment_probe": {
            "profile": current_profile,
            "identity": runtime_identity(current_profile),
            "environment_identity": environment_identity,
            "python": sys.version.split()[0],
            "python_supported": _current_python_supported(),
            "module_results": module_results,
            "runtime_surface_results": runtime_surface_results,
        },
    }


def write_install_substrate_report(
    repo_root: Path,
    *,
    profile: str | None = None,
    report_dir: Path | None = None,
    artifact_dir: Path | None = None,
    execute_import_probes: bool = True,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)
    payload = build_install_substrate_report(repo_root, profile=profile, execute_import_probes=execute_import_probes)
    payload = sanitize_local_paths(payload, repo_root)
    json_path = report_dir / "install_substrate_report.json"
    md_path = report_dir / "install_substrate_report.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Install Substrate Report",
        "",
        f"- Generated at: `{payload.get('generated_at')}`",
        f"- Passed: `{payload.get('passed')}`",
        f"- Static manifest passed: `{payload['summary']['static_manifest_passed']}`",
        f"- Profile: `{payload['summary']['profile']}`",
        f"- Profile identity: `{payload['summary']['current_profile_identity']}`",
        f"- Environment identity present: `{payload['summary']['environment_identity_present']}`",
        f"- Current Python: `{payload['summary']['current_python']}`",
        f"- Current Python supported: `{payload['summary']['current_python_supported']}`",
        f"- Expected supported Python versions: `{', '.join(payload['summary']['expected_supported_python_versions'])}`",
        f"- Detected supported Python binaries: `{payload['summary']['detected_supported_python_count']}` / `{payload['summary']['expected_supported_python_count']}`",
        f"- Certification tox envs declared: `{payload['summary']['declared_certification_tox_env_count']}`",
        f"- Runtime matrix envs declared: `{payload['summary']['declared_runtime_matrix_env_count']}`",
        f"- Test lane envs declared: `{payload['summary']['declared_test_lane_env_count']}`",
        f"- Tox templates with pip check: `{payload['summary']['tox_envs_with_pip_check_count']}` / `{payload['summary']['tox_section_template_count']}`",
        f"- Tox templates with install probe: `{payload['summary']['tox_envs_with_install_probe_count']}` / `{payload['summary']['tox_section_template_count']}`",
        f"- Current profile import probe passed: `{payload['summary']['current_profile_import_probe_passed']}`",
        f"- Runtime surface probe passed: `{payload['summary']['runtime_surface_probe_passed']}`",
        "",
    ]
    if payload.get("failures"):
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in payload["failures"]])
        lines.append("")
    if payload.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend([f"- {item}" for item in payload["warnings"]])
        lines.append("")
    lines.extend(["## Current environment import probe", ""])
    for item in payload.get("current_environment_probe", {}).get("module_results", []):
        lines.append(f"- `{item['module']}` ({item['package']}) → passed=`{item['passed']}` message=`{item['message']}`")
    lines.append("")
    lines.extend(["## Runtime import surfaces", ""])
    for item in payload.get("current_environment_probe", {}).get("runtime_surface_results", []):
        lines.append(f"- `{item['module']}` → passed=`{item['passed']}` message=`{item['message']}`")
    lines.append("")
    lines.extend(["## Detected supported interpreters", ""])
    for item in payload.get("detected_supported_pythons", []):
        lines.append(f"- `{item['version']}` → available=`{item['available']}` path=`{item['path']}`")
    lines.append("")
    workflow = payload.get("workflow", {})
    lines.extend(
        [
            "## Workflow coverage",
            "",
            f"- install_profiles_workflow_present: `{workflow.get('install_profiles_workflow_present')}`",
            f"- release_gates_workflow_present: `{workflow.get('release_gates_workflow_present')}`",
            f"- install_profiles_runtime_env_present_count: `{workflow.get('install_profiles_runtime_env_present_count')}`",
            f"- release_gates_runtime_env_present_count: `{workflow.get('release_gates_runtime_env_present_count')}`",
            f"- release_gates_test_lane_env_present_count: `{workflow.get('release_gates_test_lane_env_present_count')}`",
            f"- release_gates_extra_env_present_count: `{workflow.get('release_gates_extra_env_present_count')}`",
            f"- install_profiles_artifact_upload_present: `{workflow.get('install_profiles_artifact_upload_present')}`",
            f"- release_gates_artifact_upload_present: `{workflow.get('release_gates_artifact_upload_present')}`",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    if artifact_dir is not None:
        artifact_dir = artifact_dir.resolve()
        artifact_dir.mkdir(parents=True, exist_ok=True)
        profile_name = payload["summary"]["profile"]
        (artifact_dir / f"{profile_name}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


__all__ = [
    "CERTIFICATION_TOX_ENVS",
    "PROFILE_TOGGLES",
    "RUNTIME_MATRIX_ENVS",
    "TEST_LANE_ENVS",
    "SUPPORTED_PYTHON_VERSIONS",
    "build_install_substrate_report",
    "write_install_substrate_report",
]
