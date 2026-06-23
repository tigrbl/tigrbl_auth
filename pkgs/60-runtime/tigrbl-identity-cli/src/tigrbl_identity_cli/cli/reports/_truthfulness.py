from __future__ import annotations

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
        summary="The storage-backed administration workflow materializes durable sqlite-backed state outside the repository tree.",
        evidence=[
            "pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/operator_store.py",
            "tests/unit/test_operator_control_plane.py",
        ],
        details_payload=operator_summary,
    )
    capabilities["register_manage_clients"] = _capability(
        "register/manage clients",
        passed=client_passed,
        summary="Client records can be created, updated, listed, fetched, and deleted through storage-backed administration workflows.",
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
        summary="Key lifecycle workflows generate, rotate, retire, and publish JWKS artifacts.",
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
        summary="Portability workflows export a versioned artifact and import it into a new storage-backed identity state root.",
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
