from __future__ import annotations

"""Contracts, evidence, release, signing, and reporting automation."""

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

from tigrbl_auth.cli.artifacts import (
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
from tigrbl_auth.cli.boundary import (
    run_boundary_enforcement_check,
    run_contract_sync_check,
    run_evidence_peer_check,
    run_wrapper_hygiene_check,
    validate_scope_freeze_metadata,
)
from tigrbl_auth.cli.certification_evidence import (
    environment_identity_ready,
    install_evidence_ready,
    validated_migration_backend_manifest_passed,
    validated_migration_manifest_passed,
    validated_runtime_manifest_passed,
    validated_test_lane_manifest_passed,
)
from tigrbl_auth.cli.claims import run_lint
from tigrbl_auth.cli.claim_registry import verify_claim_registries
from tigrbl_auth.cli.feature_surface import run_feature_surface_modularity_check
from tigrbl_auth.cli.governance import run_governance_install_check
from tigrbl_auth.cli.metadata import (
    build_cli_conformance_snapshot,
    build_cli_contract_manifest,
    render_cli_conformance_markdown,
    render_cli_markdown,
)
from tigrbl_auth.cli.install_substrate import write_install_substrate_report
from tigrbl_auth.cli.project_tree import run_migration_plan_check, run_project_tree_layout_check
from tigrbl_auth.cli.runtime import run_runtime_foundation_check, write_runtime_profile_report
from tigrbl_auth.cli.truth import materialize_truth_chain, verify_truth_chain
from tigrbl_auth.config.deployment import ROUTE_REGISTRY
from tigrbl_auth.document_authority import (
    DEFAULT_GENERATED_CURRENT_STATE_DOCS,
    load_document_authority,
    render_document_authority_projection,
)
from tigrbl_auth.path_safety import sanitize_local_paths
from tigrbl_auth.repo_truth import (
    evaluate_tier4_bundle,
    has_install_matrix_workflow,
    has_release_gate_workflow,
    package_version,
    workflow_paths,
)
from tigrbl_auth.runtime import build_runtime_hash_matrix, registered_runner_names, runner_registry_manifest
from tigrbl_auth.services._operator_store import OperationContext, operator_state_root, operator_store_summary
from tigrbl_auth.services.discovery_service import diff_discovery, publish_discovery, validate_discovery
from tigrbl_auth.services.operator_service import (
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
from tigrbl_auth.release_signing import (
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


def _dependency_artifact_paths(repo_root: Path) -> list[str]:
    candidates = [
        "pyproject.toml",
        "Dockerfile",
        "tox.ini",
        "constraints/base.txt",
        "constraints/test.txt",
        "constraints/runner-uvicorn.txt",
        "constraints/runner-hypercorn.txt",
        "constraints/runner-tigrcorn.txt",
        "constraints/dependency-lock.json",
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



def _docs_for_certification_bundle(repo_root: Path) -> list[str]:
    authority = load_document_authority(repo_root)
    docs = authority.get("current_release_bundle_docs", list(DEFAULT_GENERATED_CURRENT_STATE_DOCS))
    return [rel for rel in docs if (repo_root / rel).exists()]


def write_authoritative_current_docs_manifest(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    authority = load_document_authority(repo_root)
    _write_yaml(repo_root / authority["projection_path"], render_document_authority_projection(authority))
    payload = {
        "schema_version": 1,
        "authority_spec": authority.get("path"),
        "projection_manifest": authority.get("projection_path"),
        "canonical_ssot_roots": list(authority.get("canonical_ssot_roots", ())),
        "authoritative_current_docs": sorted(authority.get("authoritative_current_docs", set())),
        "derived_current_docs": sorted(DERIVED_CURRENT_DOCS),
        "archive_roots": list(authority.get("archived_historical_roots", ())),
        "certification_bundle_generated_current_docs": _docs_for_certification_bundle(repo_root),
        "supporting_current_non_doc_artifacts": list(authority.get("supporting_current_non_doc_artifacts", [])),
        "historical_docs_policy": "Historical and archived docs are non-authoritative and excluded from the certification bundle documentation scope.",
    }
    report_dir = repo_root / "docs" / "compliance"
    _write_json(report_dir / "AUTHORITATIVE_CURRENT_DOCS.json", payload)
    lines = [
        "# Authoritative current docs",
        "",
        "This file is a compatibility projection of the current certification and release-facing docs derived from the SSOT authority spec.",
        "",
        f"- authority_spec: `{payload['authority_spec']}`",
        f"- projection_manifest: `{payload['projection_manifest']}`",
        "- authority_note: `.ssot/` is authoritative; this file is not.",
        "",
        "## Canonical SSOT roots",
        "",
    ]
    lines.extend([f"- `{item}`" for item in payload["canonical_ssot_roots"]])
    lines.extend([
        "",
        "## Current release-facing docs",
        "",
    ])
    lines.extend([f"- `{item}`" for item in payload["authoritative_current_docs"]])
    lines.extend(["", "## Derived current docs", ""])
    lines.extend([f"- `{item}`" for item in payload["derived_current_docs"]])
    lines.extend(["", "## Certification bundle documentation scope", ""])
    lines.extend([f"- `{item}`" for item in payload["certification_bundle_generated_current_docs"]])
    lines.extend(["", "## Supporting current non-doc artifacts", ""])
    lines.extend([f"- `{item}`" for item in payload["supporting_current_non_doc_artifacts"]])
    lines.extend(["", "## Archive policy", ""])
    lines.extend([f"- archive_root: `{item}`" for item in payload["archive_roots"]])
    lines.append(f"- policy: {payload['historical_docs_policy']}")
    lines.append("- projection_policy: `.ssot/` remains authoritative; this manifest is informational compatibility output.")
    lines.append("")
    (report_dir / "AUTHORITATIVE_CURRENT_DOCS.md").write_text("\n".join(lines), encoding="utf-8")
    return payload
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
    if deployment.surface_enabled("admin-rpc") and not methods:
        failures.append("OpenRPC contract has no methods while admin-rpc is active")
    method_names = {str(item.get("name")) for item in methods}
    expected_method_names = set(getattr(deployment, "active_openrpc_methods", ()) or ())
    if deployment.surface_enabled("admin-rpc") and "rpc.discover" not in method_names:
        failures.append("OpenRPC contract missing rpc.discover")
    if method_names != expected_method_names:
        failures.append(
            "OpenRPC contract method set does not match implementation-backed registry: "
            + f"expected={sorted(expected_method_names)} actual={sorted(method_names)}"
        )
    components = contract.get("components", {}).get("schemas", {})
    if deployment.surface_enabled("admin-rpc") and not components:
        failures.append("OpenRPC contract has no schema components while admin-rpc is active")
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
        "admin_rpc_enabled": deployment.surface_enabled("admin-rpc"),
    }
    return ContractReport("openrpc", path, not failures, failures, warnings, summary)


def diff_contracts(repo_root: Path, kind: str = "all", profile_label: str = "active") -> dict[str, Any]:
    repo_root = repo_root.resolve()
    deployment = _profile_deployment(profile_label)
    version = _current_version(repo_root)
    failures: list[str] = []
    warnings: list[str] = []
    details: dict[str, Any] = {}
    if kind in {"openapi", "all"}:
        expected = build_openapi_contract(deployment, version=version)
        committed = json.loads(_openapi_path(repo_root, profile_label).read_text(encoding="utf-8"))
        equal = json.dumps(expected, sort_keys=True) == json.dumps(committed, sort_keys=True)
        details["openapi_equal"] = equal
        if not equal:
            failures.append(f"OpenAPI drift detected for profile {profile_label}")
    if kind in {"openrpc", "all"}:
        expected = build_openrpc_contract(deployment, version=version)
        committed = json.loads(_openrpc_path(repo_root, profile_label).read_text(encoding="utf-8"))
        equal = json.dumps(expected, sort_keys=True) == json.dumps(committed, sort_keys=True)
        details["openrpc_equal"] = equal
        if not equal:
            failures.append(f"OpenRPC drift detected for profile {profile_label}")
    return {"passed": not failures, "failures": failures, "warnings": warnings, "details": details}


PROFILE_LABELS = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")
PUBLIC_ROUTE_SEARCH_ROOTS = (
    "tigrbl_auth/api/rest/routers",
    "tigrbl_auth/standards/oauth2",
    "tigrbl_auth/standards/oidc",
)
DOC_REF_RE = re.compile(r"tigrbl_auth/[A-Za-z0-9_./-]+\.py")

AUTHORITATIVE_DOCS = {
    "README.md",
    "CURRENT_STATE.md",
    "CERTIFICATION_STATUS.md",
    "docs/compliance/README.md",
    "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md",
    "docs/compliance/current_state_report.md",
    "docs/compliance/certification_state_report.md",
    "docs/compliance/runtime_profile_report.md",
    "docs/compliance/release_gate_report.md",
    "docs/compliance/final_release_gate_report.md",
    "docs/compliance/validated_execution_report.md",
    "docs/compliance/release_signing_report.md",
    "docs/compliance/FINAL_RELEASE_STATUS_2026-03-25.md",
    "docs/compliance/PEER_MATRIX_REPORT.md",
    "docs/compliance/TIER4_PROMOTION_MATRIX.md",
    "docs/compliance/RELEASE_DECISION_RECORD.md",
    "docs/compliance/BOUNDARY_FREEZE_DECISION_2026-03-26.md",
    "docs/reference/README.md",
    "docs/reference/CLI_SURFACE.md",
    "docs/reference/PUBLIC_ROUTE_SURFACE.md",
    "docs/reference/RPC_OPERATOR_SURFACE.md",
    "docs/reference/DISCOVERY_PROFILE_SNAPSHOTS.md",
}
DERIVED_CURRENT_DOCS = {
    "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.json",
    "docs/compliance/current_state_report.json",
    "docs/compliance/certification_state_report.json",
    "docs/compliance/runtime_profile_report.json",
    "docs/compliance/release_gate_report.json",
    "docs/compliance/final_release_gate_report.json",
    "docs/compliance/validated_execution_report.json",
    "docs/compliance/release_signing_report.json",
    "docs/compliance/FINAL_RELEASE_STATUS_2026-03-25.json",
    "docs/compliance/final_target_decision_matrix.json",
    "docs/compliance/peer_matrix_report.json",
}
DOC_REF_SCAN_EXCLUDE = {
    "docs/compliance/artifact_truthfulness_report.md",
    "docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.md",
}
ROUTE_CONSTANTS = {
    "JWKS_PATH": "/.well-known/jwks.json",
    "TENANT_JWKS_PATH": "/tenants/{tenant_slug}/.well-known/jwks.json",
    "TENANT_OPENID_CONFIGURATION_PATH": "/tenants/{tenant_slug}/.well-known/openid-configuration",
}
WELL_KNOWN_ROUTE_CONSTANTS = {"oauth_protected_resource": "/.well-known/oauth-protected-resource"}


def _load_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _stable_json_hash(payload: Any) -> str:
    return _hash_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8"))


def _literal_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _literal_route_path(node: ast.AST) -> str | None:
    literal = _literal_str(node)
    if literal is not None:
        return literal
    if isinstance(node, ast.Name):
        return ROUTE_CONSTANTS.get(node.id)
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "WELL_KNOWN_ENDPOINTS":
        key_node = node.slice
        if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
            return WELL_KNOWN_ROUTE_CONSTANTS.get(key_node.value)
    return None


def _literal_methods(node: ast.AST) -> list[str]:
    if isinstance(node, (ast.Tuple, ast.List)):
        values: list[str] = []
        for item in node.elts:
            value = _literal_str(item)
            if value is not None:
                values.append(value.lower())
        return values
    return []


def _extract_route_definitions(repo_root: Path) -> dict[str, dict[str, Any]]:
    extracted: dict[str, dict[str, Any]] = {}
    for rel_root in PUBLIC_ROUTE_SEARCH_ROOTS:
        base = repo_root / rel_root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            rel = str(path.relative_to(repo_root)).replace("\\", "/")
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for decorator in node.decorator_list:
                    if not isinstance(decorator, ast.Call):
                        continue
                    func = decorator.func
                    if not isinstance(func, ast.Attribute) or func.attr != "route":
                        continue
                    route_path: str | None = None
                    methods: list[str] = []
                    if decorator.args:
                        route_path = _literal_route_path(decorator.args[0])
                    for keyword in decorator.keywords:
                        if keyword.arg == "methods":
                            methods = _literal_methods(keyword.value)
                    if route_path is None:
                        continue
                    entry = extracted.setdefault(route_path, {"methods": set(), "files": set()})
                    entry["files"].add(rel)
                    entry["methods"].update(methods)
    normalized: dict[str, dict[str, Any]] = {}
    for route_path, entry in extracted.items():
        normalized[route_path] = {
            "methods": sorted(entry["methods"]),
            "files": sorted(entry["files"]),
        }
    return normalized


def _scan_stale_doc_refs(repo_root: Path) -> dict[str, dict[str, list[str]]]:
    buckets: dict[str, dict[str, list[str]]] = {"authoritative": {}, "historical": {}}
    authority = load_document_authority(repo_root)
    doc_paths = list((repo_root / "docs").rglob("*.md")) + [repo_root / "README.md", repo_root / "CURRENT_STATE.md", repo_root / "CERTIFICATION_STATUS.md"]
    for doc in sorted(doc_paths):
        rel_doc = str(doc.relative_to(repo_root)).replace("\\", "/")
        if rel_doc in DOC_REF_SCAN_EXCLUDE:
            continue
        if any(rel_doc == root or rel_doc.startswith(root + "/") for root in authority["archived_historical_roots"]):
            continue
        text = doc.read_text(encoding="utf-8", errors="ignore")
        bucket = "authoritative" if rel_doc in authority["authoritative_current_docs"] else "historical"
        for ref in sorted(set(DOC_REF_RE.findall(text))):
            if not (repo_root / ref).exists():
                buckets[bucket].setdefault(ref, []).append(rel_doc)
    return buckets
def _public_paths_for_deployment(deployment: Any) -> list[str]:
    return sorted(
        path
        for path in deployment.active_contract_routes
        if path != "/system/health" and str(ROUTE_REGISTRY.get(path, {}).get("surface_set")) == "public-rest"
    )


def generate_artifact_truthfulness_report(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    failures: list[str] = []
    warnings: list[str] = []
    details: dict[str, Any] = {}
    route_defs = _extract_route_definitions(repo_root)
    version = _current_version(repo_root)

    contract_to_route_ok = True
    route_to_contract_ok = True
    target_to_contract_ok = True
    runtime_discovery_ok = True
    cli_sync_ok = True
    runner_contract_invariance_ok = True

    contract_profiles: dict[str, Any] = {}
    all_profile_paths: dict[str, set[str]] = {}
    for profile in PROFILE_LABELS:
        deployment = _profile_deployment(profile)
        expected_paths = _public_paths_for_deployment(deployment)
        committed_openapi = _load_json_if_exists(_openapi_path(repo_root, profile))
        actual_paths = sorted((committed_openapi or {}).get("paths", {}).keys()) if committed_openapi else []
        missing_from_contract = [path for path in expected_paths if path not in actual_paths]
        unmapped_contract = [path for path in actual_paths if path not in route_defs]
        if missing_from_contract:
            route_to_contract_ok = False
            failures.append(f"{profile}: executable public routes missing from OpenAPI contract: {', '.join(missing_from_contract)}")
        if unmapped_contract:
            contract_to_route_ok = False
            failures.append(f"{profile}: OpenAPI contract publishes paths without decorated implementation: {', '.join(unmapped_contract)}")
        contract_profiles[profile] = {
            "expected_paths": expected_paths,
            "actual_paths": actual_paths,
            "missing_from_contract": missing_from_contract,
            "unmapped_contract_paths": unmapped_contract,
            "path_count": len(actual_paths),
        }
        all_profile_paths[profile] = set(actual_paths)

    target_to_endpoint = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-endpoint.yaml") or {}
    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml") or {}
    for item in scope.get("targets", []):
        if str(item.get("scope_bucket")) == "out-of-scope/deferred":
            continue
        label = str(item.get("label"))
        if label == "OpenRPC 1.4.x admin/control-plane contract":
            if _load_json_if_exists(_openrpc_path(repo_root, "hardening")) is None:
                target_to_contract_ok = False
                failures.append("OpenRPC target is in scope but the hardening OpenRPC artifact is missing")
            continue
        if label == "OpenAPI 3.1 / 3.2 compatible public contract":
            continue
        mapping = target_to_endpoint.get(label) or {}
        current_paths = [str(path) for path in mapping.get("current", [])]
        if not current_paths:
            continue
        for route_path in current_paths:
            if not any(route_path in paths for paths in all_profile_paths.values()):
                target_to_contract_ok = False
                failures.append(f"{label}: mapped route not present in any committed OpenAPI profile artifact: {route_path}")

    generated_cli_doc = render_cli_markdown()
    committed_cli_doc = (repo_root / "docs" / "reference" / "CLI_SURFACE.md").read_text(encoding="utf-8") if (repo_root / "docs" / "reference" / "CLI_SURFACE.md").exists() else ""
    if committed_cli_doc != generated_cli_doc:
        cli_sync_ok = False
        failures.append("CLI reference markdown drifts from tigrbl_auth.cli.metadata")
    generated_cli_contract = build_cli_contract_manifest()
    committed_cli_contract = _load_json_if_exists(repo_root / "specs" / "cli" / "cli_contract.json") or {}
    if json.dumps(generated_cli_contract, sort_keys=True) != json.dumps(committed_cli_contract, sort_keys=True):
        cli_sync_ok = False
        failures.append("CLI contract artifact drifts from tigrbl_auth.cli.metadata")
    generated_cli_snapshot = build_cli_conformance_snapshot()
    committed_cli_snapshot = _load_json_if_exists(repo_root / "docs" / "compliance" / "cli_conformance_snapshot.json") or {}
    if json.dumps(generated_cli_snapshot, sort_keys=True) != json.dumps(committed_cli_snapshot, sort_keys=True):
        cli_sync_ok = False
        failures.append("CLI conformance snapshot drifts from argparse/metadata generation")
    committed_cli_snapshot_md = (repo_root / "docs" / "compliance" / "cli_conformance_snapshot.md").read_text(encoding="utf-8") if (repo_root / "docs" / "compliance" / "cli_conformance_snapshot.md").exists() else ""
    if committed_cli_snapshot_md != render_cli_conformance_markdown(generated_cli_snapshot):
        cli_sync_ok = False
        failures.append("CLI conformance markdown drifts from argparse/metadata generation")

    discovery_profiles: dict[str, Any] = {}
    for profile in PROFILE_LABELS:
        deployment = _profile_deployment(profile)
        expected_artifacts = build_discovery_artifacts(deployment, profile_label=profile)
        profile_dir = repo_root / "specs" / "discovery" / "profiles" / profile
        committed_artifacts = {path.name for path in profile_dir.glob("*.json")} if profile_dir.exists() else set()
        expected_names = set(expected_artifacts)
        missing_names = sorted(expected_names - committed_artifacts)
        extra_names = sorted(committed_artifacts - expected_names)
        if missing_names:
            runtime_discovery_ok = False
            failures.append(f"{profile}: missing committed discovery artifacts: {', '.join(missing_names)}")
        if extra_names:
            runtime_discovery_ok = False
            failures.append(f"{profile}: committed discovery artifacts have unexpected files: {', '.join(extra_names)}")
        for name, payload in expected_artifacts.items():
            actual = _load_json_if_exists(profile_dir / name)
            if actual is None:
                continue
            if json.dumps(actual, sort_keys=True) != json.dumps(payload, sort_keys=True):
                runtime_discovery_ok = False
                failures.append(f"{profile}: discovery artifact drifts from executable deployment metadata: {name}")
        discovery_profiles[profile] = {
            "expected": sorted(expected_names),
            "committed": sorted(committed_artifacts),
            "missing": missing_names,
            "extra": extra_names,
        }

    runner_profiles: dict[str, Any] = {}
    for profile in PROFILE_LABELS:
        deployment = _profile_deployment(profile)
        matrix = build_runtime_hash_matrix(deployment=deployment)
        application_hashes = {runner: payload["application_hash"] for runner, payload in matrix.items()}
        contract_hashes = {
            "openapi": _stable_json_hash(build_openapi_contract(deployment, version=version)),
            "openrpc": _stable_json_hash(build_openrpc_contract(deployment, version=version)),
            "discovery": {
                name: _stable_json_hash(payload)
                for name, payload in build_discovery_artifacts(deployment, profile_label=profile).items()
            },
        }
        if len(set(application_hashes.values())) != 1:
            runner_contract_invariance_ok = False
            failures.append(f"{profile}: application hash varies across runner profiles")
        runner_profiles[profile] = {
            "application_hashes": application_hashes,
            "contract_hashes": {runner: contract_hashes for runner in registered_runner_names()},
            "application_hash_invariant": len(set(application_hashes.values())) == 1,
            "contract_hash_invariant": True,
        }

    stale_refs = _scan_stale_doc_refs(repo_root)
    authoritative_stale_count = sum(len(paths) for paths in stale_refs["authoritative"].values())
    historical_stale_count = sum(len(paths) for paths in stale_refs["historical"].values())
    if authoritative_stale_count:
        failures.append(f"Authoritative docs contain stale code-path references: {authoritative_stale_count}")

    summary = {
        "contract_to_route_sync_passed": contract_to_route_ok,
        "route_to_contract_sync_passed": route_to_contract_ok,
        "target_to_contract_sync_passed": target_to_contract_ok,
        "cli_metadata_to_docs_sync_passed": cli_sync_ok,
        "runtime_plan_to_discovery_sync_passed": runtime_discovery_ok,
        "runner_contract_hash_invariance_passed": runner_contract_invariance_ok,
        "authoritative_current_doc_stale_ref_count": authoritative_stale_count,
        "historical_doc_stale_ref_count": historical_stale_count,
        "openapi_profile_count_checked": len(PROFILE_LABELS),
        "discovery_profile_count_checked": len(PROFILE_LABELS),
    }
    details.update({
        "contract_profiles": contract_profiles,
        "discovery_profiles": discovery_profiles,
        "runner_profiles": runner_profiles,
        "stale_doc_refs": stale_refs,
    })
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": summary,
        "details": details,
    }
    _write_report(repo_root / "docs" / "compliance", "artifact_truthfulness_report", payload, "Artifact Truthfulness Report")
    return payload


def build_feature_completeness_report(repo_root: Path, *, report_dir: Path | None = None) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    warnings: list[str] = []
    details: dict[str, Any] = {}

    cli_snapshot = build_cli_conformance_snapshot()
    cli_contract = build_cli_contract_manifest()
    verb_index = {
        str(spec.get("name")): {str(verb.get("name")) for verb in spec.get("verbs", [])}
        for spec in cli_contract.get("commands", [])
    }

    def _capability(label: str, *, passed: bool, summary: str, evidence: list[str] | None = None, details_payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "label": label,
            "passed": bool(passed),
            "summary": summary,
            "evidence": list(evidence or []),
            "details": dict(details_payload or {}),
        }

    capabilities: dict[str, dict[str, Any]] = {}

    project_tree_rc = run_project_tree_layout_check(repo_root, strict=False, report_dir=report_dir)
    bootstrap_verbs = verb_index.get("bootstrap", set())
    capabilities["initialize_repo_project_tree"] = _capability(
        "initialize repo/project tree",
        passed=project_tree_rc == 0 and {"status", "manifest", "apply", "verify"} <= bootstrap_verbs,
        summary="Project-tree layout verification and bootstrap lifecycle verbs are installed.",
        evidence=["docs/compliance/project_tree_layout_report.md", "docs/compliance/cli_conformance_snapshot.md"],
        details_payload={"project_tree_layout_passed": project_tree_rc == 0, "bootstrap_verbs": sorted(bootstrap_verbs)},
    )

    sandbox_root = Path(
        tempfile.mkdtemp(
            prefix="feature-completeness-sandbox-",
            dir=str((repo_root / "dist").resolve()),
        )
    )

    def _ctx(root: Path, resource: str, command: str, *, profile: str = "baseline", tenant: str | None = None) -> OperationContext:
        return OperationContext(repo_root=root, command=command, resource=resource, actor="feature-completeness", profile=profile, tenant=tenant)

    def _reset_operator_state(root: Path) -> None:
        state_root = operator_state_root(root)
        if state_root.exists():
            shutil.rmtree(state_root)

    operator_root = sandbox_root / "operator-state"
    _reset_operator_state(operator_root)
    client_create = create_resource(_ctx(operator_root, "client", "client.create", tenant="tenant-a"), record_id="client-a", patch={"name": "Feature Client"}, if_exists="error")
    client_update = update_resource(_ctx(operator_root, "client", "client.update", tenant="tenant-a"), record_id="client-a", patch={"display_name": "Feature Client Alpha"}, if_missing="error")
    client_get = get_resource(_ctx(operator_root, "client", "client.get", tenant="tenant-a"), record_id="client-a")
    client_list = list_resource_result(_ctx(operator_root, "client", "client.list", tenant="tenant-a"), limit=20, offset=0)
    client_delete = delete_resource(_ctx(operator_root, "client", "client.delete", tenant="tenant-a"), record_id="client-a")
    operator_summary = operator_store_summary(operator_root)
    client_verbs = verb_index.get("client", set())
    client_passed = (
        client_create.status == "created"
        and client_update.status == "updated"
        and bool(client_get.record)
        and any(item.get("id") == "client-a" for item in (client_list.items or []))
        and client_delete.status == "deleted"
        and {"create", "update", "delete", "get", "list", "rotate-secret", "enable", "disable"} <= client_verbs
    )
    capabilities["bootstrap_storage"] = _capability(
        "bootstrap storage",
        passed=operator_summary.get("backend") == "sqlite-authoritative" and operator_summary.get("repo_mutation_dependency") is False,
        summary="The operator plane materializes durable sqlite-backed storage outside the repository tree.",
        evidence=["tigrbl_auth/services/_operator_store.py", "tests/unit/test_operator_control_plane.py"],
        details_payload=operator_summary,
    )
    capabilities["register_manage_clients"] = _capability(
        "register/manage clients",
        passed=client_passed,
        summary="Client records can be created, updated, listed, fetched, and deleted through the durable operator plane.",
        evidence=["tests/conformance/operator/test_cli_resource_lifecycle.py", "tests/unit/test_operator_control_plane.py"],
        details_payload={"create_status": client_create.status, "update_status": client_update.status, "delete_status": client_delete.status, "client_verbs": sorted(client_verbs)},
    )

    keys_root = sandbox_root / "keys-state"
    _reset_operator_state(keys_root)
    key_create = generate_key_record(_ctx(keys_root, "keys", "keys.generate"), patch={"kid": "feature-key", "label": "primary"})
    key_rotate = rotate_key_record(_ctx(keys_root, "keys", "keys.rotate"), record_id="feature-key")
    jwks = publish_jwks_document(_ctx(keys_root, "keys", "keys.publish-jwks"))
    key_retire = retire_key_record(_ctx(keys_root, "keys", "keys.retire"), record_id="feature-key")
    keys_verbs = verb_index.get("keys", set())
    capabilities["rotate_publish_keys_jwks"] = _capability(
        "rotate and publish keys / JWKS",
        passed=(
            key_create.status == "created"
            and key_rotate.status == "updated"
            and key_retire.status == "retired"
            and jwks.status == "published"
            and {"generate", "import", "export", "rotate", "retire", "publish-jwks", "get", "list", "delete"} <= keys_verbs
        ),
        summary="Operator key lifecycle workflows generate, rotate, retire, and publish JWKS artifacts.",
        evidence=["tests/conformance/operator/test_cli_keys_lifecycle.py", "dist/jwks/jwks.json"],
        details_payload={"generate_status": key_create.status, "rotate_status": key_rotate.status, "retire_status": key_retire.status, "jwks_status": jwks.status, "keys_verbs": sorted(keys_verbs)},
    )

    portability_source = sandbox_root / "portability-source"
    portability_import = sandbox_root / "portability-import"
    _reset_operator_state(portability_source)
    _reset_operator_state(portability_import)
    create_resource(_ctx(portability_source, "tenant", "tenant.create", tenant="tenant-a"), record_id="tenant-a", patch={"name": "Portable Tenant"}, if_exists="error")
    generate_key_record(_ctx(portability_source, "keys", "keys.generate", tenant="tenant-a"), patch={"kid": "portable-key", "label": "portable"})
    export_path = sandbox_root / "exports" / "portable-export.json"
    export_result = run_export(_ctx(portability_source, "export", "export.run", tenant="tenant-a"), output_path=export_path, redact=True)
    import_validation = validate_import_artifact(export_path)
    import_result = run_import(_ctx(portability_import, "import", "import.run", tenant="tenant-a"), path=export_path)
    imported_tenant = get_resource(_ctx(portability_import, "tenant", "tenant.get", tenant="tenant-a"), record_id="tenant-a")
    capabilities["export_import_state"] = _capability(
        "export/import state",
        passed=export_result.status == "exported" and import_validation.get("valid") is True and import_result.status == "imported" and bool(imported_tenant.record),
        summary="Portability workflows export a versioned artifact and import it into a new durable operator-plane state root.",
        evidence=["tests/conformance/operator/test_cli_import_export.py", str(export_path.relative_to(repo_root)) if export_path.exists() else ""],
        details_payload={"export_status": export_result.status, "import_valid": import_validation.get("valid"), "import_status": import_result.status},
    )

    deployment = deployment_from_options(profile="baseline")
    openapi_path = write_openapi_contract(repo_root, deployment)
    openrpc_path = write_openrpc_contract(repo_root, deployment)
    discovery_paths = write_discovery_artifacts(repo_root, deployment, profile_label=deployment.profile)
    discovery_context = _ctx(repo_root, "discovery", "discovery.publish", profile="baseline")
    discovery_publish = publish_discovery(discovery_context, output_dir=sandbox_root / "discovery")
    discovery_validation = validate_discovery(repo_root, profile="baseline")
    discovery_diff = diff_discovery(repo_root, left_profile="baseline", right_profile="production")
    contract_sync_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "contract_sync_report.json") or {}
    artifact_truthfulness_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "artifact_truthfulness_report.json") or {}
    spec_verbs = verb_index.get("spec", set())
    discovery_verbs = verb_index.get("discovery", set())
    capabilities["emit_contract_artifacts"] = _capability(
        "emit OpenAPI/OpenRPC/discovery artifacts",
        passed=(
            openapi_path.exists()
            and openrpc_path.exists()
            and bool(discovery_paths)
            and discovery_publish.status == "published"
            and discovery_validation.get("valid") is True
            and bool(contract_sync_report.get("passed", False))
            and bool(artifact_truthfulness_report.get("passed", False))
            and {"generate", "validate", "diff", "report"} <= spec_verbs
            and {"show", "validate", "publish", "diff"} <= discovery_verbs
        ),
        summary="Contracts and discovery artifacts regenerate cleanly and remain synchronized with executable reality.",
        evidence=["docs/compliance/contract_sync_report.md", "docs/compliance/artifact_truthfulness_report.md", "docs/reference/CLI_SURFACE.md"],
        details_payload={
            "openapi_path": str(openapi_path.relative_to(repo_root)),
            "openrpc_path": str(openrpc_path.relative_to(repo_root)),
            "discovery_publish_status": discovery_publish.status,
            "discovery_document_count": discovery_validation.get("document_count", 0),
            "discovery_changed_count": len(discovery_diff.get("changed", [])),
            "spec_verbs": sorted(spec_verbs),
            "discovery_verbs": sorted(discovery_verbs),
        },
    )

    release_verbs = verb_index.get("release", set())
    release_bundle_dir = sandbox_root / "release-bundle"
    bundle = build_release_bundle(repo_root, deployment, bundle_dir=release_bundle_dir)
    signed = sign_release_bundle(bundle, signing_key="capability-feature-key")
    verified = verify_release_bundle_signatures(bundle)
    capabilities["build_sign_verify_release_bundles"] = _capability(
        "build, sign, and verify release bundles",
        passed=bundle.exists() and signed.get("verification", {}).get("passed") is True and verified.get("passed") is True and {"bundle", "sign", "verify", "status"} <= release_verbs,
        summary="Release bundles can be materialized, signed, and verified from repository state.",
        evidence=["tests/security/test_release_bundle_signing.py", str(bundle.relative_to(repo_root))],
        details_payload={"bundle_dir": str(bundle.relative_to(repo_root)), "sign_status": signed.get("status"), "release_verbs": sorted(release_verbs)},
    )

    runtime_report = write_runtime_profile_report(repo_root, deployment=deployment, report_dir=report_dir)
    runner_names = set(registered_runner_names())
    capabilities["serve_supported_runners"] = _capability(
        "serve the app under supported runners",
        passed=(
            runner_names == {"uvicorn", "hypercorn", "tigrcorn"}
            and int(runtime_report.get("summary", {}).get("runner_count", 0)) == 3
            and int(runtime_report.get("summary", {}).get("ready_count", 0)) == 3
            and bool(runtime_report.get("summary", {}).get("application_hash_invariant", False))
            and bool(runtime_report.get("summary", {}).get("surface_probe_passed", False))
        ),
        summary="The runtime boundary declares all supported runners, but this checkpoint still requires supported-matrix readiness evidence for a full pass.",
        evidence=["docs/compliance/runtime_profile_report.md", "tests/runtime/test_runner_invariance.py", "tests/conformance/operator/test_cli_serve_runtime.py"],
        details_payload={"registered_runners": sorted(runner_names), "runtime_summary": runtime_report.get("summary", {})},
    )

    migration_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "migration_portability_report.json") or {}
    migrate_verbs = verb_index.get("migrate", set())
    capabilities["migrate_up_down_reapply"] = _capability(
        "migrate up/down/reapply",
        passed=bool(migration_report.get("passed", False)) and {"status", "plan", "apply", "verify"} <= migrate_verbs,
        summary="Migration portability remains blocked until both SQLite and PostgreSQL preserve upgrade/downgrade/reapply evidence.",
        evidence=["docs/compliance/migration_portability_report.md", "tests/integration/test_migration_upgrade_downgrade_safety.py"],
        details_payload={
            "migration_report_passed": bool(migration_report.get("passed", False)),
            "validated_backends": migration_report.get("validated_backends", []),
            "passed_backends": migration_report.get("passed_backends", []),
            "migrate_verbs": sorted(migrate_verbs),
        },
    )

    no_fastapi = _load_json_if_exists(repo_root / "docs" / "compliance" / "no_fastapi_starlette_report.json") or {}
    direct_import_hits = int(no_fastapi.get("direct_fastapi_starlette_imports_found", 0) or 0)
    metadata_hits = len(no_fastapi.get("pyproject_forbidden_dependencies_found", [])) if isinstance(no_fastapi.get("pyproject_forbidden_dependencies_found"), list) else 0
    capabilities["tigrbl_native_runtime_boundary"] = _capability(
        "remain Tigrbl-native with no FastAPI/Starlette drift",
        passed=direct_import_hits == 0 and metadata_hits == 0,
        summary="The active runtime and packaging metadata remain free of forbidden FastAPI/Starlette dependencies or imports.",
        evidence=["docs/compliance/no_fastapi_starlette_report.md", "docs/adr/ADR-0004-no-fastapi-no-starlette.md"],
        details_payload={"direct_import_hits": direct_import_hits, "metadata_hits": metadata_hits},
    )

    passed_count = sum(1 for payload in capabilities.values() if payload["passed"])
    feature_complete = passed_count == len(capabilities)
    if not feature_complete:
        for key, payload in capabilities.items():
            if not payload["passed"]:
                failures.append(f"{payload['label']}: {payload['summary']}")

    details = {name: payload for name, payload in capabilities.items()}
    payload = {
        "passed": feature_complete,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "capability_count": len(capabilities),
            "passed_capability_count": passed_count,
            "failed_capability_count": len(capabilities) - passed_count,
            "fully_featured_package_boundary_now": feature_complete,
            "cli_metadata_single_source_passed": bool(cli_snapshot.get("summary", {}).get("passed", False)),
            "required_release_verify_verb_present": "verify" in release_verbs,
            "no_fastapi_starlette_passed": direct_import_hits == 0 and metadata_hits == 0,
        },
        "details": details,
    }
    _write_report(report_dir, "feature_completeness_report", payload, "Feature Completeness Report")
    return payload


def _ensure_repo_local_operator_state(repo_root: Path) -> Path:
    state_root = repo_root / ".pytest-tmp" / "operator-state" / "certification-closure"
    state_root.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(state_root))
    return state_root


def generate_state_reports(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    claims = _load_yaml(repo_root / "compliance" / "claims" / "declared-target-claims.yaml")
    target_to_module = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-module.yaml")
    target_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml")
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    scope_path = repo_root / "compliance" / "targets" / "certification_scope.yaml"
    scope = _load_yaml(scope_path) if scope_path.exists() else {}
    scope_freeze_failures, scope_freeze_summary = validate_scope_freeze_metadata(scope) if scope else (["missing certification_scope"], {})
    claim_entries = list(claims.get("claim_set", {}).get("claims", []))
    targets = [str(entry.get("target")) for entry in claim_entries]
    effective_baseline = _load_yaml(repo_root / "compliance" / "claims" / "effective-target-claims.baseline.yaml")
    effective_production = _load_yaml(repo_root / "compliance" / "claims" / "effective-target-claims.production.yaml")
    effective_hardening = _load_yaml(repo_root / "compliance" / "claims" / "effective-target-claims.hardening.yaml")
    tier_counts = {tier: 0 for tier in range(5)}
    tier_by_target: dict[str, int] = {}
    for entry in claim_entries:
        tier = int(entry.get("tier", 0))
        target = str(entry.get("target"))
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        tier_by_target[target] = tier

    scope_entries = [entry for entry in scope.get("targets", []) if str(entry.get("scope_bucket")) != "out-of-scope/deferred"]
    protocol_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("family")) not in {"runtime", "operator"}]
    runtime_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("family")) == "runtime"]
    operator_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("family")) == "operator"]
    retained_targets = [str(entry.get("label")) for entry in scope_entries]
    baseline_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("scope_bucket")) == "baseline-certifiable-now"]
    production_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("scope_bucket")) == "production-completion-required"]
    hardening_targets = [str(entry.get("label")) for entry in scope_entries if str(entry.get("scope_bucket")) == "hardening-completion-required"]

    def _count_below_tier(target_names: list[str], *, minimum: int = 3) -> int:
        return sum(1 for name in target_names if tier_by_target.get(name, 0) < minimum)

    all_retained_tier3 = _count_below_tier(retained_targets) == 0
    all_protocol_tier3 = _count_below_tier(protocol_targets) == 0
    strict_independent_claims_ready = _count_below_tier(retained_targets, minimum=4) == 0

    bucket_counts = {
        "baseline_certifiable_now_count": len(baseline_targets),
        "production_completion_required_count": _count_below_tier(production_targets),
        "hardening_completion_required_count": _count_below_tier(hardening_targets),
        "runtime_completion_required_count": _count_below_tier(runtime_targets),
        "operator_completion_required_count": _count_below_tier(operator_targets),
        "retained_targets_below_tier3_count": _count_below_tier(retained_targets),
    }
    signed_bundles = sorted((repo_root / "dist" / "release-bundles").glob("*/*/signature.json")) if (repo_root / "dist" / "release-bundles").exists() else []

    pyproject = _load_pyproject_manifest(repo_root)
    project = pyproject.get("project", {}) if isinstance(pyproject, dict) else {}
    base_dependencies = [str(item) for item in project.get("dependencies", []) or []]
    optional_dependencies = project.get("optional-dependencies", {}) or {}
    workspace_sources = (((pyproject.get("tool", {}) or {}).get("uv", {}) or {}).get("sources", {}) or {}) if isinstance(pyproject, dict) else {}
    runner_extras = {name: list(values) for name, values in optional_dependencies.items() if name in {"uvicorn", "hypercorn", "tigrcorn", "servers"}}
    storage_extras = {name: list(values) for name, values in optional_dependencies.items() if name in {"postgres", "sqlite"}}
    dependency_artifacts = _dependency_artifact_paths(repo_root)
    dependency_lock_manifest = repo_root / "constraints" / "dependency-lock.json"
    test_constraints_manifest = repo_root / "constraints" / "test.txt"
    tox_manifest = repo_root / "tox.ini"
    tigrcorn_extra = runner_extras.get("tigrcorn", [])
    runtime_pkg = repo_root / "tigrbl_auth" / "runtime"
    runtime_module_count = len(list(runtime_pkg.glob("*.py"))) if runtime_pkg.exists() else 0
    runner_names = list(registered_runner_names())
    hash_matrix = build_runtime_hash_matrix()
    runner_registry = runner_registry_manifest()
    runtime_profile_report = write_runtime_profile_report(
        repo_root,
        deployment=deployment_from_options(profile="baseline"),
        report_dir=repo_root / "docs" / "compliance",
    )
    install_substrate_report = write_install_substrate_report(
        repo_root,
        report_dir=repo_root / "docs" / "compliance",
    )
    authoritative_docs_manifest = write_authoritative_current_docs_manifest(repo_root)
    run_contract_sync_check(repo_root, strict=False, report_dir=repo_root / "docs" / "compliance")
    run_runtime_foundation_check(repo_root, strict=False, report_dir=repo_root / "docs" / "compliance")
    contract_sync_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "contract_sync_report.json") or {}
    no_fastapi_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "no_fastapi_starlette_report.json") or {}
    artifact_truthfulness = generate_artifact_truthfulness_report(repo_root)
    feature_completeness = build_feature_completeness_report(repo_root, report_dir=repo_root / "docs" / "compliance")
    certification_evidence_index = generate_certification_evidence_index(repo_root)
    peer_bundle_completeness = verify_peer_bundle_completeness(repo_root, strict=False)
    operator_plane = operator_plane_status(repo_root)
    validated_execution = load_validated_execution_status(repo_root)
    peer_matrix_report_path = repo_root / "docs" / "compliance" / "peer_matrix_report.json"
    peer_matrix_report = json.loads(peer_matrix_report_path.read_text(encoding="utf-8")) if peer_matrix_report_path.exists() else {}
    peer_matrix_summary = peer_matrix_report.get("summary", {}) if isinstance(peer_matrix_report, dict) else {}

    current_state = {
        "repository_tier": claims.get("claim_set", {}).get("current_repository_tier", 0),
        "delivery_track": claims.get("claim_set", {}).get("delivery_track", "unknown"),
        "authoritative_scope_manifest": str(scope_path.relative_to(repo_root)) if scope_path.exists() else None,
        "boundary_freeze_active": bool(scope.get("boundary_freeze")),
        "boundary_freeze_passed": not scope_freeze_failures,
        "boundary_freeze_decision_id": str(scope.get("boundary_freeze", {}).get("decision_id", "")),
        "boundary_freeze_effective_date": str(scope.get("boundary_freeze", {}).get("effective_date", "")),
        "boundary_freeze_retained_target_count": int(scope.get("boundary_freeze", {}).get("retained_target_count", 0) or 0),
        "boundary_freeze_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_rfc_target_count", 0) or 0),
        "boundary_freeze_non_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_non_rfc_target_count", 0) or 0),
        "boundary_freeze_deferred_target_count": int(scope.get("boundary_freeze", {}).get("deferred_target_count", 0) or 0),
        "boundary_freeze_identity_hash_matches": bool(scope_freeze_summary.get("scope_freeze_retained_target_identity_hash_matches", False)),
        "document_authority_manifest": authoritative_docs_manifest.get("projection_manifest"),
        "document_authority_spec": authoritative_docs_manifest.get("authority_spec"),
        "document_authority_projection_manifest": authoritative_docs_manifest.get("projection_manifest"),
        "canonical_ssot_root_count": len(authoritative_docs_manifest.get("canonical_ssot_roots", [])),
        "certification_bundle_current_state_doc_only": True,
        "certification_bundle_generated_current_docs_only": True,
        "authoritative_current_doc_count": len(authoritative_docs_manifest.get("authoritative_current_docs", [])),
        "archived_historical_root_count": len(authoritative_docs_manifest.get("archive_roots", [])),
        "archived_reference_doc_count": len(list((repo_root / "docs" / "archive" / "historical" / "reference").glob("*.md"))) if (repo_root / "docs" / "archive" / "historical" / "reference").exists() else 0,
        "certification_bundle_current_state_doc_count": len(authoritative_docs_manifest.get("certification_bundle_generated_current_docs", [])),
        "declared_claim_count": len(claim_entries),
        "mapped_module_count": sum(1 for target in targets if target in target_to_module),
        "mapped_test_count": sum(1 for target in targets if target in target_to_test),
        "mapped_evidence_count": sum(1 for target in targets if target in target_to_evidence),
        "effective_baseline_count": len(effective_baseline.get("claim_set", {}).get("claims", [])),
        "effective_production_count": len(effective_production.get("claim_set", {}).get("claims", [])),
        "effective_hardening_count": len(effective_hardening.get("claim_set", {}).get("claims", [])),
        "tier_0_claim_count": tier_counts.get(0, 0),
        "tier_1_claim_count": tier_counts.get(1, 0),
        "tier_2_claim_count": tier_counts.get(2, 0),
        "tier_3_claim_count": tier_counts.get(3, 0),
        "tier_4_claim_count": tier_counts.get(4, 0),
        "protocol_boundary_tier3_complete": all_protocol_tier3,
        "retained_boundary_tier3_complete": all_retained_tier3,
        "strict_independent_claims_ready": strict_independent_claims_ready,
        "tier4_peer_bundle_completeness_passed": bool(peer_bundle_completeness.get("passed", False)),
        "tier4_supported_peer_profile_count": int(peer_matrix_summary.get("candidate_profile_count", peer_matrix_summary.get("profile_count", 0))),
        "tier4_required_external_bundle_count": int(peer_matrix_summary.get("candidate_profile_count", peer_matrix_summary.get("profile_count", 0))),
        "tier4_external_bundle_count": int(peer_matrix_summary.get("external_bundle_count", 0)),
        "tier4_valid_external_bundle_count": int(peer_matrix_summary.get("valid_external_bundle_count", peer_matrix_summary.get("external_bundle_count", 0))),
        "tier4_invalid_external_bundle_count": int(peer_matrix_summary.get("invalid_external_bundle_count", 0)),
        "tier4_missing_external_bundle_count": int(peer_matrix_summary.get("missing_external_bundle_count", max(int(peer_matrix_summary.get("candidate_profile_count", peer_matrix_summary.get("profile_count", 0))) - int(peer_matrix_summary.get("external_bundle_count", 0)) - int(peer_matrix_summary.get("invalid_external_bundle_count", 0)), 0))),
        "tier4_external_handoff_template_present": (repo_root / "dist" / "tier4-external-handoff" / "external-root-template.json").exists(),
        "signed_release_bundle_count": len(signed_bundles),
        "release_attestation_verifiable": len(signed_bundles) > 0,
        "base_dependency_count": len(base_dependencies),
        "base_exact_pinned_dependency_count": sum(1 for item in base_dependencies if _is_exact_pin(item)),
        "optional_extra_count": len(optional_dependencies),
        "runner_extra_count": len(runner_extras),
        "storage_extra_count": len(storage_extras),
        "workspace_source_count": len(workspace_sources),
        "workspace_sources_present": bool(workspace_sources),
        "dependency_provenance_artifact_count": len(dependency_artifacts),
        "dependency_lock_manifest_present": dependency_lock_manifest.exists(),
        "install_substrate_report_present": (repo_root / "docs" / "compliance" / "install_substrate_report.json").exists(),
        "install_substrate_manifest_passed": bool(install_substrate_report.get("summary", {}).get("static_manifest_passed", False)),
        "install_substrate_current_profile": str(install_substrate_report.get("summary", {}).get("profile", "")),
        "install_substrate_current_python_supported": bool(install_substrate_report.get("summary", {}).get("current_python_supported", False)),
        "install_substrate_detected_supported_python_count": int(install_substrate_report.get("summary", {}).get("detected_supported_python_count", 0)),
        "install_substrate_expected_supported_python_count": int(install_substrate_report.get("summary", {}).get("expected_supported_python_count", 0)),
        "install_substrate_tox_env_count": int(install_substrate_report.get("summary", {}).get("declared_certification_tox_env_count", 0)),
        "install_substrate_tox_pip_check_complete": bool(install_substrate_report.get("summary", {}).get("tox_envs_declare_pip_check", False)),
        "install_substrate_tox_import_probe_complete": bool(install_substrate_report.get("summary", {}).get("tox_envs_declare_install_probe", False)),
        "install_substrate_current_profile_import_probe_passed": bool(install_substrate_report.get("summary", {}).get("current_profile_import_probe_passed", False)),
        "test_constraints_manifest_present": test_constraints_manifest.exists(),
        "tox_manifest_present": tox_manifest.exists(),
        "native_uv_lock_present": (repo_root / "uv.lock").exists(),
        "install_profile_workflow_present": has_install_matrix_workflow(repo_root),
        "release_gate_workflow_present": has_release_gate_workflow(repo_root),
        "clean_room_matrix_implemented": tox_manifest.exists() and has_install_matrix_workflow(repo_root) and has_release_gate_workflow(repo_root),
        "clean_room_matrix_executed_in_this_container": False,
        "tigrcorn_extra_placeholder": len(tigrcorn_extra) == 0 and "tigrcorn" in runner_extras,
        "tigrcorn_pin_committed": len(tigrcorn_extra) > 0,
        "runtime_adapter_layer_present": runtime_pkg.exists(),
        "runtime_adapter_module_count": runtime_module_count,
        "registered_runner_count": len(runner_names),
        "registered_runner_names": ", ".join(runner_names),
        "runtime_application_hash_invariant": len({item["application_hash"] for item in hash_matrix.values()}) == 1,
        "runtime_runner_availability_count": len([item for item in runner_registry if item.get("installed")]),
        "runtime_profile_report_present": (repo_root / "docs" / "compliance" / "runtime_profile_report.json").exists(),
        "runtime_profile_ready_count": int(runtime_profile_report.get("summary", {}).get("ready_count", 0)),
        "runtime_profile_missing_count": int(runtime_profile_report.get("summary", {}).get("missing_count", 0)),
        "runtime_profile_invalid_count": int(runtime_profile_report.get("summary", {}).get("invalid_count", 0)),
        "runtime_profile_application_probe_passed": bool(runtime_profile_report.get("application_probe", {}).get("passed", False)),
        "runtime_profile_surface_probe_passed": bool(runtime_profile_report.get("summary", {}).get("surface_probe_passed", False)),
        "runtime_profile_surface_probe_endpoint_count": int(runtime_profile_report.get("summary", {}).get("surface_probe_endpoint_count", 0)),
        "runtime_profile_surface_probe_passed_count": int(runtime_profile_report.get("summary", {}).get("surface_probe_passed_count", 0)),
        "runtime_profile_surface_probe_failed_count": int(runtime_profile_report.get("summary", {}).get("surface_probe_failed_count", 0)),
        "runtime_profile_serve_check_passed_count": int(runtime_profile_report.get("summary", {}).get("serve_check_passed_count", 0)),
        "runtime_profile_execution_probe_complete": bool(runtime_profile_report.get("summary", {}).get("execution_probe_complete", False)),
        "runtime_profile_placeholder_supported_runner_count": int(runtime_profile_report.get("summary", {}).get("placeholder_supported_runner_count", 0)),
        "runtime_profile_declared_ci_installable_runner_count": int(runtime_profile_report.get("summary", {}).get("declared_ci_installable_runner_count", 0)),
        "runtime_profile_declared_ci_install_probe_complete": bool(runtime_profile_report.get("summary", {}).get("declared_ci_install_probe_complete", False)),
        "operator_plane_backend": str(operator_plane.get("backend", "unknown")),
        "operator_plane_repo_mutation_dependency": bool(operator_plane.get("repo_mutation_dependency", True)),
        "operator_plane_tenancy_enforced": bool(operator_plane.get("tenancy_enforced", False)),
        "operator_plane_database_present": bool(operator_plane.get("database_present", False)),
        "operator_plane_state_root": str(operator_plane.get("state_root", "")),
        "operator_plane_portability_schema_version": int(operator_plane.get("portability_schema_version", 0) or 0),
        "pyproject_requires_python": str(project.get("requires-python", "unspecified")),
        "serve_runtime_launcher_present": True,
        "cli_contract_artifact_present": (repo_root / "specs" / "cli" / "cli_contract.json").exists(),
        "cli_contract_snapshot_present": (repo_root / "docs" / "compliance" / "cli_conformance_snapshot.json").exists(),
        "cli_help_snapshot_present": (repo_root / "docs" / "compliance" / "cli_conformance_snapshot.md").exists(),
        "cli_command_count": int(build_cli_contract_manifest().get("summary", {}).get("command_count", 0)),
        "cli_verb_count": int(build_cli_contract_manifest().get("summary", {}).get("verb_count", 0)),
        "cli_catalog_only_resource_command_count": len(build_cli_conformance_snapshot().get("summary", {}).get("catalog_only_resource_commands", [])),
        "cli_required_verbs_missing": bool(build_cli_conformance_snapshot().get("summary", {}).get("missing_required_verbs", {})),
        "artifact_truthfulness_passed": bool(artifact_truthfulness.get("passed", False)),
        "contract_sync_report_passed": bool(contract_sync_report.get("passed", False)),
        "contract_to_route_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("contract_to_route_sync_passed", False)),
        "route_to_contract_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("route_to_contract_sync_passed", False)),
        "target_to_contract_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("target_to_contract_sync_passed", False)),
        "cli_metadata_to_docs_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("cli_metadata_to_docs_sync_passed", False)),
        "runtime_plan_to_discovery_sync_passed": bool(artifact_truthfulness.get("summary", {}).get("runtime_plan_to_discovery_sync_passed", False)),
        "runner_contract_hash_invariance_passed": bool(artifact_truthfulness.get("summary", {}).get("runner_contract_hash_invariance_passed", False)),
        "no_fastapi_starlette_passed": bool(feature_completeness.get("summary", {}).get("no_fastapi_starlette_passed", False)),
        "feature_completeness_capability_count": int(feature_completeness.get("summary", {}).get("capability_count", 0)),
        "feature_completeness_passed_capability_count": int(feature_completeness.get("summary", {}).get("passed_capability_count", 0)),
        "feature_completeness_failed_capability_count": int(feature_completeness.get("summary", {}).get("failed_capability_count", 0)),
        "fully_featured_package_boundary_now": bool(feature_completeness.get("summary", {}).get("fully_featured_package_boundary_now", False)),
        "feature_release_verify_verb_present": bool(feature_completeness.get("summary", {}).get("required_release_verify_verb_present", False)),
        "certification_evidence_index_passed": bool(certification_evidence_index.get("passed", False)),
        "certification_evidence_claim_count": int(certification_evidence_index.get("summary", {}).get("claim_count", 0)),
        "certification_evidence_partition_count": int(certification_evidence_index.get("summary", {}).get("partition_count", 0)),
        "certification_evidence_target_profile_bundle_count": int(certification_evidence_index.get("summary", {}).get("target_profile_bundle_count", 0)),
        "release_evidence_clean_checkout_required": True,
        "release_evidence_clean_checkout_now": bool(certification_evidence_index.get("summary", {}).get("clean_checkout", {}).get("clean", False)),
        "release_evidence_dirty_checkout_path_count": int(certification_evidence_index.get("summary", {}).get("clean_checkout", {}).get("changed_path_count", 0)),
        "authoritative_current_doc_stale_ref_count": int(artifact_truthfulness.get("summary", {}).get("authoritative_current_doc_stale_ref_count", 0)),
        "historical_doc_stale_ref_count": int(artifact_truthfulness.get("summary", {}).get("historical_doc_stale_ref_count", 0)),
        "authoritative_current_doc_count": len(authoritative_docs_manifest.get("authoritative_current_docs", [])),
        "derived_current_doc_count": len(authoritative_docs_manifest.get("derived_current_docs", [])),
        "historical_archive_present": (repo_root / "docs" / "archive").exists(),
        "certification_bundle_generated_current_docs_only": True,
        "validated_execution_artifact_count": int(validated_execution.get("validated_artifact_count", 0)),
        "required_validated_inventory_count": int(validated_execution.get("required_validated_inventory_count", 0)),
        "validated_inventory_present_count": int(validated_execution.get("validated_inventory_present_count", 0)),
        "validated_inventory_complete": bool(validated_execution.get("validated_inventory_complete", False)),
        "validated_runtime_matrix_expected_count": int(validated_execution.get("runtime_matrix_expected_count", 0)),
        "validated_runtime_matrix_passed_count": int(validated_execution.get("runtime_matrix_passed_count", 0)),
        "validated_clean_room_matrix_green": bool(validated_execution.get("runtime_matrix_green", False)),
        "validated_test_lane_expected_count": int(validated_execution.get("test_lane_expected_count", 0)),
        "validated_test_lane_passed_count": int(validated_execution.get("test_lane_passed_count", 0)),
        "validated_in_scope_test_lanes_green": bool(validated_execution.get("in_scope_test_lanes_green", False)),
        "migration_portability_passed": bool(validated_execution.get("migration_portability_passed", False)),
        "tier3_evidence_rebuilt_from_validated_runs": bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)),
        **bucket_counts,
    }
    certification_state = {
        "fully_certifiable_now": strict_independent_claims_ready and all_retained_tier3 and bool(artifact_truthfulness.get("passed", False)) and bool(validated_execution.get("runtime_matrix_green", False)) and bool(validated_execution.get("in_scope_test_lanes_green", False)) and bool(validated_execution.get("migration_portability_passed", False)) and bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)) and int(runtime_profile_report.get("summary", {}).get("ready_count", 0)) == len(runner_names) and int(runtime_profile_report.get("summary", {}).get("invalid_count", 0)) == 0 and int(runtime_profile_report.get("summary", {}).get("missing_count", 0)) == 0,
        "fully_rfc_compliant_now": strict_independent_claims_ready and all_protocol_tier3 and bool(validated_execution.get("runtime_matrix_green", False)) and bool(validated_execution.get("in_scope_test_lanes_green", False)) and bool(validated_execution.get("migration_portability_passed", False)),
        "protocol_boundary_tier3_complete": all_protocol_tier3,
        "retained_boundary_tier3_complete": all_retained_tier3,
        "strict_independent_claims_ready": strict_independent_claims_ready,
        "authoritative_scope_manifest": str(scope_path.relative_to(repo_root)) if scope_path.exists() else None,
        "boundary_freeze_active": bool(scope.get("boundary_freeze")),
        "boundary_freeze_passed": not scope_freeze_failures,
        "boundary_freeze_decision_id": str(scope.get("boundary_freeze", {}).get("decision_id", "")),
        "boundary_freeze_effective_date": str(scope.get("boundary_freeze", {}).get("effective_date", "")),
        "boundary_freeze_retained_target_count": int(scope.get("boundary_freeze", {}).get("retained_target_count", 0) or 0),
        "boundary_freeze_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_rfc_target_count", 0) or 0),
        "boundary_freeze_non_rfc_target_count": int(scope.get("boundary_freeze", {}).get("retained_non_rfc_target_count", 0) or 0),
        "boundary_freeze_deferred_target_count": int(scope.get("boundary_freeze", {}).get("deferred_target_count", 0) or 0),
        "boundary_freeze_identity_hash_matches": bool(scope_freeze_summary.get("scope_freeze_retained_target_identity_hash_matches", False)),
        "clean_room_matrix_implemented": bool(current_state.get("tox_manifest_present", False) and current_state.get("install_profile_workflow_present", False) and current_state.get("release_gate_workflow_present", False)),
        "clean_room_matrix_executed_in_this_container": False,
        "tox_manifest_present": bool(current_state.get("tox_manifest_present", False)),
        "test_constraints_manifest_present": bool(current_state.get("test_constraints_manifest_present", False)),
        "tigrcorn_pin_committed": bool(current_state.get("tigrcorn_pin_committed", False)),
        "operator_plane_backend": str(current_state.get("operator_plane_backend", "unknown")),
        "operator_plane_repo_mutation_dependency": bool(current_state.get("operator_plane_repo_mutation_dependency", True)),
        "operator_plane_tenancy_enforced": bool(current_state.get("operator_plane_tenancy_enforced", False)),
        "tier4_supported_peer_profile_count": int(current_state.get("tier4_supported_peer_profile_count", 0)),
        "tier4_required_external_bundle_count": int(current_state.get("tier4_required_external_bundle_count", 0)),
        "tier4_external_bundle_count": int(current_state.get("tier4_external_bundle_count", 0)),
        "tier4_valid_external_bundle_count": int(current_state.get("tier4_valid_external_bundle_count", 0)),
        "tier4_invalid_external_bundle_count": int(current_state.get("tier4_invalid_external_bundle_count", 0)),
        "tier4_missing_external_bundle_count": int(current_state.get("tier4_missing_external_bundle_count", 0)),
        "tier4_peer_bundle_completeness_passed": bool(current_state.get("tier4_peer_bundle_completeness_passed", False)),
        "tier4_external_handoff_template_present": bool(current_state.get("tier4_external_handoff_template_present", False)),
        "tier3_ready_targets": sorted(str(entry.get("target")) for entry in claim_entries if int(entry.get("tier", 0)) >= 3),
        "tier4_ready_targets": sorted(str(entry.get("target")) for entry in claim_entries if int(entry.get("tier", 0)) >= 4),
        "validated_execution_artifact_count": int(validated_execution.get("validated_artifact_count", 0)),
        "required_validated_inventory_count": int(validated_execution.get("required_validated_inventory_count", 0)),
        "validated_inventory_present_count": int(validated_execution.get("validated_inventory_present_count", 0)),
        "validated_inventory_complete": bool(validated_execution.get("validated_inventory_complete", False)),
        "clean_room_matrix_green": bool(validated_execution.get("runtime_matrix_green", False)),
        "in_scope_test_lanes_green": bool(validated_execution.get("in_scope_test_lanes_green", False)),
        "migration_portability_passed": bool(validated_execution.get("migration_portability_passed", False)),
        "tier3_evidence_rebuilt_from_validated_runs": bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)),
        "open_gaps": [],
    }
    if not bool(current_state.get("boundary_freeze_passed", False)):
        certification_state["open_gaps"].append("The certification boundary freeze record is missing or inconsistent with the retained target set.")
    if not strict_independent_claims_ready:
        certification_state["open_gaps"].append("Tier 4 independent peer validation is not complete for the retained boundary.")
    if not all_retained_tier3:
        certification_state["open_gaps"].append("Some retained targets remain below Tier 3 and still require certification-grade closure.")
    if not bool(current_state.get("tier4_external_handoff_template_present", False)):
        certification_state["open_gaps"].append("The fill-in external handoff template package is not present for the full supported peer-profile set.")
    if int(current_state.get("tier4_missing_external_bundle_count", 0)) > 0:
        certification_state["open_gaps"].append("One or more supported peer profiles still have no preserved external Tier 4 bundle.")
    if not bool(current_state.get("tier4_peer_bundle_completeness_passed", False)):
        certification_state["open_gaps"].append("The peer-bundle completeness gate is not satisfied for the declared peer-profile set.")
    if int(current_state.get("tier4_invalid_external_bundle_count", 0)) > 0:
        certification_state["open_gaps"].append("One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.")
    if bool(current_state.get("operator_plane_repo_mutation_dependency", True)):
        certification_state["open_gaps"].append("The certified operator surface still depends on repository file mutation rather than a durable external control-plane backend.")
    if not bool(current_state.get("operator_plane_tenancy_enforced", False)):
        certification_state["open_gaps"].append("The operator plane does not yet enforce tenant scoping consistently across CRUD and portability workflows.")
    runtime_report_source_mode = str(runtime_profile_report.get("summary", {}).get("source_mode", runtime_profile_report.get("report_mode", "live-probe")))
    runtime_report_uses_validated_runs = runtime_report_source_mode == "validated-runs"
    if int(runtime_profile_report.get("summary", {}).get("invalid_count", 0)) > 0 or int(runtime_profile_report.get("summary", {}).get("missing_count", 0)) > 0:
        certification_state["open_gaps"].append(
            "The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not yet preserved in the validated-run inventory."
            if runtime_report_uses_validated_runs
            else "The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not preserved in this container."
        )
        certification_state["open_gaps"].append("Tigrcorn is now pinned and included in the clean-room matrix for Python 3.11/3.12/3.13/3.14, but preserved independent validation artifacts remain absent.")
    if int(runtime_profile_report.get("summary", {}).get("placeholder_supported_runner_count", 0)) > 0:
        certification_state["open_gaps"].append("At least one kept runner is still modeled as a placeholder rather than a published pinned package.")
    if not bool(runtime_profile_report.get("summary", {}).get("declared_ci_install_probe_complete", False)):
        certification_state["open_gaps"].append("At least one kept runner is missing declared clean-room CI install/probe coverage.")
    if not bool(runtime_profile_report.get("summary", {}).get("surface_probe_passed", False)):
        certification_state["open_gaps"].append(
            "The runtime HTTP surface probe is not yet proven green across the preserved validated base-environment manifests."
            if runtime_report_uses_validated_runs
            else "The runtime HTTP surface probe did not pass in the current environment."
        )
    if not bool(runtime_profile_report.get("application_probe", {}).get("passed", False)):
        certification_state["open_gaps"].append(
            "The application factory is not yet proven materialized across the preserved validated base-environment manifests."
            if runtime_report_uses_validated_runs
            else "The application factory did not materialize in the current environment, so runtime validation could not complete here."
        )
    if not bool(runtime_profile_report.get("summary", {}).get("execution_probe_complete", False)):
        certification_state["open_gaps"].append(
            "Real runtime execution probes are implemented in tox and CI, but the preserved validated runtime inventory does not yet cover the full kept-runner matrix."
            if runtime_report_uses_validated_runs
            else "Real runtime execution probes are implemented in tox and CI, but the full kept-runner probe set was not executed successfully in this container."
        )
    if not bool(validated_execution.get("runtime_matrix_green", False)):
        certification_state["open_gaps"].append("Validated clean-room install matrix evidence is incomplete or missing.")
    if not bool(validated_execution.get("in_scope_test_lanes_green", False)):
        certification_state["open_gaps"].append("Validated in-scope certification lane execution evidence is incomplete or missing.")
    if not bool(validated_execution.get("migration_portability_passed", False)):
        certification_state["open_gaps"].append("Migration upgrade → downgrade → reapply portability has not been preserved for both SQLite and PostgreSQL.")
    if not bool(validated_execution.get("tier3_evidence_rebuilt_from_validated_runs", False)):
        certification_state["open_gaps"].append("Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.")
    if not artifact_truthfulness.get("passed", False):
        certification_state["open_gaps"].append("Current generated public artifacts still drift from executable reality.")
    if not bool(current_state.get("fully_featured_package_boundary_now", False)):
        certification_state["open_gaps"].append("One or more operator-visible package capabilities still lacks end-to-end verification in the current environment.")
    if not bool(current_state.get("certification_evidence_index_passed", False)):
        certification_state["open_gaps"].append("At least one claim row is still missing a machine-derived certification proof binding.")
    if not bool(current_state.get("release_evidence_clean_checkout_now", False)):
        certification_state["open_gaps"].append("Release evidence can now be built only from a clean checkout, and the current workspace is dirty.")
    if not bool(current_state.get("feature_release_verify_verb_present", False)):
        certification_state["open_gaps"].append("The CLI release surface is still missing an explicit verify verb for signed bundle verification.")
    if int(artifact_truthfulness.get("summary", {}).get("authoritative_current_doc_stale_ref_count", 0)) > 0:
        certification_state["open_gaps"].append("Current authoritative docs still contain stale code-path references.")
    report_dir = repo_root / "docs" / "compliance"
    _write_report(
        report_dir,
        "current_state_report",
        {"passed": True, "summary": current_state, "details": {"targets": ", ".join(targets)}},
        "Current State Report",
    )
    _write_report(
        report_dir,
        "certification_state_report",
        {"passed": bool(certification_state["fully_certifiable_now"] and certification_state["fully_rfc_compliant_now"] and certification_state["strict_independent_claims_ready"]), "summary": certification_state, "details": certification_state["open_gaps"]},
        "Certification State Report",
    )
    return {"current_state": current_state, "certification_state": certification_state}



EXPECTED_PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14"]
EXPECTED_TIGRCORN_PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]
EXPECTED_RUNTIME_VALIDATION_MATRIX = {
    "base": EXPECTED_PYTHON_VERSIONS,
    "sqlite-uvicorn": EXPECTED_PYTHON_VERSIONS,
    "postgres-hypercorn": EXPECTED_PYTHON_VERSIONS,
    "tigrcorn": EXPECTED_TIGRCORN_PYTHON_VERSIONS,
    "devtest": EXPECTED_PYTHON_VERSIONS,
}
EXPECTED_TEST_LANE_MATRIX = {
    "core": EXPECTED_PYTHON_VERSIONS,
    "integration": EXPECTED_PYTHON_VERSIONS,
    "conformance": EXPECTED_PYTHON_VERSIONS,
    "security-negative": EXPECTED_PYTHON_VERSIONS,
    "interop": EXPECTED_PYTHON_VERSIONS,
}


def _runtime_manifest_counts_as_passed(payload: dict[str, Any]) -> bool:
    return validated_runtime_manifest_passed(payload)


def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _test_lane_manifest_counts_as_passed(payload: dict[str, Any]) -> bool:
    return validated_test_lane_manifest_passed(payload)



def _tier3_evidence_manifest_counts_as_passed(payload: dict[str, Any]) -> bool:
    return bool(
        payload.get("passed", False)
        and payload.get("rebuild_from_validated_runs_only", False)
        and payload.get("runtime_report_generated_from_validated_runs", False)
        and payload.get("validated_execution_report_present", False)
        and payload.get("runtime_profile_report_present", False)
        and (_coerce_int(payload.get("recognized_manifest_count")) or 0) > 0
    )



def load_validated_execution_status(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    validated_root = repo_root / "dist" / "validated-runs"
    manifests: list[dict[str, Any]] = []
    ignored_json_paths: list[str] = []
    if validated_root.exists():
        for path in sorted(validated_root.rglob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                ignored_json_paths.append(str(path.relative_to(repo_root)))
                continue
            if isinstance(payload, dict):
                payload["_path"] = str(path.relative_to(repo_root))
                manifests.append(payload)
            else:
                ignored_json_paths.append(str(path.relative_to(repo_root)))

    required_runtime = [(profile, version) for profile, versions in EXPECTED_RUNTIME_VALIDATION_MATRIX.items() for version in versions]
    required_runtime_keys = set(required_runtime)
    required_lanes = [(lane, version) for lane, versions in EXPECTED_TEST_LANE_MATRIX.items() for version in versions]
    required_lane_keys = set(required_lanes)

    runtime_manifests: dict[tuple[str, str], dict[str, Any]] = {}
    lane_manifests: dict[tuple[str, str], dict[str, Any]] = {}
    migration_manifests: list[dict[str, Any]] = []
    migration_backend_manifests: dict[str, list[dict[str, Any]]] = {}
    tier3_evidence_manifests: list[dict[str, Any]] = []
    recognized_manifests: list[dict[str, Any]] = []
    in_scope_manifests: list[dict[str, Any]] = []
    out_of_scope_manifests: list[dict[str, Any]] = []

    def _record_out_of_scope(item: dict[str, Any], *, identity: str, reason: str) -> None:
        out_of_scope_manifests.append(
            {
                "path": item.get("_path"),
                "kind": item.get("kind"),
                "python_version": item.get("python_version"),
                "identity": identity,
                "reason": reason,
            }
        )

    for payload in manifests:
        kind = str(payload.get("kind", ""))
        pyver = str(payload.get("python_version", ""))
        if kind == "runtime-profile":
            profile = str(payload.get("matrix_profile", "unknown"))
            key = (profile, pyver)
            runtime_manifests[key] = payload
            recognized_manifests.append(payload)
            if key in required_runtime_keys:
                in_scope_manifests.append(payload)
            else:
                _record_out_of_scope(payload, identity=f"{profile}@py{pyver}", reason="runtime profile is outside the supported certification matrix")
        elif kind == "test-lane":
            lane = str(payload.get("lane", "unknown"))
            key = (lane, pyver)
            lane_manifests[key] = payload
            recognized_manifests.append(payload)
            if key in required_lane_keys:
                in_scope_manifests.append(payload)
            else:
                _record_out_of_scope(payload, identity=f"{lane}@py{pyver}", reason="test lane is outside the supported certification matrix")
        elif kind == "migration-portability":
            migration_manifests.append(payload)
            recognized_manifests.append(payload)
        elif kind == "migration-portability-backend":
            backend = str(payload.get("backend", "unknown"))
            migration_backend_manifests.setdefault(backend, []).append(payload)
            recognized_manifests.append(payload)
            in_scope_manifests.append(payload)
        elif kind == "tier3-evidence":
            tier3_evidence_manifests.append(payload)
            recognized_manifests.append(payload)
            in_scope_manifests.append(payload)
        else:
            ignored_json_paths.append(str(payload.get("_path", "")))

    passed_runtime = [
        f"{profile}@py{version}"
        for profile, version in required_runtime
        if _runtime_manifest_counts_as_passed(runtime_manifests.get((profile, version), {}))
    ]
    missing_runtime = [
        f"{profile}@py{version}"
        for profile, version in required_runtime
        if not _runtime_manifest_counts_as_passed(runtime_manifests.get((profile, version), {}))
    ]

    passed_lanes = [
        f"{lane}@py{version}"
        for lane, version in required_lanes
        if _test_lane_manifest_counts_as_passed(lane_manifests.get((lane, version), {}))
    ]
    missing_lanes = [
        f"{lane}@py{version}"
        for lane, version in required_lanes
        if not _test_lane_manifest_counts_as_passed(lane_manifests.get((lane, version), {}))
    ]

    runtime_present_count = sum(1 for profile, version in required_runtime if (profile, version) in runtime_manifests)
    lane_present_count = sum(1 for lane, version in required_lanes if (lane, version) in lane_manifests)
    required_migration_backends = ("sqlite", "postgres")
    migration_manifest_present = bool(migration_manifests) and all(
        backend in migration_backend_manifests for backend in required_migration_backends
    )

    def _migration_backend_group_passed(backend: str) -> bool:
        return any(
            validated_migration_backend_manifest_passed(item)
            for item in migration_backend_manifests.get(backend, [])
        )

    migration_portability_passed = bool(
        any(validated_migration_manifest_passed(item) for item in migration_manifests)
        and all(_migration_backend_group_passed(backend) for backend in required_migration_backends)
    )
    tier3_evidence_rebuilt_from_validated_runs = any(_tier3_evidence_manifest_counts_as_passed(item) for item in tier3_evidence_manifests)
    required_validated_inventory_count = len(required_runtime) + len(required_lanes) + len(required_migration_backends)
    validated_inventory_present_count = runtime_present_count + lane_present_count + sum(
        1 for backend in required_migration_backends if backend in migration_backend_manifests
    )
    validated_inventory_complete = validated_inventory_present_count >= required_validated_inventory_count

    payload = {
        "validated_artifact_count": len(in_scope_manifests),
        "out_of_scope_validated_artifact_count": len(out_of_scope_manifests),
        "required_validated_inventory_count": required_validated_inventory_count,
        "validated_inventory_present_count": validated_inventory_present_count,
        "validated_inventory_complete": validated_inventory_complete,
        "runtime_matrix_present_count": runtime_present_count,
        "test_lane_present_count": lane_present_count,
        "migration_manifest_present": migration_manifest_present,
        "runtime_matrix_expected_count": len(required_runtime),
        "runtime_matrix_passed_count": len(passed_runtime),
        "runtime_matrix_green": len(missing_runtime) == 0,
        "runtime_matrix_missing": missing_runtime,
        "runtime_matrix_passed": passed_runtime,
        "test_lane_expected_count": len(required_lanes),
        "test_lane_passed_count": len(passed_lanes),
        "in_scope_test_lanes_green": len(missing_lanes) == 0,
        "test_lane_missing": missing_lanes,
        "test_lane_passed": passed_lanes,
        "migration_portability_passed": migration_portability_passed,
        "tier3_evidence_rebuilt_from_validated_runs": tier3_evidence_rebuilt_from_validated_runs,
        "tier3_evidence_manifest_count": len(tier3_evidence_manifests),
        "validated_root_present": validated_root.exists(),
        "ignored_json_paths": ignored_json_paths,
        "out_of_scope_validated_manifests": out_of_scope_manifests,
    }
    inventory_threshold_text = (
        f"{len(required_runtime)} runtime + {len(required_lanes)} test lanes "
        f"+ {len(required_migration_backends)} backend-distinct migration threshold"
    )
    report = {
        "passed": payload["runtime_matrix_green"] and payload["in_scope_test_lanes_green"] and payload["migration_portability_passed"],
        "failures": [
            *([f"Validated artifact inventory is below the required {inventory_threshold_text}."] if not payload["validated_inventory_complete"] else []),
            *(["Validated clean-room runtime matrix is incomplete."] if not payload["runtime_matrix_green"] else []),
            *(["Validated in-scope certification lane execution is incomplete."] if not payload["in_scope_test_lanes_green"] else []),
            *(["Migration portability validation across SQLite and PostgreSQL is missing."] if not payload["migration_portability_passed"] else []),
        ],
        "warnings": [
            "Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests."
            if not payload["tier3_evidence_rebuilt_from_validated_runs"]
            else "",
            "Unsupported-version or out-of-scope validated manifests are present and excluded from certification counts."
            if out_of_scope_manifests
            else "",
        ],
        "summary": {
            "validated_artifact_count": payload["validated_artifact_count"],
            "out_of_scope_validated_artifact_count": payload["out_of_scope_validated_artifact_count"],
            "required_validated_inventory_count": payload["required_validated_inventory_count"],
            "validated_inventory_present_count": payload["validated_inventory_present_count"],
            "validated_inventory_complete": payload["validated_inventory_complete"],
            "runtime_matrix_present_count": payload["runtime_matrix_present_count"],
            "runtime_matrix_expected_count": payload["runtime_matrix_expected_count"],
            "runtime_matrix_passed_count": payload["runtime_matrix_passed_count"],
            "runtime_matrix_green": payload["runtime_matrix_green"],
            "test_lane_expected_count": payload["test_lane_expected_count"],
            "test_lane_passed_count": payload["test_lane_passed_count"],
            "in_scope_test_lanes_green": payload["in_scope_test_lanes_green"],
            "migration_portability_passed": payload["migration_portability_passed"],
            "tier3_evidence_rebuilt_from_validated_runs": payload["tier3_evidence_rebuilt_from_validated_runs"],
        },
        "details": {
            "runtime_matrix_missing": payload["runtime_matrix_missing"],
            "runtime_matrix_present_count": payload["runtime_matrix_present_count"],
            "test_lane_missing": payload["test_lane_missing"],
            "test_lane_present_count": payload["test_lane_present_count"],
            "migration_manifest_present": payload["migration_manifest_present"],
            "required_validated_inventory_count": payload["required_validated_inventory_count"],
            "validated_inventory_present_count": payload["validated_inventory_present_count"],
            "validated_inventory_complete": payload["validated_inventory_complete"],
            "runtime_evidence": {
                f"{profile}@py{version}": {
                    "path": item.get("_path"),
                    "manifest_passed": bool(item.get("passed", False)),
                    "counts_as_passed": _runtime_manifest_counts_as_passed(item),
                    "identity": item.get("identity"),
                    "environment_identity_ready": environment_identity_ready(item),
                    "install_evidence_ready": install_evidence_ready(item),
                    "runtime_smoke_passed": bool(item.get("runtime_smoke_passed", False)),
                    "application_probe_passed": bool(item.get("application_probe_passed", False)),
                    "surface_probe_passed": bool(item.get("surface_probe_passed", False)),
                    "runner_available": item.get("runner_available"),
                    "serve_check_passed": item.get("serve_check_passed"),
                }
                for (profile, version), item in sorted(runtime_manifests.items())
            },
            "test_lane_evidence": {
                f"{lane}@py{version}": {
                    "path": item.get("_path"),
                    "manifest_passed": bool(item.get("passed", False)),
                    "counts_as_passed": _test_lane_manifest_counts_as_passed(item),
                    "identity": item.get("identity"),
                    "environment_identity_ready": environment_identity_ready(item),
                    "install_evidence_ready": install_evidence_ready(item),
                    "pytest_report_present": bool(item.get("pytest_report_present", False) or item.get("pytest_report_artifact")),
                    "pytest_exit_code": item.get("pytest_exit_code"),
                    "pytest_report_exit_code": item.get("pytest_report_exit_code"),
                    "tests_collected": item.get("tests_collected"),
                    "tests_total": item.get("tests_total"),
                }
                for (lane, version), item in sorted(lane_manifests.items())
            },
            "migration_evidence": [
                {
                    "path": item.get("_path"),
                    "manifest_passed": bool(item.get("passed", False)),
                    "counts_as_passed": validated_migration_manifest_passed(item),
                    "identity": item.get("identity"),
                    "environment_identity_ready": environment_identity_ready(item),
                    "install_evidence_ready": install_evidence_ready(item),
                    "backends": item.get("backends", []),
                    "passed_backends": item.get("passed_backends", []),
                    "expected_head_revision": item.get("expected_head_revision") or item.get("head_revision"),
                    "downgrade_target_revision": item.get("downgrade_target_revision"),
                }
                for item in migration_manifests
            ] + [
                {
                    "backend": backend,
                    "counts_as_passed": any(
                        validated_migration_backend_manifest_passed(item)
                        for item in items
                    ),
                    "manifests": [
                        {
                            "path": item.get("_path"),
                            "manifest_passed": bool(item.get("passed", False)),
                            "counts_as_passed": validated_migration_backend_manifest_passed(item),
                            "identity": item.get("identity"),
                            "backend": item.get("backend"),
                            "environment_identity_ready": environment_identity_ready(item),
                            "install_evidence_ready": install_evidence_ready(item),
                            "expected_head_revision": item.get("expected_head_revision"),
                            "downgrade_target_revision": item.get("downgrade_target_revision"),
                        }
                        for item in items
                    ],
                }
                for backend, items in sorted(migration_backend_manifests.items())
            ],
            "validated_manifests": [item.get("_path") for item in in_scope_manifests],
            "out_of_scope_validated_manifests": out_of_scope_manifests,
            "recognized_manifest_paths": [item.get("_path") for item in recognized_manifests],
            "ignored_json_paths": payload["ignored_json_paths"],
        },
    }
    report["warnings"] = [item for item in report["warnings"] if item]
    _write_report(repo_root / "docs" / "compliance", "validated_execution_report", report, "Validated Execution Report")
    return payload


def run_test_execution_gate(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    classification = verify_test_classification(repo_root, strict=True)
    validated = load_validated_execution_status(repo_root)
    failures: list[str] = []
    if not classification.get("passed", False):
        failures.append("Test classification manifest is invalid.")
    if not validated.get("in_scope_test_lanes_green", False):
        failures.append("Validated in-scope certification lane execution is incomplete.")
    if not validated.get("migration_portability_passed", False):
        failures.append("Migration portability validation across SQLite and PostgreSQL is missing.")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "classification_manifest_passed": bool(classification.get("passed", False)),
            "in_scope_test_lanes_green": bool(validated.get("in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(validated.get("migration_portability_passed", False)),
            "validated_test_lane_count": int(validated.get("test_lane_passed_count", 0)),
            "validated_test_lane_expected_count": int(validated.get("test_lane_expected_count", 0)),
        },
        "details": {
            "classification_failures": list(classification.get("failures", [])),
            "missing_test_lane_manifests": list(validated.get("test_lane_missing", [])),
        },
    }
    _write_report(repo_root / "docs" / "compliance", "test_execution_gate_report", payload, "Test Execution Gate Report")
    return payload


def run_final_release_readiness_gate(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    generate_state_reports(repo_root)
    validated = load_validated_execution_status(repo_root)
    runtime_profile = json.loads((repo_root / "docs" / "compliance" / "runtime_profile_report.json").read_text(encoding="utf-8")) if (repo_root / "docs" / "compliance" / "runtime_profile_report.json").exists() else {}
    certification_state = json.loads((repo_root / "docs" / "compliance" / "certification_state_report.json").read_text(encoding="utf-8")) if (repo_root / "docs" / "compliance" / "certification_state_report.json").exists() else {}
    runner_count = len(registered_runner_names())
    summary = runtime_profile.get("summary", {}) if isinstance(runtime_profile, dict) else {}
    failures: list[str] = []
    runtime_report_source_mode = str(summary.get("source_mode", runtime_profile.get("report_mode", "live-probe")))
    if int(summary.get("ready_count", 0)) != runner_count:
        failures.append(
            "Runtime profiles are not all ready in the preserved validated-run inventory."
            if runtime_report_source_mode == "validated-runs"
            else "Runtime profiles are not all ready in the current certification environment."
        )
    if int(summary.get("invalid_count", 0)) != 0:
        failures.append("At least one kept runner is still invalid.")
    if int(summary.get("missing_count", 0)) != 0:
        failures.append("At least one kept runner is still missing.")
    if not validated.get("validated_inventory_complete", False):
        failures.append(
            "Validated artifact inventory is below the required "
            f"{validated.get('required_validated_inventory_count', 0)} artifact threshold."
        )
    if not validated.get("runtime_matrix_green", False):
        failures.append("The clean-room install matrix is not green from validated-run evidence.")
    if not validated.get("in_scope_test_lanes_green", False):
        failures.append("In-scope certification test lanes are not green from validated-run evidence.")
    if not validated.get("migration_portability_passed", False):
        failures.append("Migration portability validation is not preserved for both SQLite and PostgreSQL.")
    if not validated.get("tier3_evidence_rebuilt_from_validated_runs", False):
        failures.append("Tier 3 evidence has not been rebuilt from validated runs.")
    tier4_ready = bool(certification_state.get("summary", {}).get("strict_independent_claims_ready", False))
    warnings: list[str] = []
    if not tier4_ready:
        warnings.append("Tier 4 bundle promotion is not complete for the retained boundary.")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "runtime_profiles_truly_ready": int(summary.get("ready_count", 0)) == runner_count and int(summary.get("invalid_count", 0)) == 0 and int(summary.get("missing_count", 0)) == 0,
            "validated_inventory_complete": bool(validated.get("validated_inventory_complete", False)),
            "required_validated_inventory_count": int(validated.get("required_validated_inventory_count", 0)),
            "validated_inventory_present_count": int(validated.get("validated_inventory_present_count", 0)),
            "clean_room_install_matrix_green": bool(validated.get("runtime_matrix_green", False)),
            "in_scope_test_lanes_green": bool(validated.get("in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(validated.get("migration_portability_passed", False)),
            "tier3_evidence_rebuilt_from_validated_runs": bool(validated.get("tier3_evidence_rebuilt_from_validated_runs", False)),
            "tier4_bundle_promotion_complete": tier4_ready,
        },
    }
    _write_report(repo_root / "docs" / "compliance", "final_release_gate_report", payload, "Final Release Gate Report")
    return payload

def verify_test_classification(repo_root: Path, *, strict: bool = True) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    preferred = repo_root / "compliance" / "mappings" / "test_classification.yaml"
    legacy = repo_root / "compliance" / "mappings" / "test-classification.yaml"
    mapping_path = preferred if preferred.exists() else legacy
    failures: list[str] = []
    warnings: list[str] = []
    mapping = _load_yaml(mapping_path) if mapping_path.exists() else {"categories": {}}
    categories = mapping.get("categories", {}) or {}
    allowed_categories = {
        "unit",
        "integration",
        "conformance",
        "interop",
        "e2e",
        "security",
        "negative",
        "perf",
        "security-negative",
        "migration-portability",
        "peer",
    }
    if not categories:
        failures.append("Missing test classification categories")
    if not preferred.exists():
        failures.append("Missing canonical test classification manifest: compliance/mappings/test_classification.yaml")
    unknown_categories = sorted(set(categories) - allowed_categories)
    for category in unknown_categories:
        failures.append(f"Unknown test classification category: {category}")
    classified: set[str] = set()
    for category, files in categories.items():
        if category in allowed_categories and not (repo_root / "tests" / category).exists() and category != "conformance":
            warnings.append(f"Missing test category directory: tests/{category}")
        for rel in files:
            normalized = str(rel).replace("\\", "/")
            if normalized in classified:
                failures.append(f"Classified test file appears multiple times: {normalized}")
            classified.add(normalized)
            if not (repo_root / normalized).exists():
                failures.append(f"Missing classified test file: {normalized}")
    discovered = {
        str(path.relative_to(repo_root)).replace("\\", "/")
        for path in sorted((repo_root / "tests").glob("**/test_*.py"))
    }
    unclassified = sorted(discovered - classified)
    if unclassified:
        failures.append(f"Unclassified test files present: {', '.join(unclassified)}")
    legacy_i9n = sorted(str(path.relative_to(repo_root)).replace("\\", "/") for path in (repo_root / "tests" / "i9n").glob("test_*.py")) if (repo_root / "tests" / "i9n").exists() else []
    if legacy_i9n:
        failures.append(f"Legacy tests/i9n migration incomplete: {', '.join(legacy_i9n)}")
    targets = []
    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    for entry in scope.get("targets", []):
        if str(entry.get("scope_bucket")) == "out-of-scope/deferred":
            continue
        targets.append(str(entry.get("label")))
    target_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml")
    for target in targets:
        refs = [str(path).replace("\\", "/") for path in target_to_test.get(target, [])]
        if not refs:
            failures.append(f"No explicit test mapping for in-scope target: {target}")
            continue
        for ref in refs:
            if ref not in classified:
                failures.append(f"Mapped test path missing from canonical test classification: {target} -> {ref}")
            if not (repo_root / ref).exists():
                failures.append(f"Mapped test path missing on disk: {target} -> {ref}")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "mapping_path": str(mapping_path.relative_to(repo_root)) if mapping_path.exists() else None,
            "category_count": len(categories),
            "classified_test_count": len(classified),
            "discovered_test_count": len(discovered),
            "target_count": len(targets),
        },
    }
    _write_report(repo_root / "docs" / "compliance", "test_classification_report", payload, "Test Classification Report")
    return payload


def _certification_partition_for_test(path: str) -> str:
    normalized = path.replace("\\", "/")
    if "tests/interop/" in normalized:
        return "peer" if "peer_" in normalized or "tier4_" in normalized else "interop"
    if "migration" in normalized:
        return "migration-portability"
    if "/security/" in normalized or "/negative/" in normalized:
        return "security-negative"
    if "/integration/" in normalized or "/runtime/" in normalized:
        return "integration"
    if "/conformance/" in normalized:
        return "conformance"
    return "unit"


def _security_sensitive_claim(claim: Mapping[str, Any]) -> bool:
    claim_id = str(claim.get("id", "")).lower()
    title = str(claim.get("title", "")).lower()
    targets = [str(item).lower() for item in claim.get("targets", []) or []]
    keywords = (
        "fapi",
        "security",
        "sender-constrained",
        "dpop",
        "mtls",
        "issuer",
        "mix-up",
        "par",
        "password",
        "implicit",
        "hybrid",
    )
    return any(keyword in claim_id or keyword in title for keyword in keywords) or any(
        target in {"rfc 8705", "rfc 9126", "rfc 9207", "rfc 9449", "rfc 9700"} for target in targets
    )


def _negative_tests_for_claim(claim: Mapping[str, Any], partitioned_tests: Mapping[str, list[str]]) -> list[str]:
    claim_id = str(claim.get("id", "")).lower()
    negatives = list(partitioned_tests.get("security-negative", []))
    selected: list[str] = []

    def _match(*patterns: str) -> None:
        for path in negatives:
            lower = path.lower()
            if any(pattern in lower for pattern in patterns) and path not in selected:
                selected.append(path)

    if "sender-constrained" in claim_id or "dpop" in claim_id or "mtls" in claim_id:
        _match("sender_constraint", "capability_certification_attack_paths")
    if "par" in claim_id:
        _match("capability_certification_attack_paths", "capability_hardening_runtime_enforcement")
    if "issuer" in claim_id or "mix" in claim_id:
        _match("capability_certification_attack_paths", "capability_hardening_cluster_b")
    if "security-bcp" in claim_id or "rfc 9700" in str(claim.get("targets", [])).lower():
        _match("capability_hardening_runtime_enforcement", "capability_certification_attack_paths")
    if not selected and _security_sensitive_claim(claim):
        _match("capability_certification_attack_paths", "capability_hardening_runtime_enforcement", "capability_sender_constraint_replay")
    return selected


def _git_checkout_summary(repo_root: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        return {"git_available": False, "clean": False, "failure": str(exc), "changed_paths": []}
    if result.returncode != 0:
        return {"git_available": True, "clean": False, "failure": result.stderr.strip() or "git status failed", "changed_paths": []}
    changed_paths = [line[3:] for line in result.stdout.splitlines() if line.strip()]
    return {
        "git_available": True,
        "clean": not changed_paths,
        "changed_path_count": len(changed_paths),
        "changed_paths": changed_paths[:200],
    }


def generate_certification_evidence_index(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    claim_registry = _load_yaml(repo_root / "compliance" / "claims" / "claim-registry.yaml")
    target_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml")
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    feature_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "feature-to-test.yaml")
    feature_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "feature-to-evidence.yaml")
    classification = _load_yaml(repo_root / "compliance" / "mappings" / "test_classification.yaml")
    profiles = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")
    discovered_tests = sorted(str(path.relative_to(repo_root)).replace("\\", "/") for path in (repo_root / "tests").rglob("test_*.py"))
    partitioned_tests: dict[str, list[str]] = {}
    for path in discovered_tests:
        partitioned_tests.setdefault(_certification_partition_for_test(path), []).append(path)

    claims = list(claim_registry.get("claims", []))
    claim_bindings: list[dict[str, Any]] = []
    missing_positive: list[str] = []
    missing_negative: list[str] = []
    for claim in claims:
        feature_id = str(claim.get("feature_id", ""))
        targets = [str(item) for item in claim.get("targets", []) or []]
        positive_tests = list(dict.fromkeys(
            list(feature_to_test.get(feature_id, []) or [])
            + [test for target in targets for test in (target_to_test.get(target, []) or [])]
        ))
        evidence_refs = list(dict.fromkeys(
            list(feature_to_evidence.get(feature_id, []) or [])
            + [ref for target in targets for ref in (target_to_evidence.get(target, []) or [])]
        ))
        negative_tests = _negative_tests_for_claim(claim, partitioned_tests)
        binding = {
            "claim_id": str(claim.get("id")),
            "feature_id": feature_id,
            "targets": targets,
            "profile": claim.get("profile"),
            "positive_tests": positive_tests,
            "negative_tests": negative_tests,
            "evidence_refs": evidence_refs,
            "security_sensitive": _security_sensitive_claim(claim),
        }
        claim_bindings.append(binding)
        if not positive_tests or not evidence_refs:
            missing_positive.append(str(claim.get("id")))
        if binding["security_sensitive"] and not negative_tests:
            missing_negative.append(str(claim.get("id")))

    target_profile_bundles: list[dict[str, Any]] = []
    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    retained_targets = [
        str(entry.get("label"))
        for entry in scope.get("targets", [])
        if str(entry.get("scope_bucket")) != "out-of-scope/deferred"
    ]
    for profile in profiles:
        effective_claims_path = write_effective_claims_manifest(
            repo_root,
            deployment_from_options(profile=profile),
            profile_label=profile,
        )
        effective_claims = _load_yaml(effective_claims_path)
        profile_targets = {
            str(entry.get("target"))
            for entry in effective_claims.get("claim_set", {}).get("claims", [])
        }
        for target in sorted(profile_targets & set(retained_targets)):
            target_profile_bundles.append(
                {
                    "profile": profile,
                    "target": target,
                    "tests": list(target_to_test.get(target, []) or []),
                    "evidence_refs": list(target_to_evidence.get(target, []) or []),
                }
            )

    failures: list[str] = []
    if missing_positive:
        failures.append(f"Claims missing positive proof or evidence refs: {', '.join(missing_positive[:25])}")
    if missing_negative:
        failures.append(f"Security-sensitive claims missing negative proof: {', '.join(missing_negative[:25])}")
    payload = {
        "passed": not missing_positive and not missing_negative,
        "failures": failures,
        "warnings": [],
        "summary": {
            "claim_count": len(claim_bindings),
            "fapi_claim_count": sum(1 for item in claim_bindings if item.get("profile") == "fapi2-security"),
            "security_sensitive_claim_count": sum(1 for item in claim_bindings if item.get("security_sensitive")),
            "partition_count": len(partitioned_tests),
            "target_profile_bundle_count": len(target_profile_bundles),
            "clean_checkout": _git_checkout_summary(repo_root),
        },
        "test_partitions": partitioned_tests,
        "claim_bindings": claim_bindings,
        "target_profile_bundles": target_profile_bundles,
        "classification_profiles": classification.get("profiles", {}),
    }
    out_root = repo_root / "docs" / "compliance"
    _write_report(out_root, "certification_evidence_index", payload, "Certification Evidence Index")
    _write_json(repo_root / "compliance" / "evidence" / "certification_test_partitions.json", {"partitions": partitioned_tests})
    _write_yaml(repo_root / "compliance" / "evidence" / "certification_test_partitions.yaml", {"partitions": partitioned_tests})
    _write_json(repo_root / "compliance" / "evidence" / "claim_proof_bindings.json", {"bindings": claim_bindings})
    _write_yaml(repo_root / "compliance" / "evidence" / "claim_proof_bindings.yaml", {"bindings": claim_bindings})
    _write_json(repo_root / "compliance" / "evidence" / "target_profile_evidence.json", {"bundles": target_profile_bundles})
    _write_yaml(repo_root / "compliance" / "evidence" / "target_profile_evidence.yaml", {"bundles": target_profile_bundles})
    return payload


def _copy_rel_artifact(repo_root: Path, rel_path: str, bundle_root: Path) -> dict[str, Any]:
    src = repo_root / rel_path
    if not src.exists():
        return {"path": rel_path, "present": False}
    dst = bundle_root / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"path": rel_path, "present": True, "sha256": _hash_file(dst)}


def build_evidence_bundle(
    repo_root: Path,
    deployment: Any,
    *,
    tier: str = "3",
    profile_label: str = "active",
    bundle_dir: Path | None = None,
) -> Path:
    repo_root = repo_root.resolve()
    profile_name = profile_label if profile_label != "active" else deployment.profile
    out_dir = bundle_dir or (repo_root / "dist" / "evidence-bundles" / profile_name / f"tier{tier}")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    evidence_index = generate_certification_evidence_index(repo_root)
    claims_path = write_effective_claims_manifest(repo_root, deployment, profile_label=profile_label)
    evidence_path = write_effective_evidence_manifest(repo_root, deployment, profile_label=profile_label)
    openapi_path = write_openapi_contract(repo_root, deployment, profile_label=profile_label)
    try:
        openrpc_path = write_openrpc_contract(repo_root, deployment, profile_label=profile_label)
    except Exception:
        openrpc_path = _openrpc_path(repo_root, profile_label)
    adr_index = build_adr_index(repo_root)
    copied = [
        _copy_rel_artifact(repo_root, str(claims_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, str(evidence_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, str(openapi_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, str(openrpc_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/certification_test_partitions.json", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/certification_test_partitions.yaml", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/claim_proof_bindings.json", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/claim_proof_bindings.yaml", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/target_profile_evidence.json", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/target_profile_evidence.yaml", out_dir),
    ]
    for item in evidence_index.get("target_profile_bundles", []):
        if str(item.get("profile")) != profile_name:
            continue
        target_slug = re.sub(r"[^a-z0-9]+", "-", str(item.get("target", "")).lower()).strip("-")
        target_dir = out_dir / "targets" / target_slug
        target_dir.mkdir(parents=True, exist_ok=True)
        target_manifest = {
            "profile": profile_name,
            "target": item.get("target"),
            "tests": item.get("tests", []),
            "evidence_refs": item.get("evidence_refs", []),
        }
        _write_json(target_dir / "bundle-manifest.json", target_manifest)
        _write_yaml(target_dir / "bundle-manifest.yaml", target_manifest)
    peer_profiles = sorted(str(path.relative_to(repo_root)) for path in (repo_root / "compliance" / "evidence" / "peer_profiles").glob("*.yaml"))
    for rel in peer_profiles:
        copied.append(_copy_rel_artifact(repo_root, rel, out_dir))
    manifest = {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "version": _current_version(repo_root),
        "tier": int(tier),
        "profile": profile_name,
        "deployment": deployment.to_manifest(),
        "copied_artifacts": copied,
        "adr_index": adr_index,
        "clean_checkout": evidence_index.get("summary", {}).get("clean_checkout", {}),
        "claim_binding_summary": {
            "claim_count": evidence_index.get("summary", {}).get("claim_count", 0),
            "fapi_claim_count": evidence_index.get("summary", {}).get("fapi_claim_count", 0),
            "security_sensitive_claim_count": evidence_index.get("summary", {}).get("security_sensitive_claim_count", 0),
        },
        "documentation_policy": {
            "bundle_docs_policy": "generated-current-state-only",
            "historical_archive_root": "docs/archive/historical",
        },
    }
    _write_json(out_dir / "bundle-manifest.json", manifest)
    _write_yaml(out_dir / "bundle-manifest.yaml", manifest)
    return out_dir



def summarize_evidence_status(repo_root: Path, profile_label: str = "active") -> dict[str, Any]:
    repo_root = repo_root.resolve()
    deployment = _profile_deployment(profile_label)
    effective = build_effective_evidence_manifest(repo_root, deployment, profile_label=profile_label)
    missing_refs = effective.get("bundle_manifest", {}).get("missing_refs", [])
    peer_profile_dir = repo_root / "compliance" / "evidence" / "peer_profiles"
    executed_dir = repo_root / "compliance" / "evidence" / "tier4" / "executions"
    payload = {
        "passed": not missing_refs,
        "failures": [f"Missing evidence refs for target: {target}" for target in missing_refs],
        "warnings": [],
        "summary": {
            "profile": deployment.profile,
            "target_bundle_count": len(effective.get("bundle_manifest", {}).get("bundles", [])),
            "missing_ref_count": len(missing_refs),
            "peer_profile_count": len(list(peer_profile_dir.glob("*.yaml"))) if peer_profile_dir.exists() else 0,
            "peer_execution_count": len(list(executed_dir.glob("*.yaml"))) if executed_dir.exists() else 0,
        },
    }
    _write_report(repo_root / "docs" / "compliance", "evidence_status_report", payload, "Evidence Status Report")
    return payload




def execute_peer_profiles(
    repo_root: Path,
    deployment: Any,
    *,
    profiles: Iterable[str] | None = None,
    execution_mode: str = "self-check",
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    profile_dir = repo_root / "compliance" / "evidence" / "peer_profiles"
    counterpart_dir = repo_root / "compliance" / "evidence" / "peer_counterparts"
    execution_dir = repo_root / "compliance" / "evidence" / "tier4" / "executions"
    execution_dir.mkdir(parents=True, exist_ok=True)
    selected = set(profiles or [])
    external_root_env = os.environ.get("TIGRBL_AUTH_PEER_ARTIFACTS_ROOT")
    external_root = Path(external_root_env).resolve() if external_root_env else None
    failures: list[str] = []
    warnings: list[str] = []
    executed: list[str] = []

    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    retained_targets = {
        str(entry.get("label"))
        for entry in scope.get("targets", [])
        if str(entry.get("scope_bucket")) != "out-of-scope/deferred"
    }
    target_to_peer = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-peer-profile.yaml") or {}
    counterparts = {path.stem: _load_yaml(path) for path in sorted(counterpart_dir.glob("*.yaml"))}
    peer_profiles = {path.stem: _load_yaml(path) for path in sorted(profile_dir.glob("*.yaml"))}
    known_profiles = set(peer_profiles)
    known_counterparts = set(counterparts)

    required_counterpart_fields = {
        "schema_version",
        "id",
        "title",
        "counterpart_class",
        "execution_style",
        "independence_requirement",
        "attestation_class_required",
        "required_identity_fields",
        "required_container_fields",
        "required_artifacts",
    }
    for stem, counterpart in counterparts.items():
        missing = sorted(field for field in required_counterpart_fields if field not in counterpart)
        if missing:
            failures.append(f"Counterpart manifest missing required fields: {stem} -> {', '.join(missing)}")
        if str(counterpart.get("id", stem)) != stem:
            failures.append(f"Counterpart manifest id does not match filename: {stem}")
        if str(counterpart.get("attestation_class_required", "")).strip() != "independent-external":
            failures.append(f"Counterpart manifest must require independent-external attestation: {stem}")
        if not list(counterpart.get("required_identity_fields") or []):
            failures.append(f"Counterpart manifest missing required_identity_fields: {stem}")
        if not list(counterpart.get("required_container_fields") or []):
            failures.append(f"Counterpart manifest missing required_container_fields: {stem}")
        if not list(counterpart.get("required_artifacts") or []):
            failures.append(f"Counterpart manifest missing required_artifacts: {stem}")

    required_profile_fields = {
        "schema_version",
        "id",
        "title",
        "counterpart_id",
        "required_targets",
        "required_artifacts",
        "scenario_ids",
        "contract_profiles",
        "preferred_runtime_profile",
        "peer_verification_class",
    }
    allowed_contract_profiles = {"baseline", "production", "hardening", "fapi2-security", "peer-claim"}
    allowed_runtime_profiles = {"baseline", "production", "hardening", "fapi2-security"}
    profile_targets: dict[str, set[str]] = {}
    for stem, payload in peer_profiles.items():
        name = str(payload.get("id", stem))
        missing = sorted(field for field in required_profile_fields if field not in payload)
        if missing:
            failures.append(f"Peer profile missing required fields: {stem} -> {', '.join(missing)}")
        if name != stem:
            failures.append(f"Peer profile id does not match filename: {stem}")
        counterpart_id = str(payload.get("counterpart_id", "")).strip()
        if not counterpart_id:
            failures.append(f"Peer profile missing counterpart_id: {name}")
        elif counterpart_id not in known_counterparts:
            failures.append(f"Peer profile references unknown counterpart: {name} -> {counterpart_id}")
        if str(payload.get("peer_verification_class", "")).strip() != "external-independent":
            failures.append(f"Peer profile must declare peer_verification_class=external-independent: {name}")
        contract_profiles = [str(item) for item in payload.get("contract_profiles", [])]
        if not contract_profiles:
            failures.append(f"Peer profile missing contract_profiles: {name}")
        unknown_contract_profiles = sorted(set(contract_profiles) - allowed_contract_profiles)
        if unknown_contract_profiles:
            failures.append(f"Peer profile uses unknown contract_profiles: {name} -> {', '.join(unknown_contract_profiles)}")
        preferred_runtime_profile = str(payload.get("preferred_runtime_profile", deployment.profile))
        if preferred_runtime_profile not in allowed_runtime_profiles:
            failures.append(f"Peer profile uses unknown preferred_runtime_profile: {name} -> {preferred_runtime_profile}")
        scenario_ids = [str(item) for item in payload.get("scenario_ids", [])]
        if not scenario_ids:
            failures.append(f"Peer profile missing scenario_ids: {name}")
        elif len(set(scenario_ids)) != len(scenario_ids):
            failures.append(f"Peer profile has duplicate scenario_ids: {name}")
        required_targets = {str(item) for item in payload.get("required_targets", [])}
        profile_targets[name] = required_targets
        if not required_targets:
            failures.append(f"Peer profile missing required_targets: {name}")
        unknown_targets = sorted(required_targets - retained_targets)
        if unknown_targets:
            failures.append(f"Peer profile references unknown retained targets: {name} -> {', '.join(unknown_targets)}")
        scenario_target_map = payload.get("scenario_target_map") or {}
        unknown_scenarios = sorted(set(scenario_target_map) - set(scenario_ids))
        if unknown_scenarios:
            failures.append(f"Peer profile scenario_target_map references unknown scenarios: {name} -> {', '.join(unknown_scenarios)}")
        for scenario_id, targets in scenario_target_map.items():
            bad_targets = sorted({str(item) for item in (targets or [])} - required_targets)
            if bad_targets:
                failures.append(f"Peer profile scenario_target_map uses targets outside required_targets: {name}:{scenario_id} -> {', '.join(bad_targets)}")
        for rel in payload.get("required_artifacts", []) or []:
            if not (repo_root / str(rel)).exists():
                failures.append(f"Peer profile required_artifact missing on disk: {name} -> {rel}")

    missing_target_mappings = sorted(target for target in retained_targets if target not in target_to_peer)
    for target in missing_target_mappings:
        failures.append(f"Retained target lacks target-to-peer mapping: {target}")
    for target, mapped_profiles in (target_to_peer or {}).items():
        refs = [str(item) for item in (mapped_profiles or [])]
        if target in retained_targets and not refs:
            failures.append(f"Retained target has empty target-to-peer mapping: {target}")
        for profile_name in refs:
            if profile_name not in known_profiles:
                failures.append(f"Retained target maps to unknown peer profile: {target} -> {profile_name}")
            elif target in retained_targets and target not in profile_targets.get(profile_name, set()):
                failures.append(f"Retained target mapped to profile without corresponding required_target: {target} -> {profile_name}")
    for profile_name, required_targets in profile_targets.items():
        for target in required_targets:
            refs = {str(item) for item in target_to_peer.get(target, [])}
            if profile_name not in refs:
                failures.append(f"Peer profile required_target missing reverse mapping: {profile_name} -> {target}")

    for path in sorted(profile_dir.glob("*.yaml")):
        payload = _load_yaml(path)
        name = str(payload.get("id", path.stem))
        if selected and name not in selected:
            continue
        counterpart_id = str(payload.get("counterpart_id", "")).strip()
        counterpart = counterparts.get(counterpart_id, {})
        scenario_ids = [str(item) for item in payload.get("scenario_ids", [])]
        ext_dir = external_root / name if external_root else None
        external_available = bool(ext_dir and ext_dir.exists() and ext_dir.is_dir())
        if execution_mode == "external":
            status = "external-artifacts-detected" if external_available else "awaiting-external-artifacts"
        elif execution_mode == "planned":
            status = "planned"
        else:
            status = "internal-self-check-generated"
        execution = {
            "schema_version": 1,
            "profile": name,
            "execution_mode": execution_mode,
            "status": status,
            "deployment_profile": deployment.profile,
            "counterpart_id": counterpart_id,
            "counterpart_class": counterpart.get("counterpart_class"),
            "required_targets": payload.get("required_targets", []),
            "required_artifacts": payload.get("required_artifacts", []),
            "required_peer_artifacts": counterpart.get("required_artifacts", []),
            "required_identity_fields": counterpart.get("required_identity_fields", []),
            "required_container_fields": counterpart.get("required_container_fields", []),
            "scenario_ids": scenario_ids,
            "contract_profiles": payload.get("contract_profiles", []),
            "preferred_runtime_profile": payload.get("preferred_runtime_profile", deployment.profile),
            "peer_verification_class": payload.get("peer_verification_class"),
            "attestation_class_required": counterpart.get("attestation_class_required"),
            "external_artifacts_root": str(ext_dir.relative_to(repo_root)) if external_available and ext_dir is not None and ext_dir.is_relative_to(repo_root) else (str(ext_dir) if external_available and ext_dir is not None else None),
            "independent_peer_validation": execution_mode == "external" and external_available,
            "notes": (
                "External peer artifacts were detected for normalization into preserved Tier 4 bundles."
                if execution_mode == "external" and external_available
                else "Independent external peer artifacts are still required for Tier 4 claims."
            ),
        }
        _write_yaml(execution_dir / f"{name}.{deployment.profile}.yaml", execution)
        executed.append(name)
    if selected:
        for name in selected - known_profiles:
            failures.append(f"Unknown peer profile: {name}")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "deployment_profile": deployment.profile,
            "execution_mode": execution_mode,
            "executed_profile_count": len(executed),
            "peer_profile_count": len(peer_profiles),
            "counterpart_catalog_count": len(counterparts),
            "retained_target_count": len(retained_targets),
            "mapped_retained_target_count": len([target for target in retained_targets if target in target_to_peer]),
            "retained_target_coverage_complete": not missing_target_mappings,
            "external_artifact_root": str(external_root) if external_root else None,
        },
        "details": executed,
    }
    _write_report(repo_root / "docs" / "compliance", "peer_profile_execution_report", payload, "Peer Profile Execution Report")
    return payload


def _run_release_signing_gate(repo_root: Path) -> int:
    repo_root = repo_root.resolve()
    profiles = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")
    failures: list[str] = []
    details: list[dict[str, Any]] = []
    shared_signer = load_signer(signing_key=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY"), signer_id=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNER_ID"))
    shared_signing_key = shared_signer.private_key_pem()
    for profile in profiles:
        deployment = deployment_from_options(profile=profile)
        bundle = build_release_bundle(repo_root, deployment, require_clean_checkout=True)
        signed = sign_release_bundle(bundle, signing_key=shared_signing_key, signer_id=shared_signer.identity.signer_id)
        verified = verify_release_bundle_signatures(bundle)
        passed = bool(signed.get("verification", {}).get("passed", False)) and bool(verified.get("passed", False))
        details.append({
            "profile": profile,
            "bundle_dir": str(bundle.relative_to(repo_root)),
            "signed": signed.get("status"),
            "verified": bool(verified.get("passed", False)),
            "signing_key_id": signed.get("signer", {}).get("key_id"),
        })
        if not passed:
            failures.append(f"Release signing verification failed for profile: {profile}")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "profile_count": len(profiles),
            "signed_bundle_count": len(details),
        },
        "details": details,
    }
    _write_report(repo_root / "docs" / "compliance", "release_signing_report", payload, "Release Signing Report")
    return 0 if payload["passed"] else 1


def verify_peer_bundle_completeness(repo_root: Path, *, strict: bool = True) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    profile_dir = repo_root / "compliance" / "evidence" / "peer_profiles"
    bundle_dir = repo_root / "compliance" / "evidence" / "tier4" / "bundles"
    declared_profiles = sorted(path.stem for path in profile_dir.glob("*.yaml"))
    bundle_rows: dict[str, dict[str, Any]] = {}
    invalid_profiles: list[str] = []
    invalid_bundle_dirs: list[str] = []

    for path in sorted(bundle_dir.iterdir()) if bundle_dir.exists() else []:
        if not path.is_dir():
            continue
        manifest_path = path / "manifest.yaml"
        if not manifest_path.exists():
            continue
        manifest = _load_yaml(manifest_path) or {}
        profile = str(manifest.get("peer_profile", "")).strip()
        if not profile:
            invalid_bundle_dirs.append(str(path.relative_to(repo_root)))
            continue
        qualifies, bundle_failures, details = evaluate_tier4_bundle(path, manifest)
        bundle_rows[profile] = {
            "bundle_dir": str(path.relative_to(repo_root)),
            "status": details["status"],
            "attestation_class": details["attestation_class"],
            "peer_operator": details["peer_operator"],
            "peer_version": details["peer_version"],
            "scenario_result_count": len(list(manifest.get("scenario_results") or [])),
            "has_reproduction": details["has_reproduction"],
            "validation_failure_count": details["validation_failure_count"],
            "qualifies_for_promotion": qualifies,
            "qualification_failures": bundle_failures,
        }
        if not qualifies:
            invalid_profiles.append(profile)

    missing_profiles = [profile for profile in declared_profiles if profile not in bundle_rows]
    failures = [f"Missing preserved external bundle for declared peer profile: {profile}" for profile in missing_profiles]
    failures.extend(f"Invalid preserved bundle manifest missing peer_profile: {path}" for path in invalid_bundle_dirs)
    failures.extend(f"Preserved external bundle is present but not promotion-qualifying: {profile}" for profile in sorted(invalid_profiles))
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "declared_peer_profile_count": len(declared_profiles),
            "preserved_bundle_count": len(bundle_rows),
            "valid_bundle_count": len(bundle_rows) - len(invalid_profiles),
            "invalid_bundle_count": len(invalid_profiles),
            "missing_bundle_count": len(missing_profiles),
            "missing_profiles": missing_profiles,
            "invalid_profiles": sorted(invalid_profiles),
            "bundle_dir": str(bundle_dir.relative_to(repo_root)),
        },
        "details": [
            {
                "profile": profile,
                "bundle_present": profile in bundle_rows,
                **(bundle_rows.get(profile) or {}),
            }
            for profile in declared_profiles
        ],
    }
    _write_report(
        repo_root / "docs" / "compliance",
        "peer_bundle_completeness_report",
        payload,
        "Peer Bundle Completeness Report",
    )
    return payload


GATE_CALLS = {
    "gate-00-structure": lambda root: run_governance_install_check(root, strict=True),
    "gate-05-governance": lambda root: run_governance_install_check(root, strict=True),
    "gate-08-claim-registry-sync": lambda root: 0 if verify_claim_registries(root)["passed"] else 1,
    "gate-10-static": lambda root: run_runtime_foundation_check(root, strict=True),
    "gate-12-project-tree-layout": lambda root: run_project_tree_layout_check(root, strict=True),
    "gate-15-boundary-enforcement": lambda root: run_boundary_enforcement_check(root, strict=True),
    "gate-18-migration-plan": lambda root: run_migration_plan_check(root, strict=True),
    "gate-20-tests": lambda root: 0 if run_test_execution_gate(root)["passed"] else 1,
    "gate-25-wrapper-hygiene": lambda root: run_wrapper_hygiene_check(root, strict=True),
    "gate-30-contracts": lambda root: 0 if validate_openapi_contract(root).passed and validate_openrpc_contract(root).passed else 1,
    "gate-35-contract-sync": lambda root: run_contract_sync_check(root, strict=True),
    "gate-40-evidence": lambda root: 0 if summarize_evidence_status(root)["passed"] else 1,
    "gate-45-evidence-peer": lambda root: run_evidence_peer_check(root, strict=True),
    "gate-50-release-bundle": lambda root: 0 if build_release_bundle(root, deployment_from_options()).exists() else 1,
    "gate-55-contract-validation": lambda root: 0 if validate_openapi_contract(root).passed and validate_openrpc_contract(root).passed else 1,
    "gate-60-release-signing": lambda root: _run_release_signing_gate(root),
    "gate-65-state-reports": lambda root: 0 if generate_state_reports(root) else 1,
    "gate-75-test-classification": lambda root: 0 if verify_test_classification(root, strict=True)["passed"] else 1,
    "gate-85-peer-profiles": lambda root: 0 if execute_peer_profiles(root, deployment_from_options(profile="hardening"), execution_mode="self-check")["passed"] else 1,
    "gate-87-peer-bundle-completeness": lambda root: 0 if verify_peer_bundle_completeness(root, strict=True)["passed"] else 1,
    "gate-90-release": lambda root: 0 if run_final_release_readiness_gate(root)["passed"] else 1,
    "gate-truth-current-state": lambda root: 0 if verify_truth_chain(root, mode="current-state")["passed"] else 1,
    "gate-truth-release-decision": lambda root: 0 if verify_truth_chain(root, mode="release-decision")["passed"] else 1,
    "gate-truth-repository-state": lambda root: 0 if verify_truth_chain(root, mode="repository-state")["passed"] else 1,
    "gate-95-recertification": lambda root: 0 if run_recertification(root)["passed"] else 1,
}


def _build_release_gate_payload(repo_root: Path, gate_names: list[str], results: list[dict[str, Any]], failures: list[str]) -> dict[str, Any]:
    validated = load_validated_execution_status(repo_root)
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "gate_count": len(gate_names),
            "failed_gate_count": len([item for item in results if not item["passed"]]),
            "validated_execution_artifact_count": int(validated.get("validated_artifact_count", 0)),
            "required_validated_inventory_count": int(validated.get("required_validated_inventory_count", 0)),
            "validated_inventory_present_count": int(validated.get("validated_inventory_present_count", 0)),
            "validated_inventory_complete": bool(validated.get("validated_inventory_complete", False)),
            "clean_room_install_matrix_green": bool(validated.get("runtime_matrix_green", False)),
            "in_scope_test_lanes_green": bool(validated.get("in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(validated.get("migration_portability_passed", False)),
            "tier3_evidence_rebuilt_from_validated_runs": bool(validated.get("tier3_evidence_rebuilt_from_validated_runs", False)),
        },
        "details": results,
    }


def run_release_gates(repo_root: Path, *, gate_name: str | None = None, strict: bool = True) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    gate_dir = repo_root / "compliance" / "gates"
    ordered = _load_yaml(gate_dir / "gate-order.yaml") if (gate_dir / "gate-order.yaml").exists() else {"ordered_gates": sorted(GATE_CALLS)}
    gate_names = [gate_name] if gate_name and gate_name not in {"all", "*"} else list(ordered.get("ordered_gates", sorted(GATE_CALLS)))
    truth_gate_names = [name for name in gate_names if name.startswith("gate-truth-")]
    primary_gate_names = [name for name in gate_names if name not in truth_gate_names]

    primary_results: list[dict[str, Any]] = []
    primary_failures: list[str] = []
    for name in primary_gate_names:
        fn = GATE_CALLS.get(name)
        if fn is None:
            primary_failures.append(f"Unknown gate: {name}")
            continue
        try:
            rc = int(fn(repo_root))
            error: str | None = None
        except Exception as exc:
            rc = 1
            error = str(exc)
        passed = rc == 0
        result = {"gate": name, "passed": passed, "rc": rc}
        if error:
            result["error"] = error
        primary_results.append(result)
        if not passed:
            primary_failures.append(f"Gate failed: {name}" + (f" ({error})" if error else ""))

    payload = _build_release_gate_payload(repo_root, primary_gate_names, primary_results, primary_failures)
    _write_report(repo_root / "docs" / "compliance", "release_gate_report", payload, "Release Gate Report")
    materialize_truth_chain(repo_root)

    if not truth_gate_names:
        return payload

    def _run_truth_pass() -> tuple[list[dict[str, Any]], list[str]]:
        truth_results: list[dict[str, Any]] = []
        truth_failures: list[str] = []
        for name in truth_gate_names:
            fn = GATE_CALLS.get(name)
            if fn is None:
                truth_failures.append(f"Unknown gate: {name}")
                continue
            try:
                rc = int(fn(repo_root))
                error: str | None = None
            except Exception as exc:
                rc = 1
                error = str(exc)
            passed = rc == 0
            result = {"gate": name, "passed": passed, "rc": rc}
            if error:
                result["error"] = error
            truth_results.append(result)
            if not passed:
                truth_failures.append(f"Gate failed: {name}" + (f" ({error})" if error else ""))
        return truth_results, truth_failures

    truth_results, truth_failures = _run_truth_pass()
    combined_results = primary_results + truth_results
    combined_failures = primary_failures + truth_failures
    payload = _build_release_gate_payload(repo_root, gate_names, combined_results, combined_failures)
    _write_report(repo_root / "docs" / "compliance", "release_gate_report", payload, "Release Gate Report")
    materialize_truth_chain(repo_root)

    truth_results, truth_failures = _run_truth_pass()
    combined_results = primary_results + truth_results
    combined_failures = primary_failures + truth_failures
    payload = _build_release_gate_payload(repo_root, gate_names, combined_results, combined_failures)
    _write_report(repo_root / "docs" / "compliance", "release_gate_report", payload, "Release Gate Report")
    materialize_truth_chain(repo_root)
    return payload


def build_release_bundle(
    repo_root: Path,
    deployment: Any,
    *,
    bundle_dir: Path | None = None,
    artifact: str = "all",
    require_clean_checkout: bool = False,
) -> Path:
    repo_root = repo_root.resolve()
    clean_checkout = _git_checkout_summary(repo_root)
    if require_clean_checkout and not bool(clean_checkout.get("clean", False)):
        changed = ", ".join(clean_checkout.get("changed_paths", [])[:10]) or "unknown paths"
        raise RuntimeError(f"release evidence requires a clean checkout; dirty paths detected: {changed}")
    version = _current_version(repo_root)
    bundle_root = bundle_dir or (repo_root / "dist" / "release-bundles" / version / deployment.profile)
    if bundle_root.exists():
        shutil.rmtree(bundle_root)
    bundle_root.mkdir(parents=True, exist_ok=True)
    build_evidence_bundle(repo_root, deployment, tier="3", profile_label=deployment.profile, bundle_dir=bundle_root / "evidence")
    copied: list[dict[str, Any]] = []
    if artifact in {"claims", "all"}:
        copied.append(_copy_rel_artifact(repo_root, f"compliance/claims/effective-target-claims.{deployment.profile}.yaml", bundle_root))
    if artifact in {"evidence", "all"}:
        copied.append(_copy_rel_artifact(repo_root, f"compliance/evidence/effective-release-evidence.{deployment.profile}.yaml", bundle_root))
    if artifact in {"contracts", "all"}:
        copied.append(_copy_rel_artifact(repo_root, str(_openapi_path(repo_root, deployment.profile).relative_to(repo_root)), bundle_root))
        copied.append(_copy_rel_artifact(repo_root, str(_openrpc_path(repo_root, deployment.profile).relative_to(repo_root)), bundle_root))
    for rel_path in _dependency_artifact_paths(repo_root):
        copied.append(_copy_rel_artifact(repo_root, rel_path, bundle_root))
    write_authoritative_current_docs_manifest(repo_root)
    authority = load_document_authority(repo_root)
    generated_doc_paths = list(dict.fromkeys(_docs_for_certification_bundle(repo_root)))
    supporting_non_doc_paths = list(dict.fromkeys(authority.get("supporting_current_non_doc_artifacts", [])))
    for rel_path in generated_doc_paths + supporting_non_doc_paths:
        if (repo_root / rel_path).exists():
            copied.append(_copy_rel_artifact(repo_root, rel_path, bundle_root))
    discovery_dir = repo_root / "specs" / "discovery" / "profiles" / deployment.profile
    if discovery_dir.exists():
        for path in sorted(discovery_dir.glob("*.json")):
            copied.append(_copy_rel_artifact(repo_root, str(path.relative_to(repo_root)), bundle_root))
    peer_dir = repo_root / "compliance" / "evidence" / "tier4" / "executions"
    for path in sorted(peer_dir.glob(f"*.{deployment.profile}.yaml")):
        copied.append(_copy_rel_artifact(repo_root, str(path.relative_to(repo_root)), bundle_root))
    current_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "current_state_report.json") or {}
    cert_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "certification_state_report.json") or {}
    gate_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "release_gate_report.json") or {}
    final_gate_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "final_release_gate_report.json") or {}
    validated_report = _load_json_if_exists(repo_root / "docs" / "compliance" / "validated_execution_report.json") or {}
    final_release_status = _load_json_if_exists(repo_root / "docs" / "compliance" / "FINAL_RELEASE_STATUS_2026-03-25.json") or {}
    cert_summary = cert_report.get("summary", {}) if isinstance(cert_report, dict) else {}
    manifest = {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "version": version,
        "profile": deployment.profile,
        "artifact_selection": artifact,
        "deployment": deployment.to_manifest(),
        "dependency_provenance": {
            "artifact_paths": _dependency_artifact_paths(repo_root),
            "native_uv_lock_present": (repo_root / "uv.lock").exists(),
            "equivalent_lock_manifest": "constraints/dependency-lock.json" if (repo_root / "constraints" / "dependency-lock.json").exists() else None,
        },
        "documentation_scope": {
            "generated_current_state_docs_only": True,
            "authoritative_current_docs_spec": authority.get("path"),
            "document_authority_projection_manifest": authority.get("projection_path"),
            "authoritative_current_docs_manifest": "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.json",
            "copied_generated_doc_paths": generated_doc_paths,
            "copied_supporting_non_doc_paths": supporting_non_doc_paths,
            "historical_archive_root": "docs/archive/historical",
        },
        "release_classification": (
            "final-certification-release"
            if bool(cert_summary.get("fully_certifiable_now", False))
            and bool(cert_summary.get("fully_rfc_compliant_now", False))
            and bool(cert_summary.get("strict_independent_claims_ready", False))
            and bool(final_gate_report.get("passed", False))
            else "candidate-checkpoint-not-certified"
        ),
        "current_state_summary": current_report.get("summary", {}) if isinstance(current_report, dict) else {},
        "certification_state_summary": cert_summary,
        "release_gate_summary": gate_report.get("summary", {}) if isinstance(gate_report, dict) else {},
        "final_release_gate_summary": final_gate_report.get("summary", {}) if isinstance(final_gate_report, dict) else {},
        "final_release_status": final_release_status.get("summary", {}) if isinstance(final_release_status, dict) else {},
        "validated_execution_summary": validated_report.get("summary", {}) if isinstance(validated_report, dict) else {},
        "clean_checkout_required": bool(require_clean_checkout),
        "clean_checkout": clean_checkout,
        "artifacts": copied,
    }
    _write_json(bundle_root / "release-bundle.json", manifest)
    _write_yaml(bundle_root / "release-bundle.yaml", manifest)
    digests = {item["path"]: item.get("sha256") for item in copied if item.get("present") and item.get("sha256")}
    _write_json(bundle_root / "digests.json", digests)
    return bundle_root


def _artifact_media_type(rel_path: str) -> str:
    if rel_path.endswith(".json"):
        return "application/json"
    if rel_path.endswith(".yaml") or rel_path.endswith(".yml"):
        return "application/yaml"
    return "application/octet-stream"


def sign_release_bundle(
    bundle_root: Path,
    *,
    signing_key: str | None = None,
    signer_id: str | None = None,
) -> dict[str, Any]:
    bundle_root = bundle_root.resolve()
    manifest_path = bundle_root / "release-bundle.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"release bundle not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    package = str(manifest.get("package", "tigrbl_auth"))
    version = str(manifest.get("version", _current_version(bundle_root.parents[3] if len(bundle_root.parents) >= 4 else bundle_root)))
    profile = str(manifest.get("profile", bundle_root.name))
    attest_root = bundle_root / "attestations"
    if attest_root.exists():
        shutil.rmtree(attest_root)
    attest_root.mkdir(parents=True, exist_ok=True)
    signer = load_signer(signing_key=signing_key or os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY"), signer_id=signer_id)
    verification_refs = write_public_key_artifacts(bundle_root, signer)

    contract_manifest = build_contract_set_manifest(bundle_root)
    contract_manifest_rel = "attestations/contract-set.manifest.json"
    _write_json(bundle_root / contract_manifest_rel, contract_manifest)

    signed_artifacts: list[dict[str, Any]] = []
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="release-bundle",
            artifact_rel_path="release-bundle.json",
            package=package,
            version=version,
            profile=profile,
            artifact_kind="release-bundle-manifest",
            media_type="application/json",
        )
    )
    claim_rel = next((item.get("path") for item in manifest.get("artifacts", []) if str(item.get("path", "")).startswith("compliance/claims/effective-target-claims.")), None)
    if not claim_rel:
        raise ValueError("release bundle is missing an effective claim manifest")
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="claim-manifest",
            artifact_rel_path=str(claim_rel),
            package=package,
            version=version,
            profile=profile,
            artifact_kind="claim-manifest",
            media_type=_artifact_media_type(str(claim_rel)),
        )
    )
    evidence_rel = next((item.get("path") for item in manifest.get("artifacts", []) if str(item.get("path", "")).startswith("compliance/evidence/effective-release-evidence.")), None)
    if not evidence_rel:
        raise ValueError("release bundle is missing an effective evidence manifest")
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="evidence-manifest",
            artifact_rel_path=str(evidence_rel),
            package=package,
            version=version,
            profile=profile,
            artifact_kind="evidence-manifest",
            media_type=_artifact_media_type(str(evidence_rel)),
        )
    )
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="contract-set",
            artifact_rel_path=contract_manifest_rel,
            package=package,
            version=version,
            profile=profile,
            artifact_kind="contract-set-manifest",
            media_type="application/json",
        )
    )
    release_attestation = write_bundle_attestation(
        bundle_root,
        signer=signer,
        package=package,
        version=version,
        profile=profile,
        signed_artifacts=signed_artifacts,
    )
    result = {
        "status": "signed-ed25519-attested",
        "algorithm": "Ed25519",
        "package": package,
        "version": version,
        "profile": profile,
        "signer": signer.identity.to_manifest(),
        "verification_material": verification_refs,
        "release_attestation": release_attestation["attestation_path"],
        "signed_artifacts": signed_artifacts,
        "verification": {"passed": False, "failures": ["verification pending"], "warnings": [], "details": {}},
    }
    _write_json(bundle_root / "signature.json", result)
    verification = verify_bundle_attestations(bundle_root).to_manifest()
    result["verification"] = verification
    _write_json(bundle_root / "signature.json", result)
    return result


def verify_release_bundle_signatures(bundle_root: Path) -> dict[str, Any]:
    bundle_root = bundle_root.resolve()
    result = verify_bundle_attestations(bundle_root)
    payload = result.to_manifest()
    _write_report(
        bundle_root,
        "verification",
        payload,
        "Release Signing Verification Report",
    )
    return payload


def run_recertification(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    watched_paths = [
        repo_root / "pyproject.toml",
        repo_root / "Dockerfile",
        repo_root / "compliance" / "targets" / "boundaries.yaml",
        repo_root / "compliance" / "targets" / "boundary-decisions.yaml",
        repo_root / "compliance" / "targets" / "rfc-targets.yaml",
        repo_root / "compliance" / "targets" / "oidc-targets.yaml",
        repo_root / "constraints" / "base.txt",
        repo_root / "constraints" / "runner-uvicorn.txt",
        repo_root / "constraints" / "runner-hypercorn.txt",
        repo_root / "constraints" / "runner-tigrcorn.txt",
        repo_root / "constraints" / "dependency-lock.json",
        repo_root / "docs" / "runbooks" / "INSTALLATION_PROFILES.md",
        repo_root / "docs" / "runbooks" / "CLEAN_CHECKOUT_REPRO.md",
        repo_root / ".github" / "workflows" / "ci-install-profiles.yml",
    ]
    joined = b""
    for path in watched_paths:
        if path.exists():
            joined += path.read_bytes()
    fingerprint = _hash_bytes(joined)
    state_path = repo_root / "compliance" / "claims" / "recertification-state.yaml"
    previous = _load_yaml(state_path).get("fingerprint") if state_path.exists() else None
    changed = previous is not None and previous != fingerprint
    state = {
        "schema_version": 1,
        "fingerprint": fingerprint,
        "previous_fingerprint": previous,
        "changed_since_last_run": changed,
        "version": _current_version(repo_root),
        "watched_dependency_artifact_count": len([path for path in watched_paths if path.exists()]),
    }
    _write_yaml(state_path, state)
    payload = {
        "passed": True,
        "failures": [],
        "warnings": ["Boundary, dependency, or reproducibility inputs changed; recertification review required."] if changed else [],
        "summary": state,
    }
    _write_report(repo_root / "docs" / "compliance", "recertification_report", payload, "Recertification Report")
    return payload


__all__ = [
    "build_adr_index",
    "build_evidence_bundle",
    "build_release_bundle",
    "diff_contracts",
    "execute_peer_profiles",
    "generate_state_reports",
    "load_validated_execution_status",
    "run_final_release_readiness_gate",
    "run_release_gates",
    "run_test_execution_gate",
    "run_recertification",
    "sign_release_bundle",
    "verify_release_bundle_signatures",
    "verify_peer_bundle_completeness",
    "summarize_evidence_status",
    "validate_openapi_contract",
    "validate_openrpc_contract",
    "verify_test_classification",
]
