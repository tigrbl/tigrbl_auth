from __future__ import annotations

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
    enforce_capability_strictness: bool = True,
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

    if enforce_capability_strictness:
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
        "capability_strict": enforce_capability_strictness,
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
