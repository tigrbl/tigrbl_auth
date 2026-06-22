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
from tigrbl_identity_cli.cli.install_substrate._profiles import (
    CERTIFICATION_TOX_ENVS,
    INSTALL_WORKFLOW_RUNTIME_ENVS,
    PROFILE_IMPORT_GROUPS,
    PROFILE_TOGGLES,
    RELEASE_WORKFLOW_EXTRA_ENVS,
    RELEASE_WORKFLOW_RUNTIME_ENVS,
    RELEASE_WORKFLOW_TEST_LANE_ENVS,
    RUNTIME_IMPORT_SURFACES,
    RUNTIME_MATRIX_ENVS,
    SUPPORTED_PYTHON_VERSIONS,
    TEST_LANE_ENVS,
    TOX_PROFILE_SECTION_EXPECTATIONS,
)

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]

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


def _load_pyproject(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "pyproject.toml"
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _requirements_have_forbidden_sources(requirements: list[str]) -> list[str]:
    hits: list[str] = []
    for item in requirements:
        normalized = _normalize_requirement(item)
        if any(pattern in normalized for pattern in REQUIREMENT_FORBIDDEN_PATTERNS):
            hits.append(normalized)
    return hits


def _classify_uv_sources(
    repo_root: Path, sources: dict[str, Any]
) -> tuple[dict[str, str], dict[str, str]]:
    repo_root = repo_root.resolve()
    allowed: dict[str, str] = {}
    forbidden: dict[str, str] = {}
    for name, value in sources.items():
        if not isinstance(value, dict):
            forbidden[str(name)] = "non-table source"
            continue
        raw_path = value.get("path")
        if not raw_path:
            forbidden[str(name)] = "non-path source"
            continue
        source_path = Path(str(raw_path))
        resolved = (source_path if source_path.is_absolute() else repo_root / source_path).resolve()
        try:
            rel_path = resolved.relative_to(repo_root)
        except ValueError:
            forbidden[str(name)] = str(raw_path)
            continue
        rel = rel_path.as_posix()
        if rel.startswith("pkgs/") and (resolved / "pyproject.toml").is_file():
            allowed[str(name)] = rel
            continue
        forbidden[str(name)] = rel
    return allowed, forbidden


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


def _block_declares_extra(block: str, extra: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(extra)}\s*$", block, flags=re.MULTILINE))


def _tox_section_checks(text: str) -> dict[str, Any]:
    section_results: dict[str, dict[str, Any]] = {}
    pip_check_ok_count = 0
    install_probe_ok_count = 0
    for header, profile in TOX_PROFILE_SECTION_EXPECTATIONS.items():
        block = _section_block(text, header)
        pip_check_present = "python -I -m pip check" in block
        install_probe_present = "scripts/verify_clean_room_install_substrate.py" in block
        profile_present = f"TIGRBL_AUTH_INSTALL_PROFILE = {profile}" in block
        extras = PROFILE_TOGGLES.get(profile, {}).get("extras", [])
        extras_present = all(
            _block_declares_extra(block, str(extra)) or header == "[testenv]"
            for extra in extras
        )
        section_results[header] = {
            "profile": profile,
            "pip_check_present": pip_check_present,
            "install_probe_present": install_probe_present,
            "install_profile_variable_present": profile_present,
            "extras_present": extras_present,
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
            and item["extras_present"]
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
    allowed_workspace_sources, forbidden_workspace_sources = _classify_uv_sources(
        repo_root, workspace_sources
    )
    forbidden = _requirements_have_forbidden_sources(dependencies)
    for values in optional.values():
        forbidden.extend(_requirements_have_forbidden_sources(values))
    return {
        "requires_python": str(project.get("requires-python", "")),
        "dependencies": dependencies,
        "optional_dependencies": optional,
        "workspace_sources_present": bool(forbidden_workspace_sources),
        "workspace_sources_declared": bool(workspace_sources),
        "first_party_workspace_source_count": len(allowed_workspace_sources),
        "forbidden_workspace_source_count": len(forbidden_workspace_sources),
        "forbidden_workspace_sources": forbidden_workspace_sources,
        "forbidden_dependency_references": sorted(set(forbidden)),
        "exact_pinned_dependency_count": sum(1 for item in dependencies if _is_exact_pin(item)),
        "dependency_count": len(dependencies),
    }
