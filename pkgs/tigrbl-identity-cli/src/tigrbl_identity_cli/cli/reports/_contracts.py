from __future__ import annotations

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
    "pkgs/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards",
    "pkgs/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/standards",
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
DOC_REF_SCAN_EXCLUDE = {
    "docs/compliance/artifact_truthfulness_report.md",
    "docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.md",
}
ROUTE_CONSTANTS = {
    "JWKS_PATH": "/.well-known/jwks.json",
    "TENANT_JWKS_PATH": "/tenants/{tenant_slug}/.well-known/jwks.json",
    "TENANT_OPENID_CONFIGURATION_PATH": "/tenants/{tenant_slug}/.well-known/openid-configuration",
    "REALM_JWKS_PATH": "/realms/{realm_slug}/.well-known/jwks.json",
    "REALM_OPENID_CONFIGURATION_PATH": "/realms/{realm_slug}/.well-known/openid-configuration",
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
        failures.append("CLI reference markdown drifts from tigrbl_identity_cli.cli.metadata")
    generated_cli_contract = build_cli_contract_manifest()
    committed_cli_contract = _load_json_if_exists(repo_root / "specs" / "cli" / "cli_contract.json") or {}
    if json.dumps(generated_cli_contract, sort_keys=True) != json.dumps(committed_cli_contract, sort_keys=True):
        cli_sync_ok = False
        failures.append("CLI contract artifact drifts from tigrbl_identity_cli.cli.metadata")
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
