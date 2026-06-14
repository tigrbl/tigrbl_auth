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

from tigrbl_identity_cli.cli.certification_evidence import current_environment_identity, runtime_identity
from tigrbl_identity_core.path_safety import sanitize_local_paths
from tigrbl_identity_operator.repo_truth import has_install_matrix_workflow, has_release_gate_workflow, workflow_role_text

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]

SUPPORTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12", "3.13", "3.14")
_SUPPORTED_PYTHON_TAGS = tuple(version.replace(".", "") for version in SUPPORTED_PYTHON_VERSIONS)
_TIGRCORN_PYTHON_TAGS = tuple(version.replace(".", "") for version in SUPPORTED_PYTHON_VERSIONS if version != "3.10")
RUNTIME_MATRIX_ENVS = (
    *(f"py{tag}-base" for tag in _SUPPORTED_PYTHON_TAGS),
    *(f"py{tag}-sqlite-uvicorn" for tag in _SUPPORTED_PYTHON_TAGS),
    *(f"py{tag}-postgres-hypercorn" for tag in _SUPPORTED_PYTHON_TAGS),
    *(f"py{tag}-tigrcorn" for tag in _TIGRCORN_PYTHON_TAGS),
    *(f"py{tag}-devtest" for tag in _SUPPORTED_PYTHON_TAGS),
)
TEST_LANE_ENVS = tuple(
    f"py{tag}-test-{lane}"
    for lane in ("core", "integration", "conformance", "security-negative", "interop")
    for tag in _SUPPORTED_PYTHON_TAGS
)
ADDITIONAL_CERTIFICATION_ENVS = (
    "py311-gates",
    "py311-test-extension",
    "py311-migration-portability",
    "py311-final-certification",
)
CERTIFICATION_TOX_ENVS = RUNTIME_MATRIX_ENVS + TEST_LANE_ENVS + ADDITIONAL_CERTIFICATION_ENVS
RUNTIME_IMPORT_SURFACES = (
    "tigrbl_identity_server.api.app",
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
        "python_max_exclusive": (3, 15),
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
    "[testenv:py{310,311,312,313,314}-sqlite-uvicorn]": "sqlite-uvicorn",
    "[testenv:py{310,311,312,313,314}-postgres-hypercorn]": "postgres-hypercorn",
    "[testenv:py{311,312,313,314}-tigrcorn]": "tigrcorn",
    "[testenv:py{310,311,312,313,314}-devtest]": "devtest",
    "[testenv:py311-gates]": "release-gates",
    "[testenv:py{310,311,312,313,314}-test-core]": "test-core",
    "[testenv:py{310,311,312,313,314}-test-integration]": "test-integration",
    "[testenv:py{310,311,312,313,314}-test-conformance]": "test-conformance",
    "[testenv:py{310,311,312,313,314}-test-security-negative]": "test-security-negative",
    "[testenv:py{310,311,312,313,314}-test-interop]": "test-interop",
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
