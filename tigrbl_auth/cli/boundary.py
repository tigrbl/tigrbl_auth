from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import yaml

from tigrbl_auth.repo_truth import evaluate_tier4_bundle

from tigrbl_auth.cli.artifacts import (
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
    "RFC 7952",
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
    "tigrbl_auth.runtime_cfg",
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


def run_boundary_enforcement_check(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    failures: list[str] = []
    warnings: list[str] = []
    scope_path = repo_root / "compliance" / "targets" / "certification_scope.yaml"
    scope = _load_yaml(scope_path) if scope_path.exists() else {}
    scope_freeze_failures, scope_freeze_summary = validate_scope_freeze_metadata(scope)
    failures.extend(scope_freeze_failures)

    for rel in REQUIRED_BOUNDARY_ARTIFACTS:
        if not (repo_root / rel).exists():
            failures.append(f"Missing required boundary artifact: {rel}")

    boundary_decisions = _load_yaml(repo_root / "compliance" / "targets" / "boundary-decisions.yaml")
    boundary_enforcement = _load_yaml(repo_root / "compliance" / "targets" / "boundary-enforcement.yaml")
    module_to_boundary = _load_yaml(repo_root / "compliance" / "mappings" / "module-to-boundary.yaml")
    target_to_module = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-module.yaml")
    target_to_gate = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-gate.yaml")
    target_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml")
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    decision_to_check = _load_yaml(repo_root / "compliance" / "mappings" / "decision-to-check.yaml")
    decision_to_gate = _load_yaml(repo_root / "compliance" / "mappings" / "decision-to-gate.yaml")
    partial = _load_yaml(repo_root / "compliance" / "targets" / "partial-feature-consumption.yaml")
    boundary_cfg = boundary_enforcement.get("enforcement", {})
    known_checks = set(boundary_cfg.get("checks", []))
    forbidden_import_roots = tuple(boundary_cfg.get("forbidden_import_roots", []))
    supported_paths = [repo_root / rel for rel in boundary_cfg.get("supported_package_paths", [])]

    # decisions must point to ADRs and mapped checks/gates
    gate_files = {p.stem for p in (repo_root / "compliance" / "gates").glob("gate-*.yaml")}
    for decision in boundary_decisions.get("decisions", []):
        did = str(decision.get("id"))
        adr_path = repo_root / str(decision.get("adr"))
        if not adr_path.exists():
            failures.append(f"Boundary decision {did} points to missing ADR: {decision.get('adr')}")
        checks = set(decision.get("enforced_by_checks", []))
        mapped_checks = set(decision_to_check.get(did, []))
        if checks != mapped_checks:
            failures.append(f"Boundary decision {did} check mapping mismatch")
        unknown_checks = checks - known_checks - {"certified_core_wrapper_count_zero", "tier3_claims_have_evidence_refs", "tier4_claims_have_peer_refs"}
        if unknown_checks:
            failures.append(f"Boundary decision {did} references unknown checks: {', '.join(sorted(unknown_checks))}")
        gates = set(decision.get("release_gates", []))
        mapped_gates = set(decision_to_gate.get(did, []))
        if gates != mapped_gates:
            failures.append(f"Boundary decision {did} gate mapping mismatch")
        unknown_gates = gates - gate_files
        if unknown_gates:
            failures.append(f"Boundary decision {did} references missing gate files: {', '.join(sorted(unknown_gates))}")

    if not partial.get("strict_disappearance_rule"):
        failures.append("Partial feature consumption manifest does not declare strict_disappearance_rule")

    # claim mapping completeness
    declared_claims = _load_yaml(repo_root / "compliance" / "claims" / "declared-target-claims.yaml")
    claim_targets = [str(item.get("target")) for item in declared_claims.get("claim_set", {}).get("claims", [])]
    for target in claim_targets:
        if target not in target_to_module:
            failures.append(f"Declared claim target missing target-to-module mapping: {target}")
            continue
        if target not in target_to_gate:
            failures.append(f"Declared claim target missing target-to-gate mapping: {target}")
        if target not in target_to_test:
            warnings.append(f"Declared claim target missing target-to-test mapping: {target}")
        if target not in target_to_evidence:
            warnings.append(f"Declared claim target missing target-to-evidence mapping: {target}")
        for module_rel in target_to_module.get(target, {}).get("modules", []):
            module_path = repo_root / str(module_rel)
            if not module_path.exists():
                failures.append(f"Declared claim target {target} maps to missing module: {module_rel}")
                continue
            boundary = _resolve_boundary(str(module_rel), module_to_boundary)
            if boundary != "certified_core":
                failures.append(f"Declared claim target {target} maps to non-certified module {module_rel} ({boundary})")

    # scan supported package paths for forbidden imports and boundary leaks
    certified_files: list[Path] = []
    for base in supported_paths:
        for path in _iter_python_files(base):
            if path.name == "__init__.py":
                continue
            rel = str(path.relative_to(repo_root)).replace('\\', '/')
            if _resolve_boundary(rel, module_to_boundary) == "certified_core":
                certified_files.append(path)

    boundary_leaks: list[str] = []
    import_violations: list[str] = []
    for path in certified_files:
        rel = str(path.relative_to(repo_root)).replace('\\', '/')
        for imported in _scan_imports(path):
            if imported.startswith(forbidden_import_roots):
                import_violations.append(f"{rel} imports forbidden root {imported}")
                continue
            if imported.startswith("tigrbl_auth."):
                imported_rel = imported.replace('.', '/') + ".py"
                imported_boundary = _resolve_boundary(imported_rel, module_to_boundary)
                if imported_boundary in {"legacy_transition", "extension_quarantine", "out_of_scope_baseline"}:
                    boundary_leaks.append(f"{rel} imports {imported_rel} ({imported_boundary})")

    failures.extend(sorted(set(import_violations)))
    failures.extend(sorted(set(boundary_leaks)))

    # strict disappearance and profile sync
    profile_artifacts = boundary_cfg.get("profile_artifacts", {})
    profile_summary: dict[str, dict[str, int]] = {}
    for profile in PROFILE_NAMES:
        generated = _effective_for_profile(repo_root, profile)
        deployment = generated["deployment"]
        expected_paths = {path for path in deployment.active_routes if not path.startswith("/system/")}
        actual_paths = set(generated["openapi"].get("paths", {}).keys())
        if expected_paths != actual_paths:
            failures.append(f"{profile}: generated OpenAPI paths drift from active routes")
        openrpc_methods = [item.get("name") for item in generated["openrpc"].get("methods", [])]
        expected_openrpc_methods = list(deployment.active_openrpc_methods)
        if set(openrpc_methods) != set(expected_openrpc_methods):
            failures.append(f"{profile}: generated OpenRPC methods drift from active methods")
        if len(openrpc_methods) != len(set(openrpc_methods)):
            failures.append(f"{profile}: generated OpenRPC methods contain duplicates")
        effective_claim_targets = {str(item.get("target")) for item in generated["claims"].get("claim_set", {}).get("claims", [])}
        if not effective_claim_targets.issubset(set(deployment.active_targets)):
            failures.append(f"{profile}: effective claim targets escape the active deployment boundary")
        evidence_targets = {str(item.get("target")) for item in generated["evidence"].get("bundle_manifest", {}).get("bundles", [])}
        if evidence_targets != effective_claim_targets:
            failures.append(f"{profile}: effective evidence targets are not synchronized with effective claims")

        committed_cfg = profile_artifacts.get(profile, {})
        openapi_path = repo_root / str(committed_cfg.get("openapi", ""))
        openrpc_path = repo_root / str(committed_cfg.get("openrpc", ""))
        claims_path = repo_root / str(committed_cfg.get("claims", ""))
        evidence_path = repo_root / str(committed_cfg.get("evidence", ""))
        committed_openapi = _load_json_if_exists(openapi_path)
        committed_openrpc = _load_json_if_exists(openrpc_path)
        committed_claims = _load_yaml(claims_path) if claims_path.exists() else None
        committed_evidence = _load_yaml(evidence_path) if evidence_path.exists() else None
        if committed_openapi is None:
            failures.append(f"{profile}: missing committed OpenAPI artifact {openapi_path.relative_to(repo_root)}")
        elif not _compare_json_like(committed_openapi, generated["openapi"]):
            failures.append(f"{profile}: committed OpenAPI artifact is out of sync")
        if committed_openrpc is None:
            failures.append(f"{profile}: missing committed OpenRPC artifact {openrpc_path.relative_to(repo_root)}")
        elif not _compare_json_like(committed_openrpc, generated["openrpc"]):
            failures.append(f"{profile}: committed OpenRPC artifact is out of sync")
        if committed_claims is None:
            failures.append(f"{profile}: missing committed effective claims artifact {claims_path.relative_to(repo_root)}")
        elif yaml.safe_dump(committed_claims, sort_keys=True) != yaml.safe_dump(generated["claims"], sort_keys=True):
            failures.append(f"{profile}: committed effective claims artifact is out of sync")
        if committed_evidence is None:
            failures.append(f"{profile}: missing committed effective evidence artifact {evidence_path.relative_to(repo_root)}")
        elif yaml.safe_dump(committed_evidence, sort_keys=True) != yaml.safe_dump(generated["evidence"], sort_keys=True):
            failures.append(f"{profile}: committed effective evidence artifact is out of sync")

        profile_summary[profile] = {
            "route_count": len(actual_paths),
            "claim_count": len(effective_claim_targets),
            "method_count": len(openrpc_methods),
        }

    report = {
        "scope": "boundary-enforcement",
        "strict": strict,
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "certified_core_file_count": len(certified_files),
            "boundary_leak_count": len(set(boundary_leaks)),
            "forbidden_import_count": len(set(import_violations)),
            **{f"{profile}_route_count": summary["route_count"] for profile, summary in profile_summary.items()},
            **{f"{profile}_claim_count": summary["claim_count"] for profile, summary in profile_summary.items()},
            **scope_freeze_summary,
        },
    }
    _write_report(report_dir, "boundary_enforcement_report", report, "Boundary Enforcement Report")
    return 1 if failures and strict else 0


def run_wrapper_hygiene_check(
    repo_root: Path,
    *,
    strict: bool = True,
    report_dir: Path | None = None,
    enforce_phase1_strictness: bool = True,
) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    mapping = _load_yaml(repo_root / "compliance" / "mappings" / "module-to-boundary.yaml")
    failures: list[str] = []
    warnings: list[str] = []
    certified_hits: list[str] = []
    non_certified_hits: list[str] = []
    for path in sorted((repo_root / "tigrbl_auth").rglob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = str(path.relative_to(repo_root)).replace('\\', '/')
        boundary = _resolve_boundary(rel, mapping)
        if _is_wrapper_module(path):
            if boundary == "certified_core":
                certified_hits.append(rel)
            else:
                non_certified_hits.append(rel)

    in_scope_owner_modules = _load_in_scope_owner_modules(repo_root)
    in_scope_target_wrapper_hits: list[str] = []
    in_scope_target_non_core_hits: list[str] = []
    for rel in in_scope_owner_modules:
        path = repo_root / rel
        boundary = _resolve_boundary(rel, mapping)
        if path.exists() and path.is_file() and _is_wrapper_module(path):
            in_scope_target_wrapper_hits.append(rel)
        if path.exists() and boundary not in {"certified_core", "governance_plane"}:
            in_scope_target_non_core_hits.append(f"{rel} ({boundary})")

    standards_legacy_proxy_hits: list[str] = []
    for path in _iter_python_files(repo_root / "tigrbl_auth" / "standards"):
        if path.name == "__init__.py":
            continue
        rel = str(path.relative_to(repo_root)).replace('\\', '/')
        refs = _iter_import_refs(path)
        bad = sorted({ref for ref in refs if ref.startswith(LEGACY_TREE_IMPORT_PREFIXES)})
        if bad:
            standards_legacy_proxy_hits.append(f"{rel} -> {', '.join(bad)}")

    entrypoint_legacy_hits: list[str] = []
    entrypoint_roots = [
        repo_root / "tigrbl_auth" / "api",
        repo_root / "tigrbl_auth" / "plugin.py",
        repo_root / "tigrbl_auth" / "gateway.py",
        repo_root / "tigrbl_auth" / "app.py",
        repo_root / "tigrbl_auth" / "security",
        repo_root / "tigrbl_auth" / "services",
        repo_root / "tigrbl_auth" / "ops",
        repo_root / "tigrbl_auth" / "standards",
    ]
    for base in entrypoint_roots:
        for path in _iter_python_files(base):
            if path.name == "__init__.py":
                continue
            rel = str(path.relative_to(repo_root)).replace('\\', '/')
            refs = _iter_import_refs(path)
            bad = sorted({ref for ref in refs if ref.startswith(ENTRYPOINT_LEGACY_IMPORT_PREFIXES)})
            if bad:
                entrypoint_legacy_hits.append(f"{rel} -> {', '.join(bad)}")

    if certified_hits:
        failures.append(f"Certified-core wrapper or shim modules remain: {', '.join(sorted(certified_hits))}")
    if non_certified_hits:
        warnings.append(f"Wrapper/shim modules remain outside the certified core: {', '.join(sorted(non_certified_hits))}")

    if enforce_phase1_strictness:
        if in_scope_target_wrapper_hits:
            failures.append(
                "In-scope owner modules still resolve through thin wrapper modules: "
                + ", ".join(sorted(in_scope_target_wrapper_hits))
            )
        if in_scope_target_non_core_hits:
            failures.append(
                "In-scope owner modules are still mapped outside the certified core: "
                + ", ".join(sorted(in_scope_target_non_core_hits))
            )
        if standards_legacy_proxy_hits:
            failures.append(
                "Standards-tree modules still import the legacy flat RFC tree: "
                + "; ".join(sorted(standards_legacy_proxy_hits))
            )
        if entrypoint_legacy_hits:
            failures.append(
                "Package entrypoint and certified release-path roots still import legacy compatibility surfaces: "
                + "; ".join(sorted(entrypoint_legacy_hits))
            )

    report = {
        "scope": "wrapper-hygiene",
        "strict": strict,
        "phase1_strict": enforce_phase1_strictness,
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "certified_core_wrapper_count": len(certified_hits),
            "non_certified_wrapper_count": len(non_certified_hits),
            "in_scope_target_wrapper_count": len(in_scope_target_wrapper_hits),
            "in_scope_target_non_core_count": len(in_scope_target_non_core_hits),
            "standards_legacy_proxy_count": len(standards_legacy_proxy_hits),
            "entrypoint_legacy_import_count": len(entrypoint_legacy_hits),
        },
    }
    _write_report(report_dir, "wrapper_hygiene_report", report, "Wrapper Hygiene Report")
    return 1 if failures and strict else 0



def run_contract_sync_check(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    boundary_enforcement = _load_yaml(repo_root / "compliance" / "targets" / "boundary-enforcement.yaml")
    profile_artifacts = boundary_enforcement.get("enforcement", {}).get("profile_artifacts", {})
    failures: list[str] = []
    warnings: list[str] = []

    # active artifacts
    active_deployment = deployment_from_options()
    version = _current_version(repo_root)
    active_openapi = build_openapi_contract(active_deployment, version=version)
    active_openrpc = build_openrpc_contract(active_deployment, version=version)
    active_openapi_path = repo_root / "specs" / "openapi" / "tigrbl_auth.public.openapi.json"
    active_openrpc_path = repo_root / "specs" / "openrpc" / "tigrbl_auth.admin.openrpc.json"
    committed_openapi = _load_json_if_exists(active_openapi_path)
    committed_openrpc = _load_json_if_exists(active_openrpc_path)
    if committed_openapi is None or not _compare_json_like(committed_openapi, active_openapi):
        failures.append("Active OpenAPI contract is missing or out of sync")
    if committed_openrpc is None or not _compare_json_like(committed_openrpc, active_openrpc):
        failures.append("Active OpenRPC contract is missing or out of sync")

    for profile in PROFILE_NAMES:
        generated = _effective_for_profile(repo_root, profile)
        cfg = profile_artifacts.get(profile, {})
        openapi_path = repo_root / str(cfg.get("openapi", ""))
        openrpc_path = repo_root / str(cfg.get("openrpc", ""))
        committed_openapi = _load_json_if_exists(openapi_path)
        committed_openrpc = _load_json_if_exists(openrpc_path)
        if committed_openapi is None:
            failures.append(f"{profile}: missing committed OpenAPI contract")
        elif not _compare_json_like(committed_openapi, generated["openapi"]):
            failures.append(f"{profile}: committed OpenAPI contract drifts from generated contract")
        if committed_openrpc is None:
            failures.append(f"{profile}: missing committed OpenRPC contract")
        elif not _compare_json_like(committed_openrpc, generated["openrpc"]):
            failures.append(f"{profile}: committed OpenRPC contract drifts from generated contract")
        if not generated["openapi"].get("x-tigrbl-auth"):
            failures.append(f"{profile}: generated OpenAPI contract missing x-tigrbl-auth metadata")
        if not generated["openrpc"].get("x-tigrbl-auth"):
            failures.append(f"{profile}: generated OpenRPC contract missing x-tigrbl-auth metadata")

    report = {
        "scope": "contract-sync",
        "strict": strict,
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "profile_count": len(PROFILE_NAMES),
            "active_openapi_path_count": len(active_openapi.get("paths", {})),
            "active_openrpc_method_count": len(active_openrpc.get("methods", [])),
        },
    }
    _write_report(report_dir, "contract_sync_report", report, "Contract Sync Report")
    return 1 if failures and strict else 0


def _ref_exists(repo_root: Path, ref: str) -> bool:
    path = repo_root / ref
    if path.is_file():
        return True
    if path.is_dir():
        for candidate in ("README.md", "manifest.yaml", "bundle.yaml"):
            if (path / candidate).exists():
                return True
        return any(path.iterdir())
    return False




def _tier4_bundle_valid(repo_root: Path, rel: str) -> tuple[bool, list[str]]:
    bundle_root = repo_root / str(rel)
    if bundle_root.is_file():
        return False, [f"Tier 4 evidence ref must be a directory bundle: {rel}"]
    manifest_path = bundle_root / "manifest.yaml"
    if not manifest_path.exists():
        return False, [f"Tier 4 bundle missing manifest: {rel}/manifest.yaml"]
    manifest = _load_yaml(manifest_path) or {}
    ok, failures, _details = evaluate_tier4_bundle(bundle_root, manifest)
    return ok, [f"Tier 4 bundle {rel}: {failure}" for failure in failures]


def run_evidence_peer_check(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    failures: list[str] = []
    warnings: list[str] = []
    declared_claims = _load_yaml(repo_root / "compliance" / "claims" / "declared-target-claims.yaml")
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    evidence_manifest = _load_yaml(repo_root / "compliance" / "evidence" / "manifest.yaml")

    tier3_or_higher = 0
    tier4 = 0
    for claim in declared_claims.get("claim_set", {}).get("claims", []):
        target = str(claim.get("target"))
        tier = int(claim.get("tier", 0))
        refs = list(target_to_evidence.get(target, []))
        if tier >= 3:
            tier3_or_higher += 1
            if not refs:
                failures.append(f"Tier 3+ claim lacks evidence references: {target}")
            for ref in refs:
                if not _ref_exists(repo_root, str(ref)):
                    failures.append(f"Evidence reference does not exist for {target}: {ref}")
        elif not refs:
            warnings.append(f"Tier 0-2 claim has no evidence placeholder refs yet: {target}")
        if tier >= 4:
            tier4 += 1
            tier4_refs = [str(ref) for ref in refs if "tier4" in str(ref)]
            if not tier4_refs:
                failures.append(f"Tier 4 claim lacks peer evidence references: {target}")
                continue
            valid_refs = False
            for ref in tier4_refs:
                if not _ref_exists(repo_root, ref):
                    failures.append(f"Tier 4 evidence reference does not exist for {target}: {ref}")
                    continue
                ok, bundle_failures = _tier4_bundle_valid(repo_root, ref)
                if ok:
                    valid_refs = True
                else:
                    failures.extend(bundle_failures)
            if not valid_refs:
                failures.append(f"Tier 4 claim has no valid preserved peer bundle: {target}")

    preserved = [str(item) for item in ((evidence_manifest.get("state") or {}).get("preserved_tier4_bundles") or [])]
    for ref in preserved:
        if not _ref_exists(repo_root, ref):
            failures.append(f"Preserved Tier 4 bundle listed in evidence manifest is missing: {ref}")
            continue
        ok, bundle_failures = _tier4_bundle_valid(repo_root, ref)
        if not ok:
            failures.extend(bundle_failures)

    if tier3_or_higher == 0:
        warnings.append("No Tier 3 claims declared yet; evidence gate remains preparatory")
    if tier4 == 0:
        warnings.append("No Tier 4 claims declared yet; peer gate remains preparatory")

    report = {
        "scope": "evidence-peer-readiness",
        "strict": strict,
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "tier3_or_higher_claim_count": tier3_or_higher,
            "tier4_claim_count": tier4,
            "declared_claim_count": len(declared_claims.get("claim_set", {}).get("claims", [])),
            "preserved_tier4_bundle_count": len(preserved),
        },
    }
    _write_report(report_dir, "evidence_peer_readiness_report", report, "Evidence and Peer Readiness Report")
    return 1 if failures and strict else 0
