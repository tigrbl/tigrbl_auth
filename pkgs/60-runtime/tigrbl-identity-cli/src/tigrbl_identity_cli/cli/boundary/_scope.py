from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import yaml

from tigrbl_identity_operator.repo_truth import evaluate_tier4_bundle

from tigrbl_identity_cli.cli.artifacts import (
    build_effective_claims_manifest,
    build_effective_evidence_manifest,
    build_openapi_contract,
    build_openrpc_contract,
    deployment_from_options,
)

REQUIRED_BOUNDARY_ARTIFACTS = [
    "compliance/targets/partial-feature-consumption.yaml",
    "compliance/targets/boundary-decisions.yaml",
    "compliance/targets/boundary-enforcement.yaml",
    "compliance/targets/boundaries.yaml",
    "compliance/targets/boundary-certification-plan.yaml",
    "compliance/targets/out-of-scope-baseline.yaml",
    "compliance/mappings/slice-to-target.yaml",
    "compliance/mappings/profile-to-surface-set.yaml",
    "compliance/mappings/extension-to-boundary.yaml",
    "compliance/mappings/module-to-boundary.yaml",
    "compliance/mappings/decision-to-check.yaml",
    "compliance/mappings/decision-to-gate.yaml",
    "docs/adr/ADR-0018-strict-partial-feature-disappearance.md",
    "docs/adr/ADR-0019-boundary-enforcement-as-code.md",
    "docs/adr/ADR-0020-plugin-and-gateway-composition-profiles.md",
]

PROFILE_NAMES = ("baseline", "production", "hardening")


REQUIRED_SCOPE_FREEZE_PROHIBITED_EXPANSIONS = (
    "RFC 7800",
    "RFC 8417",
    "RFC 8291",
    "RFC 8812",
    "RFC 8932",
    "OAuth 2.1 alignment profile",
    "SAML IdP/SP",
    "LDAP/AD federation",
    "SCIM",
    "policy-platform/federation breadth outside the declared boundary",
)


def _stable_label_hash(labels: Iterable[str]) -> str:
    normalized = sorted(dict.fromkeys(str(label) for label in labels))
    encoded = json.dumps(normalized, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_scope_freeze_metadata(scope: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    freeze = scope.get("boundary_freeze", {}) if isinstance(scope, dict) else {}
    target_entries = [
        entry for entry in (scope.get("targets", []) if isinstance(scope, dict) else [])
        if str(entry.get("scope_bucket", "")) != "out-of-scope/deferred"
    ]
    bucket_names = (
        "baseline-certifiable-now",
        "production-completion-required",
        "hardening-completion-required",
        "runtime-completion-required",
        "operator-completion-required",
    )
    retained_labels = [str(entry.get("label")) for entry in target_entries]
    rfc_labels = [str(entry.get("label")) for entry in target_entries if str(entry.get("family")) == "rfc"]
    non_rfc_labels = [str(entry.get("label")) for entry in target_entries if str(entry.get("family")) != "rfc"]
    deferred_labels = [str(item.get("label")) for item in (scope.get("deferred_targets", []) if isinstance(scope, dict) else [])]
    bucket_counts = {name: sum(1 for entry in target_entries if str(entry.get("scope_bucket")) == name) for name in bucket_names}
    retained_hash = _stable_label_hash(retained_labels)
    rfc_hash = _stable_label_hash(rfc_labels)
    non_rfc_hash = _stable_label_hash(non_rfc_labels)
    deferred_hash = _stable_label_hash(deferred_labels)
    summary = {
        "scope_freeze_present": bool(freeze),
        "scope_freeze_decision_id": str(freeze.get("decision_id", "")) if freeze else "",
        "scope_freeze_effective_date": str(freeze.get("effective_date", "")) if freeze else "",
        "scope_freeze_retained_target_count": len(retained_labels),
        "scope_freeze_retained_rfc_target_count": len(rfc_labels),
        "scope_freeze_retained_non_rfc_target_count": len(non_rfc_labels),
        "scope_freeze_deferred_target_count": len(deferred_labels),
        "scope_freeze_retained_target_identity_hash": retained_hash,
        "scope_freeze_retained_target_identity_hash_matches": bool(freeze) and str(freeze.get("retained_target_identity_hash", "")) == retained_hash,
        "scope_freeze_bucket_count_match": bool(freeze) and dict(freeze.get("retained_bucket_counts", {})) == bucket_counts,
    }
    if not freeze:
        failures.append("Certification scope is missing boundary_freeze metadata")
        return failures, summary
    if str(freeze.get("source_of_truth")) != "compliance/targets/certification_scope.yaml":
        failures.append("Certification scope boundary_freeze source_of_truth must reference compliance/targets/certification_scope.yaml")
    if str(freeze.get("decision_id")) != "BND-012":
        failures.append("Certification scope boundary_freeze decision_id must be BND-012")
    if int(freeze.get("retained_target_count", -1)) != len(retained_labels):
        failures.append("Certification scope boundary_freeze retained_target_count drift detected")
    if int(freeze.get("retained_rfc_target_count", -1)) != len(rfc_labels):
        failures.append("Certification scope boundary_freeze retained_rfc_target_count drift detected")
    if int(freeze.get("retained_non_rfc_target_count", -1)) != len(non_rfc_labels):
        failures.append("Certification scope boundary_freeze retained_non_rfc_target_count drift detected")
    if int(freeze.get("deferred_target_count", -1)) != len(deferred_labels):
        failures.append("Certification scope boundary_freeze deferred_target_count drift detected")
    if dict(freeze.get("retained_bucket_counts", {})) != bucket_counts:
        failures.append("Certification scope boundary_freeze retained_bucket_counts drift detected")
    if str(freeze.get("retained_target_identity_hash", "")) != retained_hash:
        failures.append("Certification scope boundary_freeze retained_target_identity_hash drift detected")
    if str(freeze.get("retained_rfc_target_identity_hash", "")) != rfc_hash:
        failures.append("Certification scope boundary_freeze retained_rfc_target_identity_hash drift detected")
    if str(freeze.get("retained_non_rfc_target_identity_hash", "")) != non_rfc_hash:
        failures.append("Certification scope boundary_freeze retained_non_rfc_target_identity_hash drift detected")
    if str(freeze.get("deferred_target_identity_hash", "")) != deferred_hash:
        failures.append("Certification scope boundary_freeze deferred_target_identity_hash drift detected")
    if not bool(freeze.get("no_target_count_drift_during_closeout", False)):
        failures.append("Certification scope boundary_freeze must set no_target_count_drift_during_closeout=true")
    if not bool(freeze.get("closeout_scope_expansion_requires_separate_program", False)):
        failures.append("Certification scope boundary_freeze must require a separate program for scope expansion")
    if not bool(freeze.get("fully_featured_claim_boundary_fixed", False)):
        failures.append("Certification scope boundary_freeze must lock the fully featured claim boundary during closeout")
    prohibited = {str(item) for item in freeze.get("prohibited_expansions", [])}
    missing = sorted(set(REQUIRED_SCOPE_FREEZE_PROHIBITED_EXPANSIONS) - prohibited)
    if missing:
        failures.append("Certification scope boundary_freeze prohibited_expansions missing: " + ", ".join(missing))
    return failures, summary


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _write_report(report_dir: Path, stem: str, payload: dict[str, Any], title: str) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / f"{stem}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [f"# {title}", "", f"- Passed: `{payload.get('passed', False)}`", ""]
    if payload.get("failures"):
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in payload["failures"]])
        lines.append("")
    if payload.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend([f"- {item}" for item in payload["warnings"]])
        lines.append("")
    if payload.get("summary"):
        lines.extend(["## Summary", ""])
        for key, value in payload["summary"].items():
            lines.append(f"- {key}: `{value}`")
        lines.append("")
    (report_dir / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")


def _resolve_boundary(rel_path: str, mapping: dict[str, str]) -> str | None:
    normalized = rel_path.replace('\\', '/')
    best_key: str | None = None
    for key in mapping:
        key_norm = key.replace('\\', '/')
        if normalized == key_norm or normalized.startswith(key_norm.rstrip('/') + '/'):
            if best_key is None or len(key_norm) > len(best_key):
                best_key = key_norm
    return mapping.get(best_key) if best_key else None


def _iter_python_files(base: Path) -> Iterable[Path]:
    if not base.exists():
        return []
    if base.is_file() and base.suffix == ".py":
        return [base]
    return sorted(base.rglob("*.py"))


def _scan_imports(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def _iter_import_refs(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    refs: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            refs.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * getattr(node, "level", 0)
            if node.module:
                refs.append(prefix + node.module)
            else:
                refs.extend(prefix + alias.name for alias in node.names)
    return refs


def _is_dunder_all_assign(node: ast.stmt) -> bool:
    if isinstance(node, ast.Assign):
        return any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
    if isinstance(node, ast.AnnAssign):
        return isinstance(node.target, ast.Name) and node.target.id == "__all__"
    return False


def _is_wrapper_module(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    body = list(tree.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    if not body:
        return False
    if len(body) == 1 and isinstance(body[0], ast.ImportFrom):
        return any(alias.name == "*" for alias in body[0].names)
    star_imports = [stmt for stmt in body if isinstance(stmt, ast.ImportFrom) and any(alias.name == "*" for alias in stmt.names)]
    if not star_imports:
        return False
    if all(isinstance(stmt, ast.ImportFrom) or _is_dunder_all_assign(stmt) for stmt in body):
        return True
    return False


def _load_in_scope_owner_modules(repo_root: Path) -> list[str]:
    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    owner_modules: set[str] = set()
    for item in scope.get("targets", []):
        bucket = str(item.get("scope_bucket", ""))
        if bucket == "out-of-scope/deferred":
            continue
        for module_rel in item.get("owner_modules", []):
            owner_modules.add(str(module_rel).replace('\\', '/'))
    return sorted(owner_modules)


LEGACY_TREE_IMPORT_PREFIXES = (
    "tigrbl_auth.rfc",
    ".rfc.",
    "..rfc.",
    "...rfc.",
)

ENTRYPOINT_LEGACY_IMPORT_PREFIXES = LEGACY_TREE_IMPORT_PREFIXES + (
    "tigrbl_auth.backends",
    ".backends",
    "..backends",
    "...backends",
    "tigrbl_auth.db",
    ".db",
    "..db",
    "...db",
    "tigrbl_identity_runtime.settings",
    ".runtime_cfg",
    "..runtime_cfg",
    "...runtime_cfg",
    "tigrbl_auth.orm",
    ".orm",
    "..orm",
    "...orm",
)



def _current_version(repo_root: Path) -> str:
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.exists():
        return "0.0.0"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"

def _load_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compare_json_like(left: Any, right: Any) -> bool:
    return json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)


def _effective_for_profile(repo_root: Path, profile: str) -> dict[str, Any]:
    deployment = deployment_from_options(profile=profile)
    version = _current_version(repo_root)
    return {
        "deployment": deployment,
        "openapi": build_openapi_contract(deployment, version=version),
        "openrpc": build_openrpc_contract(deployment, version=version),
        "claims": build_effective_claims_manifest(repo_root, deployment, profile_label=profile),
        "evidence": build_effective_evidence_manifest(repo_root, deployment, profile_label=profile),
    }
