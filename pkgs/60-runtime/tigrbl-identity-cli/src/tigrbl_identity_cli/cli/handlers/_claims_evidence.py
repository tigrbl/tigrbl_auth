from __future__ import annotations

def handle_keys_retire(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "keys")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "keys.retire", "resource": "keys", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
    patched = _merge_record(record, {"status": "retired", "retired_at": _utc_now()})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, _mutation_result_payload("keys.retire", "keys", patched, state_path, mutation="retire", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"published_jwks": published_path}), rc=0)


def handle_keys_publish_jwks(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    include_secrets = bool(getattr(args, "include_secrets", False)) and not bool(getattr(args, "redact", False))
    path = _publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=include_secrets)
    payload = json.loads(path.read_text(encoding="utf-8"))
    checksum_value = hashlib.sha256(path.read_bytes()).hexdigest()
    if getattr(args, "output", None):
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if getattr(args, "format", "json") == "yaml":
            out_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        else:
            out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        emitted_path = str(out_path)
    else:
        emitted_path = str(path)
    return _emit_with_code(args, {"command": "keys.publish-jwks", "resource": "keys", "jwks": payload, "published_path": emitted_path, "checksum": checksum_value, "state_path": str(_state_path(repo_root, "keys"))}, rc=0)


def handle_discovery_show(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    profile = getattr(args, "profile", "baseline")
    discovery_root = repo_root / "specs" / "discovery" / "profiles" / profile
    payload = {"command": "discovery.show", "resource": "discovery", "profile": profile, "paths": {}, "documents": {}}
    for name in ("openid-configuration.json", "oauth-authorization-server.json", "oauth-protected-resource.json"):
        path = discovery_root / name
        if path.exists():
            payload["paths"][name] = str(path.relative_to(repo_root))
            payload["documents"][name] = json.loads(path.read_text(encoding="utf-8"))
    payload["state_path"] = str(_state_path(repo_root, "discovery"))
    return _emit_with_code(args, payload, rc=0)


def handle_discovery_validate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    openapi = validate_openapi_contract(repo_root)
    openrpc = validate_openrpc_contract(repo_root)
    profile = getattr(args, "profile", "baseline")
    discovery_root = repo_root / "specs" / "discovery" / "profiles" / profile
    required = [discovery_root / "openid-configuration.json", discovery_root / "oauth-authorization-server.json", discovery_root / "oauth-protected-resource.json"]
    missing = [str(path.relative_to(repo_root)) for path in required if not path.exists()]
    passed = openapi.passed and openrpc.passed and not missing
    payload = {
        "command": "discovery.validate",
        "resource": "discovery",
        "passed": passed,
        "summary": {
            "openapi_passed": openapi.passed,
            "openrpc_passed": openrpc.passed,
            "missing_discovery_files": missing,
        },
        "failures": missing,
        "state_path": str(_state_path(repo_root, "discovery")),
    }
    return _emit_with_code(args, payload, rc=0 if passed else 1)


def handle_discovery_publish(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    profile = getattr(args, "profile", "baseline")
    source_root = repo_root / "specs" / "discovery" / "profiles" / profile
    destination_root = Path(getattr(args, "output", None)).resolve() if getattr(args, "output", None) else (repo_root / "dist" / "discovery" / profile)
    destination_root.mkdir(parents=True, exist_ok=True)
    published: list[str] = []
    for name in ("openid-configuration.json", "oauth-authorization-server.json", "oauth-protected-resource.json"):
        source = source_root / name
        if source.exists() and not bool(getattr(args, "dry_run", False)):
            target = destination_root / name
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            published.append(str(target))
        elif source.exists():
            published.append(str((destination_root / name)))
    status_path = _state_path(repo_root, "discovery")
    if not bool(getattr(args, "dry_run", False)):
        _write_json(status_path, {"profile": profile, "published_at": _utc_now(), "published": published})
    return _emit_with_code(args, {"command": "discovery.publish", "resource": "discovery", "profile": profile, "published": published, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(status_path)}, rc=0)


def _json_diff(current: Any, baseline: Any, prefix: str = "") -> list[dict[str, Any]]:
    diffs: list[dict[str, Any]] = []
    if isinstance(current, dict) and isinstance(baseline, dict):
        keys = sorted(set(current) | set(baseline))
        for key in keys:
            new_prefix = f"{prefix}.{key}" if prefix else key
            if key not in baseline:
                diffs.append({"path": new_prefix, "change": "added", "value": current[key]})
            elif key not in current:
                diffs.append({"path": new_prefix, "change": "removed", "value": baseline[key]})
            else:
                diffs.extend(_json_diff(current[key], baseline[key], new_prefix))
        return diffs
    if current != baseline:
        diffs.append({"path": prefix or "$", "change": "changed", "current": current, "baseline": baseline})
    return diffs


def handle_discovery_diff(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    profile = getattr(args, "profile", "baseline")
    current_path = repo_root / "specs" / "discovery" / "profiles" / profile / "openid-configuration.json"
    if not current_path.exists():
        return _emit_with_code(args, {"command": "discovery.diff", "resource": "discovery", "error": "missing-current-discovery", "state_path": str(_state_path(repo_root, "discovery"))}, rc=1)
    current = json.loads(current_path.read_text(encoding="utf-8"))
    baseline_path = Path(getattr(args, "input_path", None)).resolve() if getattr(args, "input_path", None) else (repo_root / "dist" / "discovery" / profile / "openid-configuration.json")
    baseline = json.loads(baseline_path.read_text(encoding="utf-8")) if baseline_path.exists() else {}
    diffs = _json_diff(current, baseline)
    return _emit_with_code(args, {"command": "discovery.diff", "resource": "discovery", "profile": profile, "current_path": str(current_path.relative_to(repo_root)), "baseline_path": str(baseline_path) if baseline_path.exists() else None, "diffs": diffs, "state_path": str(_state_path(repo_root, "discovery"))}, rc=0)


def _portability_status_path(repo_root: Path, resource: str) -> Path:
    return _state_path(repo_root, resource)


def _export_payload(repo_root: Path) -> dict[str, Any]:
    resources = {}
    for resource in ("tenant", "client", "identity", "flow", "session", "token", "keys"):
        resources[resource] = _resource_store(repo_root, resource)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "exported_at": _utc_now(),
        "resources": resources,
    }


def handle_import_validate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    source_path = getattr(args, "input_path", None)
    if not source_path:
        raise SystemExit("--input is required")
    path = Path(source_path).resolve()
    if not path.exists():
        return _emit_with_code(args, {"command": "import.validate", "resource": "import", "passed": False, "failures": [f"missing input: {path}"], "state_path": str(_portability_status_path(repo_root, "import"))}, rc=1)
    payload = _load_structured_file(path)
    checksum_value = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = getattr(args, "checksum", None)
    passed = "resources" in payload and (expected in {None, checksum_value})
    failures = [] if passed else (["input payload does not contain resources"] if "resources" not in payload else ["checksum mismatch"])
    return _emit_with_code(args, {"command": "import.validate", "resource": "import", "passed": passed, "summary": {"checksum": checksum_value}, "failures": failures, "state_path": str(_portability_status_path(repo_root, "import"))}, rc=0 if passed else 1)


def handle_import_run(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    source_path = getattr(args, "input_path", None)
    if not source_path:
        raise SystemExit("--input is required")
    path = Path(source_path).resolve()
    payload = _load_structured_file(path)
    resources = payload.get("resources", {}) if isinstance(payload, dict) else {}
    applied_resources: list[str] = []
    if not bool(getattr(args, "dry_run", False)):
        for resource, store in resources.items():
            if isinstance(store, dict):
                _save_resource_store(repo_root, resource, store)
                applied_resources.append(resource)
        _write_json(_portability_status_path(repo_root, "import"), {"last_run_at": _utc_now(), "input": str(path), "applied_resources": applied_resources})
    else:
        applied_resources = sorted(resources)
    return _emit_with_code(args, {"command": "import.run", "resource": "import", "input": str(path), "applied_resources": applied_resources, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(_portability_status_path(repo_root, "import"))}, rc=0)


def handle_import_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    status = _load_jsonish(_portability_status_path(repo_root, "import"), default={})
    return _emit_with_code(args, {"command": "import.status", "resource": "import", "record": status, "state_path": str(_portability_status_path(repo_root, "import"))}, rc=0)


def handle_export_validate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    payload = _export_payload(repo_root)
    checksum_value = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    expected = getattr(args, "checksum", None)
    passed = expected in {None, checksum_value}
    failures = [] if passed else ["checksum mismatch"]
    return _emit_with_code(args, {"command": "export.validate", "resource": "export", "passed": passed, "summary": {"checksum": checksum_value, "resource_count": len(payload["resources"])}, "failures": failures, "state_path": str(_portability_status_path(repo_root, "export"))}, rc=0 if passed else 1)


def handle_export_run(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    payload = _export_payload(repo_root)
    output_path = Path(getattr(args, "output", None)).resolve() if getattr(args, "output", None) else (repo_root / "dist" / "operator-export" / f"export-{getattr(args, 'profile', 'baseline')}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    checksum_value = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    if not bool(getattr(args, "dry_run", False)):
        if getattr(args, "format", "json") == "yaml":
            output_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        else:
            output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _write_json(_portability_status_path(repo_root, "export"), {"last_run_at": _utc_now(), "output": str(output_path), "checksum": checksum_value})
    return _emit_with_code(args, {"command": "export.run", "resource": "export", "output": str(output_path), "checksum": checksum_value, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(_portability_status_path(repo_root, "export"))}, rc=0)


def handle_export_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    status = _load_jsonish(_portability_status_path(repo_root, "export"), default={})
    return _emit_with_code(args, {"command": "export.status", "resource": "export", "record": status, "state_path": str(_portability_status_path(repo_root, "export"))}, rc=0)


def handle_bootstrap_apply(args: Any) -> int:
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
    status_path = _portability_status_path(repo_root, "bootstrap")
    record = {"applied_at": _utc_now(), "profile": deployment.profile, "bundle_dir": str(bundle_dir.relative_to(repo_root)), "manifest": str(manifest_path.relative_to(repo_root))}
    if not bool(getattr(args, "dry_run", False)):
        _write_json(status_path, record)
    return _emit_with_code(args, {"command": "bootstrap.apply", "record": record, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(status_path)}, rc=0)


def handle_bootstrap_verify(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = repo_root / "dist" / "bootstrap" / deployment.profile
    required = [bundle_dir / "deployment.json", repo_root / "compliance" / "claims" / f"effective-target-claims.{deployment.profile}.yaml", repo_root / "compliance" / "evidence" / f"effective-release-evidence.{deployment.profile}.yaml"]
    missing = [str(path.relative_to(repo_root)) for path in required if not path.exists()]
    passed = not missing
    return _emit_with_code(args, {"command": "bootstrap.verify", "passed": passed, "summary": {"bundle_dir": str(bundle_dir.relative_to(repo_root)), "missing": missing}, "failures": missing, "state_path": str(_portability_status_path(repo_root, "bootstrap"))}, rc=0 if passed else 1)


def handle_migrate_apply(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    plan = yaml.safe_load((repo_root / "compliance" / "mappings" / "current-to-target-paths.yaml").read_text(encoding="utf-8"))
    status_path = _portability_status_path(repo_root, "migrate")
    record = {"applied_at": _utc_now(), "plan_summary": plan.get("summary", {}), "moved_paths": plan.get("target_paths", [])}
    if not bool(getattr(args, "dry_run", False)):
        _write_json(status_path, record)
    return _emit_with_code(args, {"command": "migrate.apply", "record": record, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(status_path)}, rc=0)


def _generic_resource_handler(resource: str, action: str):
    def _handler(args: Any) -> int:
        if action == "create":
            return _handle_stateful_create(args, resource)
        if action == "update":
            return _handle_stateful_update(args, resource)
        if action == "delete":
            return _handle_stateful_delete(args, resource)
        if action == "get":
            return _handle_stateful_get(args, resource)
        if action == "list":
            return _handle_stateful_list(args, resource)
        if action == "enable":
            return _toggle_enabled(args, resource, enabled=True)
        if action == "disable":
            return _toggle_enabled(args, resource, enabled=False)
        raise KeyError(f"Unsupported generic resource action: {resource}.{action}")

    return _handler


HANDLER_MAP = {
    "serve": handle_serve,
    "verify": handle_verify,
    "gate": handle_gate,
    "spec.generate": handle_spec_generate,
    "spec.validate": handle_spec_validate,
    "spec.diff": handle_spec_diff,
    "spec.report": handle_spec_report,
    "claims.lint": handle_claims_lint,
    "claims.show": handle_claims_show,
    "claims.status": handle_claims_status,
    "evidence.bundle": handle_evidence_bundle,
    "evidence.status": handle_evidence_status,
    "evidence.verify": handle_evidence_verify,
    "evidence.peer_status": handle_evidence_peer_status,
    "evidence.peer_execute": handle_evidence_peer_execute,
    "adr.list": handle_adr_list,
    "adr.show": handle_adr_show,
    "adr.new": handle_adr_new,
    "adr.index": handle_adr_index,
    "doctor": handle_doctor,
    "bootstrap.status": handle_bootstrap_status,
    "bootstrap.manifest": handle_bootstrap_manifest,
    "bootstrap.apply": handle_bootstrap_apply,
    "bootstrap.verify": handle_bootstrap_verify,
    "migrate.status": handle_migrate_status,
    "migrate.plan": handle_migrate_plan,
    "migrate.apply": handle_migrate_apply,
    "migrate.verify": handle_migrate_verify,
    "release.bundle": handle_release_bundle,
    "release.sign": handle_release_sign,
    "release.verify": handle_release_verify,
    "release.status": handle_release_status,
    "release.recertify": handle_release_recertify,
    "client.rotate_secret": handle_client_rotate_secret,
    "identity.set_password": handle_identity_set_password,
    "identity.lock": lambda args: _lock_identity(args, True),
    "identity.unlock": lambda args: _lock_identity(args, False),
    "session.revoke": lambda args: _revoke_resource(args, "session"),
    "session.revoke_all": handle_session_revoke_all,
    "token.introspect": handle_token_introspect,
    "token.revoke": lambda args: _revoke_resource(args, "token"),
    "token.exchange": handle_token_exchange,
    "keys.generate": handle_keys_generate,
    "keys.import": handle_keys_import,
    "keys.export": handle_keys_export,
    "keys.rotate": handle_keys_rotate,
    "keys.retire": handle_keys_retire,
    "keys.publish_jwks": handle_keys_publish_jwks,
    "discovery.show": handle_discovery_show,
    "discovery.validate": handle_discovery_validate,
    "discovery.publish": handle_discovery_publish,
    "discovery.diff": handle_discovery_diff,
    "import.validate": handle_import_validate,
    "import.run": handle_import_run,
    "import.status": handle_import_status,
    "export.validate": handle_export_validate,
    "export.run": handle_export_run,
    "export.status": handle_export_status,
}
for resource in ("tenant", "client", "identity", "flow"):
    for action in ("create", "update", "delete", "get", "list", "enable", "disable"):
        HANDLER_MAP[f"{resource}.{action}"] = _generic_resource_handler(resource, action)
for resource in ("session", "token"):
    for action in ("get", "list"):
        HANDLER_MAP[f"{resource}.{action}"] = _generic_resource_handler(resource, action)
for action in ("get", "list", "delete"):
    HANDLER_MAP[f"keys.{action}"] = _generic_resource_handler("keys", action)


__all__ = ["HANDLER_MAP"]

# -----------------------------------------------------------------------------
# Service-layer overrides
# -----------------------------------------------------------------------------

from tigrbl_identity_storage_runtime.operator_store import OperationContext, TransactionResult, ArtifactResult
from tigrbl_identity_storage_runtime.resource_service import (
    OperatorStateError,
    create_resource as _svc_create_resource,
    delete_resource as _svc_delete_resource,
    get_resource as _svc_get_resource,
    list_resource_result as _svc_list_resource_result,
    rotate_client_secret as _svc_rotate_client_secret,
    toggle_resource as _svc_toggle_resource,
    update_resource as _svc_update_resource,
)
from tigrbl_identity_storage_runtime.key_management import (
    delete_operator_key_for_context,
    export_operator_key_for_context,
    generate_operator_key_for_context,
    get_operator_key_for_context,
    import_operator_key_for_context,
    list_operator_keys_for_context,
    publish_operator_jwks_for_context,
    retire_operator_key_for_context,
    rotate_operator_key_for_context,
)
from tigrbl_identity_storage_runtime.resource_service import lock_identity as _svc_lock_identity, set_identity_password as _svc_set_identity_password
