from __future__ import annotations

def handle_evidence_verify(args: Any) -> int:
    return run_evidence_peer_check(_repo_root(args.repo_root), strict=_strict(args), report_dir=_report_dir(args))


def handle_evidence_peer_status(args: Any) -> int:
    payload = summarize_evidence_status(_repo_root(args.repo_root))
    payload["command"] = "evidence.peer_status"
    return _emit(args, payload)


def handle_evidence_peer_execute(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    payload = execute_peer_profiles(repo_root, deployment, profiles=args.peer_profile, execution_mode=args.execution_mode)
    payload["command"] = "evidence.peer_execute"
    return _emit(args, payload)


def handle_adr_list(args: Any) -> int:
    payload = {"command": "adr.list", **build_adr_index(_repo_root(args.repo_root))}
    return _emit(args, payload)


def handle_adr_show(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    if not args.id:
        raise SystemExit("--id is required")
    path = repo_root / "docs" / "adr" / f"{args.id}.md"
    payload = {"command": "adr.show", "path": str(path.relative_to(repo_root)), "exists": path.exists()}
    if path.exists():
        payload["content"] = path.read_text(encoding="utf-8")
    return _emit(args, payload)


def handle_adr_new(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    if not args.id:
        raise SystemExit("--id is required")
    title = args.title or args.id.replace("-", " ").title()
    path = repo_root / "docs" / "adr" / f"{args.id}.md"
    if not path.exists():
        path.write_text(f"# {title}\n\n- Status: proposed\n- Context: \n- Decision: \n- Consequences: \n", encoding="utf-8")
    index = build_adr_index(repo_root)
    return _emit(args, {"command": "adr.new", "path": str(path.relative_to(repo_root)), "created": True, "index_count": index["count"]})


def handle_adr_index(args: Any) -> int:
    payload = {"command": "adr.index", **build_adr_index(_repo_root(args.repo_root))}
    return _emit(args, payload)


def handle_doctor(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = deployment_from_options(profile=getattr(args, "profile", None))
    runtime_profile_report = write_runtime_profile_report(repo_root, deployment=deployment, report_dir=_report_dir(args))
    payload = {
        "command": "doctor",
        "governance_ok": run_governance_install_check(repo_root, strict=False) == 0,
        "claims_ok": run_lint(repo_root, strict=False) == 0,
        "runtime_foundation_ok": run_runtime_foundation_check(repo_root, strict=False) == 0,
        "boundary_ok": run_boundary_enforcement_check(repo_root, strict=False) == 0,
        "contracts_ok": validate_openapi_contract(repo_root).passed and validate_openrpc_contract(repo_root).passed,
        "runner_registry": runner_registry_manifest(),
        "runner_profiles": runtime_profile_report.get("profiles", []),
        "runtime_profile_summary": runtime_profile_report.get("summary", {}),
        "evidence": summarize_evidence_status(repo_root)["summary"],
        "release_gates": run_release_gates(repo_root, strict=False)["summary"],
        "cli_contract": build_cli_contract_manifest().get("summary", {}),
        "cli_conformance": build_cli_conformance_snapshot().get("summary", {}),
    }
    return _emit(args, payload)


def handle_bootstrap_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    payload = {"command": "bootstrap.status", "deployment": deployment.to_manifest()}
    payload.update(_claims_summary(repo_root, deployment))
    return _emit(args, payload)


def handle_bootstrap_manifest(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else (repo_root / "dist" / "bootstrap" / deployment.profile)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = bundle_dir / "deployment.json"
    manifest_path.write_text(json.dumps(deployment.to_manifest(), indent=2) + "\n", encoding="utf-8")
    write_effective_claims_manifest(repo_root, deployment, profile_label=deployment.profile)
    write_effective_evidence_manifest(repo_root, deployment, profile_label=deployment.profile)
    write_openapi_contract(repo_root, deployment, profile_label=deployment.profile)
    write_openrpc_contract(repo_root, deployment, profile_label=deployment.profile)
    payload = {"command": "bootstrap.manifest", "manifest": str(manifest_path.relative_to(repo_root))}
    payload.update(_claims_summary(repo_root, deployment))
    return _emit(args, payload)


def handle_migrate_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    revisions = sorted((repo_root / "tigrbl_auth" / "migrations" / "versions").glob("*.py"))
    if _report_dir(args):
        run_migration_plan_check(repo_root, strict=False, report_dir=_report_dir(args))
    return _emit(args, {"command": "migrate.status", "revision_count": len(revisions), "revisions": [str(path.relative_to(repo_root)) for path in revisions]})


def handle_migrate_plan(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    plan = yaml.safe_load((repo_root / "compliance" / "mappings" / "current-to-target-paths.yaml").read_text(encoding="utf-8"))
    payload = {"command": "migrate.plan"}
    payload.update(plan)
    return _emit(args, payload)


def handle_migrate_verify(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    report_dir = _report_dir(args)
    rc_a = run_project_tree_layout_check(repo_root, strict=_strict(args), report_dir=report_dir)
    rc_b = run_migration_plan_check(repo_root, strict=_strict(args), report_dir=report_dir)
    return 0 if rc_a == 0 and rc_b == 0 else 1


def handle_release_bundle(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle = build_release_bundle(repo_root, deployment, bundle_dir=Path(args.bundle_dir).resolve() if args.bundle_dir else None, artifact=args.artifact)
    return _emit(args, {"command": "release.bundle", "bundle_dir": _display_path(bundle, repo_root)})


def handle_release_sign(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else (repo_root / "dist" / "release-bundles" / _version(repo_root) / deployment.profile)
    if not bundle_dir.exists():
        build_release_bundle(repo_root, deployment, bundle_dir=bundle_dir)
    payload = sign_release_bundle(bundle_dir, signing_key=args.signing_key)
    payload["command"] = "release.sign"
    payload["bundle_dir"] = _display_path(bundle_dir, repo_root)
    return _emit(args, payload)


def _version(repo_root: Path) -> str:
    pyproject = repo_root / "pyproject.toml"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"


def handle_release_verify(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else (repo_root / "dist" / "release-bundles" / _version(repo_root) / deployment.profile)
    if not bundle_dir.exists():
        payload = {
            "command": "release.verify",
            "bundle_dir": _display_path(bundle_dir, repo_root),
            "bundle_present": False,
            "verification": {"passed": False, "failures": [f"release bundle not found: {bundle_dir}"]},
        }
        return _emit_with_code(args, payload, rc=1)
    verification = verify_release_bundle_signatures(bundle_dir)
    payload = {
        "command": "release.verify",
        "bundle_dir": _display_path(bundle_dir, repo_root),
        "bundle_present": True,
        "verification": verification,
    }
    return _emit_with_code(args, payload, rc=0 if verification.get("passed") else 1)


def handle_release_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = repo_root / "dist" / "release-bundles" / _version(repo_root) / deployment.profile
    signing = verify_release_bundle_signatures(bundle_dir) if bundle_dir.exists() and (bundle_dir / "signature.json").exists() else {"passed": False, "details": {}}
    payload = {
        "command": "release.status",
        "bundle_dir": str(bundle_dir.relative_to(repo_root)) if bundle_dir.exists() else None,
        "bundle_present": bundle_dir.exists(),
        "signing": signing,
        "release_gates": run_release_gates(repo_root, strict=False)["summary"],
        "evidence": summarize_evidence_status(repo_root)["summary"],
    }
    return _emit(args, payload)


def handle_release_recertify(args: Any) -> int:
    payload = run_recertification(_repo_root(args.repo_root))
    payload["command"] = "release.recertify"
    return _emit(args, payload)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _operator_state_dir(repo_root: Path) -> Path:
    path = _durable_operator_state_root(repo_root) / "status"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _state_path(repo_root: Path, resource: str) -> Path:
    return _operator_state_dir(repo_root) / f"{resource}.json"


def _load_jsonish(path: Path, default: Any) -> Any:
    if not path.exists():
        return copy.deepcopy(default)
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text) or copy.deepcopy(default)
    return json.loads(text)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_structured_file(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {"value": data}


def _deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _set_nested(target: dict[str, Any], key: str, value: Any) -> None:
    parts = [part for part in key.split(".") if part]
    if not parts:
        return
    cursor = target
    for part in parts[:-1]:
        next_value = cursor.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            cursor[part] = next_value
        cursor = next_value
    cursor[parts[-1]] = value


def _parse_inline_set(values: list[str] | tuple[str, ...]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for item in values:
        if "=" not in item:
            raise SystemExit(f"Invalid --set value; expected key=value, got: {item}")
        key, raw_value = item.split("=", 1)
        _set_nested(payload, key.strip(), yaml.safe_load(raw_value))
    return payload


def _mutation_payload(args: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    source_path = getattr(args, "from_file", None) or getattr(args, "input_path", None)
    if source_path:
        payload = _deep_merge(payload, _load_structured_file(Path(source_path).resolve()))
    inline_values = list(getattr(args, "set_item", []) or [])
    if inline_values:
        payload = _deep_merge(payload, _parse_inline_set(inline_values))
    return payload


def _resource_store(repo_root: Path, resource: str) -> dict[str, dict[str, Any]]:
    return _load_jsonish(_state_path(repo_root, resource), default={})


def _save_resource_store(repo_root: Path, resource: str, store: dict[str, dict[str, Any]]) -> Path:
    path = _state_path(repo_root, resource)
    _write_json(path, store)
    return path


def _record_identifier(args: Any, payload: dict[str, Any], resource: str) -> str:
    identifier = getattr(args, "id", None) or payload.get("id") or payload.get("name") or payload.get("key_id")
    if identifier:
        return str(identifier)
    generated = f"{resource}-{secrets.token_hex(6)}"
    return generated


def _sort_items(items: list[dict[str, Any]], sort_key: str) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: (str(item.get(sort_key) or ""), str(item.get("id") or "")))


def _filtered_items(store: dict[str, dict[str, Any]], *, filter_text: str | None, status_filter: str | None, sort_key: str, offset: int, limit: int) -> tuple[list[dict[str, Any]], int]:
    items = [copy.deepcopy(item) for item in store.values()]
    if filter_text:
        term = filter_text.lower()
        items = [item for item in items if term in str(item.get("id", "")).lower() or term in str(item.get("name", "")).lower()]
    if status_filter:
        items = [item for item in items if str(item.get("status")) == str(status_filter)]
    items = _sort_items(items, sort_key)
    total = len(items)
    sliced = items[offset : offset + limit]
    return sliced, total


def _base_record(resource: str, identifier: str, payload: dict[str, Any]) -> dict[str, Any]:
    record = copy.deepcopy(payload)
    record.setdefault("id", identifier)
    record.setdefault("resource", resource)
    record.setdefault("status", "active")
    record.setdefault("enabled", True)
    record.setdefault("created_at", _utc_now())
    record["updated_at"] = _utc_now()
    return record


def _merge_record(existing: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = _deep_merge(existing, patch)
    merged["updated_at"] = _utc_now()
    return merged


def _mutation_result_payload(command: str, resource: str, record: dict[str, Any], state_path: Path, *, mutation: str, persisted: bool, dry_run: bool, extras: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "command": command,
        "resource": resource,
        "mutation": mutation,
        "persisted": persisted,
        "dry_run": dry_run,
        "record": record,
        "state_path": str(state_path),
    }
    if extras:
        payload.update(extras)
    return payload


def _query_result_payload(command: str, resource: str, *, record: dict[str, Any] | None = None, items: list[dict[str, Any]] | None = None, total: int | None = None, state_path: Path | None = None, offset: int | None = None, limit: int | None = None, extras: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"command": command, "resource": resource}
    if record is not None:
        payload["record"] = record
    if items is not None:
        payload["items"] = items
        payload["total"] = total if total is not None else len(items)
        payload["offset"] = 0 if offset is None else offset
        payload["limit"] = len(items) if limit is None else limit
    if state_path is not None:
        payload["state_path"] = str(state_path)
    if extras:
        payload.update(extras)
    return payload


def _resource_catalog(repo_root: Path, resource: str) -> dict[str, Any]:
    catalog: dict[str, dict[str, Any]] = {
        "tenant": {"modules": ["tigrbl_auth/tables/tenant.py"], "routes": [], "targets": [], "verbs": ["create", "update", "delete", "get", "list", "enable", "disable"]},
        "client": {"modules": ["tigrbl_auth/tables/client.py", "tigrbl_auth/standards/oauth2/rfc7591.py"], "routes": ["/register"], "targets": ["RFC 7591", "RFC 7592"], "verbs": ["create", "update", "delete", "get", "list", "rotate-secret", "enable", "disable"]},
        "identity": {"modules": ["tigrbl_auth/tables/user.py", "tigrbl_auth/tables/service.py", "tigrbl_auth/tables/api_key.py", "tigrbl_auth/tables/service_key.py"], "routes": ["/login"], "targets": ["OIDC Core 1.0"], "verbs": ["create", "update", "delete", "get", "list", "set-password", "lock", "unlock"]},
        "flow": {"modules": ["tigrbl_auth/ops/login.py", "tigrbl_auth/ops/authorize.py", "tigrbl_auth/ops/token.py"], "routes": sorted(ROUTE_REGISTRY), "targets": sorted({target for data in PROTOCOL_SLICE_REGISTRY.values() for target in data.get("targets", ())}), "verbs": ["create", "update", "delete", "get", "list", "enable", "disable"]},
        "session": {"modules": ["tigrbl_auth/tables/auth_session.py"], "routes": ["/login", "/logout"], "targets": ["OIDC Session Management", "OIDC RP-Initiated Logout"], "verbs": ["get", "list", "revoke", "revoke-all"]},
        "token": {"modules": ["tigrbl_auth/services/token_service.py"], "routes": ["/token", "/introspect", "/revoke", "/token/exchange"], "targets": ["RFC 6749", "RFC 6750", "RFC 7009", "RFC 7662", "RFC 8693"], "verbs": ["get", "list", "introspect", "revoke", "exchange"]},
        "keys": {"modules": ["tigrbl_auth/services/key_management.py", "tigrbl_auth/services/jwks_service.py"], "routes": ["/.well-known/jwks.json"], "targets": ["RFC 7517", "RFC 7518", "RFC 7519"], "verbs": ["generate", "import", "export", "rotate", "retire", "publish-jwks", "get", "list", "delete"]},
        "discovery": {"modules": ["tigrbl_auth/standards/oidc/discovery.py", "tigrbl_auth/standards/oauth2/rfc8414.py", "tigrbl_auth/standards/oauth2/rfc9728.py"], "routes": ["/.well-known/openid-configuration", "/.well-known/oauth-authorization-server", "/.well-known/oauth-protected-resource"], "targets": ["OIDC Discovery 1.0", "RFC 8414", "RFC 9728", "RFC 8615"], "verbs": ["show", "validate", "publish", "diff"]},
        "import": {"modules": ["compliance/claims", "compliance/evidence"], "routes": [], "targets": ["OpenAPI 3.1 / 3.2 compatible public contract", "OpenRPC 1.4.x admin/control-plane contract"], "verbs": ["validate", "run", "status"]},
        "export": {"modules": ["dist/release-bundles", "dist/evidence-bundles"], "routes": [], "targets": ["OpenAPI 3.1 / 3.2 compatible public contract", "OpenRPC 1.4.x admin/control-plane contract"], "verbs": ["validate", "run", "status"]},
    }
    payload = catalog[resource].copy()
    payload["resource"] = resource
    payload["available_surface_sets"] = sorted(SURFACE_SET_REGISTRY)
    payload["state_path"] = str(_state_path(repo_root, resource))
    return payload
