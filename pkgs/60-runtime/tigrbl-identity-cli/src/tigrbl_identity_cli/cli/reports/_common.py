"""Contracts, evidence, release, signing, and reporting automation."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    tomllib = None
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml

from tigrbl_identity_cli.cli.artifacts import (
    build_discovery_artifacts,
    build_effective_claims_manifest,
    build_effective_evidence_manifest,
    build_openapi_contract,
    build_openrpc_contract,
    deployment_from_options,
    write_discovery_artifacts,
    write_effective_claims_manifest,
    write_effective_evidence_manifest,
    write_openapi_contract,
    write_openrpc_contract,
)
from tigrbl_identity_cli.cli.boundary import (
    run_boundary_enforcement_check,
    run_contract_sync_check,
    run_evidence_peer_check,
    run_wrapper_hygiene_check,
    validate_scope_freeze_metadata,
)
from tigrbl_identity_cli.cli.certification_evidence import (
    environment_identity_ready,
    install_evidence_ready,
    validated_migration_backend_manifest_passed,
    validated_migration_manifest_passed,
    validated_runtime_manifest_passed,
    validated_test_lane_manifest_passed,
)
from tigrbl_identity_cli.cli.claims import run_lint
from tigrbl_identity_cli.cli.claim_registry import verify_claim_registries
from tigrbl_identity_cli.cli.feature_surface import run_feature_surface_modularity_check
from tigrbl_identity_cli.cli.governance import run_governance_install_check
from tigrbl_identity_cli.cli.metadata import (
    build_cli_conformance_snapshot,
    build_cli_contract_manifest,
    render_cli_conformance_markdown,
    render_cli_markdown,
)
from tigrbl_identity_cli.cli.reports._document_authority_helpers import (
    DERIVED_CURRENT_DOCS,
    _docs_for_certification_bundle,
    write_authoritative_current_docs_manifest,
)
from tigrbl_identity_cli.cli.install_substrate import write_install_substrate_report
from tigrbl_identity_cli.cli.project_tree import run_migration_plan_check, run_project_tree_layout_check
from tigrbl_identity_cli.cli.runtime import run_runtime_foundation_check, write_runtime_profile_report
from tigrbl_identity_cli.cli.truth import materialize_truth_chain, verify_truth_chain
from tigrbl_identity_runtime.deployment import ROUTE_REGISTRY
from tigrbl_identity_operator.document_authority import (
    DEFAULT_GENERATED_CURRENT_STATE_DOCS,
    load_document_authority,
    render_document_authority_projection,
)
from tigrbl_identity_core.path_safety import sanitize_local_paths
from tigrbl_identity_operator.repo_truth import (
    evaluate_tier4_bundle,
    has_install_matrix_workflow,
    has_release_gate_workflow,
    package_version,
    workflow_paths,
)
from tigrbl_identity_cli.package_maturity import evaluate_package_maturity
from tigrbl_identity_runtime import build_runtime_hash_matrix, registered_runner_names, runner_registry_manifest
from tigrbl_identity_storage_runtime.operator_store import OperationContext, operator_state_root, operator_store_summary
from tigrbl_auth_protocol_oidc.discovery_service import diff_discovery, publish_discovery, validate_discovery
from tigrbl_identity_storage_runtime.resource_service import (
    create_resource,
    delete_resource,
    generate_key_record,
    get_resource,
    list_resource_result,
    operator_plane_status,
    publish_jwks_document,
    retire_key_record,
    rotate_key_record,
    run_export,
    run_import,
    update_resource,
    validate_import_artifact,
)
from tigrbl_identity_author.release_signing import (
    build_contract_set_manifest,
    load_signer,
    verify_bundle_attestations,
    write_artifact_attestation,
    write_bundle_attestation,
    write_public_key_artifacts,
)


@dataclass(slots=True)
class ContractReport:
    kind: str
    path: Path
    passed: bool
    failures: list[str]
    warnings: list[str]
    summary: dict[str, Any]


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _current_version(repo_root: Path) -> str:
    return package_version(repo_root)


def _load_pyproject_manifest(repo_root: Path) -> dict[str, Any]:
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.exists() or tomllib is None:
        return {}
    return tomllib.loads(pyproject.read_text(encoding="utf-8"))


def _is_exact_pin(specifier: str) -> bool:
    cleaned = specifier.strip()
    return "==" in cleaned and all(token not in cleaned for token in (">=", "<=", "~=", "!=", " @ "))


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


def _dependency_artifact_paths(repo_root: Path) -> list[str]:
    candidates = [
        "pyproject.toml",
        "pkgs/60-runtime/tigrbl-identity-runtime/pyproject.toml",
        "uv.lock",
        "docker/Dockerfile",
        "tox.ini",
        "docs/runbooks/INSTALLATION_PROFILES.md",
        "docs/runbooks/CLEAN_CHECKOUT_REPRO.md",
        ".github/workflows/ci-install-profiles.yml",
        ".github/workflows/ci-release-gates.yml",
        "scripts/verify_clean_room_install_substrate.py",
        "scripts/run_certification_lane.py",
    ]
    return sorted({*workflow_paths(repo_root), *(rel for rel in candidates if (repo_root / rel).exists())})


def _profile_deployment(profile_label: str) -> Any:
    if profile_label == "active":
        return deployment_from_options()
    return deployment_from_options(profile=profile_label)


def _openapi_path(repo_root: Path, profile_label: str) -> Path:
    if profile_label == "active":
        return repo_root / "specs" / "openapi" / "tigrbl_auth.public.openapi.json"
    return repo_root / "specs" / "openapi" / "profiles" / profile_label / "tigrbl_auth.public.openapi.json"


def _openrpc_path(repo_root: Path, profile_label: str) -> Path:
    if profile_label == "active":
        return repo_root / "specs" / "openrpc" / "tigrbl_auth.admin.openrpc.json"
    return repo_root / "specs" / "openrpc" / "profiles" / profile_label / "tigrbl_auth.admin.openrpc.json"


def _hash_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _hash_file(path: Path) -> str:
    return _hash_bytes(path.read_bytes())


def _write_report(report_dir: Path, stem: str, payload: dict[str, Any], title: str) -> None:
    if report_dir.name == "compliance" and report_dir.parent.name == "docs":
        payload = sanitize_local_paths(payload, report_dir.parent.parent)
    _write_json(report_dir / f"{stem}.json", payload)
    lines = [f"# {title}", "", f"- Passed: `{payload.get('passed', False)}`", ""]
    if payload.get("summary"):
        lines.extend(["## Summary", ""])
        for key, value in payload["summary"].items():
            lines.append(f"- {key}: `{value}`")
        lines.append("")
    if payload.get("failures"):
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in payload["failures"]])
        lines.append("")
    if payload.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend([f"- {item}" for item in payload["warnings"]])
        lines.append("")
    if payload.get("details"):
        lines.extend(["## Details", ""])
        details = payload["details"]
        if isinstance(details, dict):
            for key, value in details.items():
                lines.append(f"- {key}: `{value}`")
        else:
            lines.extend([f"- {item}" for item in details])
        lines.append("")
    (report_dir / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")



def build_adr_index(repo_root: Path) -> dict[str, Any]:
    adr_dir = repo_root / "docs" / "adr"
    entries: list[dict[str, str]] = []
    for path in sorted(adr_dir.glob("ADR-*.md")):
        title = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        entries.append({"id": path.stem, "path": str(path.relative_to(repo_root)), "title": title or path.stem})
    payload = {"count": len(entries), "entries": entries}
    index_md = ["# ADR Index", ""]
    for entry in entries:
        index_md.append(f"- `{entry['id']}` — {entry['title']} ({entry['path']})")
    index_md.append("")
    (adr_dir / "INDEX.md").write_text("\n".join(index_md), encoding="utf-8")
    _write_json(adr_dir / "index.json", payload)
    return payload


def validate_openapi_contract(repo_root: Path, profile_label: str = "active") -> ContractReport:
    repo_root = repo_root.resolve()
    deployment = _profile_deployment(profile_label)
    path = _openapi_path(repo_root, profile_label)
    failures: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        failures.append(f"Missing contract: {path.relative_to(repo_root)}")
        return ContractReport("openapi", path, False, failures, warnings, {})
    contract = json.loads(path.read_text(encoding="utf-8"))
    version = str(contract.get("openapi", ""))
    if not version.startswith("3."):
        failures.append(f"Unexpected OpenAPI version: {version}")
    if not contract.get("info", {}).get("title"):
        failures.append("Missing OpenAPI info.title")
    if not contract.get("paths"):
        failures.append("OpenAPI contract has no paths")
    expected_routes = [route for route in deployment.active_routes if route != "/system/health"]
    missing_routes = [route for route in expected_routes if route not in contract.get("paths", {})]
    if missing_routes:
        failures.append("Missing active public routes in OpenAPI contract: " + ", ".join(missing_routes))
    xmeta = contract.get("x-tigrbl-auth", {})
    if xmeta.get("profile") != deployment.profile:
        failures.append("OpenAPI x-tigrbl-auth profile does not match deployment profile")
    security = contract.get("components", {}).get("securitySchemes", {})
    if deployment.flag_enabled("enable_rfc6750") and "bearerAuth" not in security:
        failures.append("Missing bearerAuth security scheme")
    if deployment.flag_enabled("enable_rfc6749") and "oauth2" not in security:
        failures.append("Missing oauth2 security scheme")
    if deployment.flag_enabled("enable_oidc_discovery") and "openIdConnect" not in security:
        failures.append("Missing openIdConnect security scheme")
    summary = {
        "profile": deployment.profile,
        "path_count": len(contract.get("paths", {})),
        "expected_route_count": len(expected_routes),
        "security_scheme_count": len(security),
        "version": version,
    }
    return ContractReport("openapi", path, not failures, failures, warnings, summary)


def validate_openrpc_contract(repo_root: Path, profile_label: str = "active") -> ContractReport:
    repo_root = repo_root.resolve()
    deployment = _profile_deployment(profile_label)
    path = _openrpc_path(repo_root, profile_label)
    failures: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        failures.append(f"Missing contract: {path.relative_to(repo_root)}")
        return ContractReport("openrpc", path, False, failures, warnings, {})
    contract = json.loads(path.read_text(encoding="utf-8"))
    version = str(contract.get("openrpc", ""))
    if not version.startswith("1."):
        failures.append(f"Unexpected OpenRPC version: {version}")
    methods = contract.get("methods", [])
    method_names = {str(item.get("name")) for item in methods}
    expected_method_names: set[str] = set()
    if method_names != expected_method_names:
        failures.append(
            "OpenRPC contract method set does not match implementation-backed registry: "
            + f"expected={sorted(expected_method_names)} actual={sorted(method_names)}"
        )
    components = contract.get("components", {}).get("schemas", {})
    for item in methods:
        owner = str(item.get("x-tigrbl-auth", {}).get("owner_module", ""))
        if not owner:
            failures.append(f"OpenRPC method missing owner-module metadata: {item.get('name')}")
            continue
        if not (repo_root / owner).exists():
            failures.append(f"OpenRPC method owner-module path does not exist: {owner}")
    summary = {
        "profile": deployment.profile,
        "method_count": len(methods),
        "expected_method_count": len(expected_method_names),
        "schema_count": len(components),
        "version": version,
        "admin_rpc_enabled": False,
    }
    return ContractReport("openrpc", path, not failures, failures, warnings, summary)
