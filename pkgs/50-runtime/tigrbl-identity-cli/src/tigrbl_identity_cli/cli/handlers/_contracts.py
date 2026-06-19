from __future__ import annotations

def _handle_stateful_create(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    payload = _mutation_payload(args)
    identifier = _record_identifier(args, payload, resource)
    existing = store.get(identifier)
    behavior = str(getattr(args, "if_exists", "fail"))
    if existing is not None and behavior == "fail":
        return _emit_with_code(args, _mutation_result_payload(f"{resource}.create", resource, existing, _state_path(repo_root, resource), mutation="create", persisted=False, dry_run=bool(getattr(args, "dry_run", False)), extras={"error": "already-exists", "if_exists": behavior}), rc=1)
    if existing is not None and behavior == "skip":
        return _emit_with_code(args, _mutation_result_payload(f"{resource}.create", resource, existing, _state_path(repo_root, resource), mutation="create", persisted=False, dry_run=bool(getattr(args, "dry_run", False)), extras={"skipped": True, "if_exists": behavior}), rc=0)
    record = _base_record(resource, identifier, payload) if existing is None else (_base_record(resource, identifier, payload) if behavior == "replace" else _merge_record(existing, payload))
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.create", resource, record, state_path, mutation="create", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"if_exists": behavior}), rc=0)


def _handle_stateful_update(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    payload = _mutation_payload(args)
    identifier = _record_identifier(args, payload, resource)
    existing = store.get(identifier)
    behavior = str(getattr(args, "if_missing", "fail"))
    if existing is None and behavior == "fail":
        return _emit_with_code(args, {"command": f"{resource}.update", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    if existing is None and behavior == "skip":
        return _emit_with_code(args, {"command": f"{resource}.update", "resource": resource, "id": identifier, "skipped": True, "state_path": str(_state_path(repo_root, resource))}, rc=0)
    record = _base_record(resource, identifier, payload) if existing is None else _merge_record(existing, payload)
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.update", resource, record, state_path, mutation="update", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"if_missing": behavior}), rc=0)


def _handle_stateful_delete(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    existing = store.get(identifier)
    if existing is None:
        return _emit_with_code(args, {"command": f"{resource}.delete", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    if not bool(getattr(args, "dry_run", False)):
        removed = store.pop(identifier)
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        removed = existing
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, {"command": f"{resource}.delete", "resource": resource, "id": identifier, "deleted": True, "dry_run": bool(getattr(args, "dry_run", False)), "record": removed, "state_path": str(state_path)}, rc=0)


def _handle_stateful_get(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, resource)
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"{resource}.get", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    return _emit_with_code(args, _query_result_payload(f"{resource}.get", resource, record=record, state_path=_state_path(repo_root, resource)), rc=0)


def _handle_stateful_list(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    items, total = _filtered_items(store, filter_text=getattr(args, "filter", None), status_filter=getattr(args, "status_filter", None), sort_key=str(getattr(args, "sort", "id")), offset=int(getattr(args, "offset", 0)), limit=int(getattr(args, "limit", 50)))
    return _emit_with_code(args, _query_result_payload(f"{resource}.list", resource, items=items, total=total, state_path=_state_path(repo_root, resource), offset=int(getattr(args, "offset", 0)), limit=int(getattr(args, "limit", 50))), rc=0)


def _toggle_enabled(args: Any, resource: str, *, enabled: bool) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, resource)
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"{resource}.{'enable' if enabled else 'disable'}", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    patched = _merge_record(record, {"enabled": enabled, "status": "active" if enabled else "disabled"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.{'enable' if enabled else 'disable'}", resource, patched, state_path, mutation="enable" if enabled else "disable", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def handle_client_rotate_secret(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "client")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "client.rotate-secret", "resource": "client", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "client"))}, rc=3)
    secret_value = secrets.token_urlsafe(24)
    patched = _merge_record(record, {"secret_rotated_at": _utc_now(), "secret_sha256": hashlib.sha256(secret_value.encode("utf-8")).hexdigest(), "secret_reference": f"rotated:{identifier}:{int(datetime.now(timezone.utc).timestamp())}"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "client", store)
    else:
        state_path = _state_path(repo_root, "client")
    return _emit_with_code(args, _mutation_result_payload("client.rotate-secret", "client", patched, state_path, mutation="rotate-secret", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"secret_preview": secret_value[:8] + "..."}), rc=0)


def handle_identity_set_password(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "identity")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "identity.set-password", "resource": "identity", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "identity"))}, rc=3)
    payload = _mutation_payload(args)
    raw_password = str(payload.get("password") or payload.get("secret") or secrets.token_urlsafe(18))
    patched = _merge_record(record, {"password_updated_at": _utc_now(), "password_sha256": hashlib.sha256(raw_password.encode("utf-8")).hexdigest(), "password_hint": "sha256"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "identity", store)
    else:
        state_path = _state_path(repo_root, "identity")
    return _emit_with_code(args, _mutation_result_payload("identity.set-password", "identity", patched, state_path, mutation="set-password", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def _lock_identity(args: Any, locked: bool) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "identity")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"identity.{'lock' if locked else 'unlock'}", "resource": "identity", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "identity"))}, rc=3)
    patched = _merge_record(record, {"locked": locked, "status": "locked" if locked else "active"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "identity", store)
    else:
        state_path = _state_path(repo_root, "identity")
    return _emit_with_code(args, _mutation_result_payload(f"identity.{'lock' if locked else 'unlock'}", "identity", patched, state_path, mutation="lock" if locked else "unlock", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def _revoke_resource(args: Any, resource: str, *, field: str = "revoked_at") -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, resource)
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"{resource}.revoke", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    patched = _merge_record(record, {field: _utc_now(), "status": "revoked", "enabled": False})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.revoke", resource, patched, state_path, mutation="revoke", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def handle_session_revoke_all(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "session")
    matched, _ = _filtered_items(store, filter_text=getattr(args, "filter", None), status_filter=getattr(args, "status_filter", None), sort_key="id", offset=0, limit=max(len(store), 1))
    revoked_ids: list[str] = []
    if not bool(getattr(args, "dry_run", False)):
        for item in matched:
            identifier = str(item["id"])
            store[identifier] = _merge_record(store[identifier], {"revoked_at": _utc_now(), "status": "revoked", "enabled": False})
            revoked_ids.append(identifier)
        state_path = _save_resource_store(repo_root, "session", store)
    else:
        revoked_ids = [str(item["id"]) for item in matched]
        state_path = _state_path(repo_root, "session")
    return _emit_with_code(args, {"command": "session.revoke-all", "resource": "session", "revoked_ids": revoked_ids, "revoked_count": len(revoked_ids), "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(state_path)}, rc=0)


def handle_token_introspect(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "token")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "token.introspect", "resource": "token", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "token"))}, rc=3)
    active = str(record.get("status")) not in {"revoked", "retired", "expired"} and not bool(record.get("revoked_at"))
    payload = _query_result_payload("token.introspect", "token", record=record, state_path=_state_path(repo_root, "token"), extras={"active": active})
    return _emit_with_code(args, payload, rc=0)


def handle_token_exchange(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    source_id = getattr(args, "id", None)
    if not source_id:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "token")
    source = store.get(source_id)
    if source is None:
        return _emit_with_code(args, {"command": "token.exchange", "resource": "token", "id": source_id, "error": "not-found", "state_path": str(_state_path(repo_root, "token"))}, rc=3)
    payload = _mutation_payload(args)
    new_id = str(payload.get("new_id") or f"{source_id}-xchg-{secrets.token_hex(4)}")
    record = _base_record("token", new_id, payload)
    record.update({"exchanged_from": source_id, "token_type": payload.get("token_type", "urn:ietf:params:oauth:token-type:access_token")})
    if not bool(getattr(args, "dry_run", False)):
        store[new_id] = record
        state_path = _save_resource_store(repo_root, "token", store)
    else:
        state_path = _state_path(repo_root, "token")
    return _emit_with_code(args, _mutation_result_payload("token.exchange", "token", record, state_path, mutation="exchange", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"source_id": source_id}), rc=0)


def _jwks_public_keys(store: dict[str, dict[str, Any]], *, include_secrets: bool = False) -> list[dict[str, Any]]:
    keys: list[dict[str, Any]] = []
    for record in _sort_items(list(store.values()), "id"):
        if str(record.get("status")) == "retired":
            continue
        key = {
            "kid": record.get("kid") or record.get("id"),
            "kty": record.get("kty", "OKP"),
            "use": record.get("use", "sig"),
            "alg": record.get("alg") or ("EdDSA" if record.get("kty", "OKP") == "OKP" else None),
            "crv": record.get("curve") if record.get("kty") in {"EC", "OKP"} else None,
            "status": record.get("status", "active"),
        }
        if include_secrets and record.get("material") is not None:
            key["material"] = record["material"]
        keys.append({k: v for k, v in key.items() if v is not None})
    return keys


def _jwks_publish_path(repo_root: Path, profile: str) -> Path:
    return repo_root / "dist" / "jwks" / profile / "jwks.json"


def _publish_jwks(repo_root: Path, profile: str, *, include_secrets: bool = False) -> Path:
    store = _resource_store(repo_root, "keys")
    payload = {"keys": _jwks_public_keys(store, include_secrets=include_secrets)}
    path = _jwks_publish_path(repo_root, profile)
    _write_json(path, payload)
    return path


def handle_keys_generate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    payload = _mutation_payload(args)
    identifier = _record_identifier(args, payload, "key")
    key_id = str(getattr(args, "kid", None) or payload.get("kid") or identifier)
    record = _base_record("keys", identifier, payload)
    record.update({
        "kid": key_id,
        "alg": getattr(args, "alg", None) or payload.get("alg") or ("EdDSA" if (getattr(args, "kty", "OKP") or payload.get("kty")) == "OKP" else "RS256"),
        "use": getattr(args, "use", None) or payload.get("use") or "sig",
        "kty": getattr(args, "kty", None) or payload.get("kty") or "OKP",
        "curve": getattr(args, "curve", None) or payload.get("curve") or "Ed25519",
        "status": "active" if bool(getattr(args, "activate", False)) else "staged",
        "material": {"reference": f"generated:{key_id}:{secrets.token_hex(8)}"},
        "retire_after": getattr(args, "retire_after", None) or payload.get("retire_after"),
    })
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, _mutation_result_payload("keys.generate", "keys", record, state_path, mutation="generate", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"published_jwks": published_path}), rc=0)


def handle_keys_import(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    source_path = getattr(args, "from_file", None) or getattr(args, "input_path", None)
    if not source_path:
        raise SystemExit("--from-file or --input is required")
    payload = _load_structured_file(Path(source_path).resolve())
    identifier = _record_identifier(args, payload, "key")
    record = _base_record("keys", identifier, payload)
    record.update({
        "kid": payload.get("kid") or getattr(args, "kid", None) or identifier,
        "alg": payload.get("alg") or getattr(args, "alg", None),
        "use": payload.get("use") or getattr(args, "use", None) or "sig",
        "kty": payload.get("kty") or getattr(args, "kty", None) or "OKP",
        "curve": payload.get("crv") or payload.get("curve") or getattr(args, "curve", None),
        "status": "active" if bool(getattr(args, "activate", False)) else payload.get("status", "staged"),
        "material": payload,
    })
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, _mutation_result_payload("keys.import", "keys", record, state_path, mutation="import", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"source": str(Path(source_path).resolve()), "published_jwks": published_path}), rc=0)


def handle_keys_export(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    identifier = getattr(args, "id", None)
    if identifier:
        record = store.get(identifier)
        if record is None:
            return _emit_with_code(args, {"command": "keys.export", "resource": "keys", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
        export_payload: Any = record
    else:
        export_payload = {"keys": list(_sort_items(list(store.values()), "id"))}
    checksum_value = hashlib.sha256(json.dumps(export_payload, sort_keys=True).encode("utf-8")).hexdigest()
    if getattr(args, "output", None):
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if getattr(args, "format", "json") == "yaml":
            out_path.write_text(yaml.safe_dump(export_payload, sort_keys=False), encoding="utf-8")
        else:
            out_path.write_text(json.dumps(export_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        output_path = str(out_path)
    else:
        output_path = None
    return _emit_with_code(args, _query_result_payload("keys.export", "keys", record=export_payload if identifier else None, items=export_payload.get("keys") if isinstance(export_payload, dict) and "keys" in export_payload else None, total=len(export_payload.get("keys", [])) if isinstance(export_payload, dict) and "keys" in export_payload else None, state_path=_state_path(repo_root, "keys"), extras={"checksum": checksum_value, "output_path": output_path}), rc=0)


def handle_keys_rotate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    target_id = getattr(args, "id", None)
    if target_id is None:
        active = [item for item in store.values() if str(item.get("status")) == "active"]
        if not active:
            return _emit_with_code(args, {"command": "keys.rotate", "resource": "keys", "error": "no-active-key", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
        target_id = str(_sort_items(active, "updated_at")[0]["id"])
    current = store.get(target_id)
    if current is None:
        return _emit_with_code(args, {"command": "keys.rotate", "resource": "keys", "id": target_id, "error": "not-found", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
    successor_id = f"{target_id}-rotated-{secrets.token_hex(4)}"
    successor = _base_record("keys", successor_id, {})
    successor.update({
        "kid": getattr(args, "kid", None) or successor_id,
        "alg": getattr(args, "alg", None) or current.get("alg"),
        "use": getattr(args, "use", None) or current.get("use"),
        "kty": getattr(args, "kty", None) or current.get("kty"),
        "curve": getattr(args, "curve", None) or current.get("curve"),
        "status": "active" if bool(getattr(args, "activate", True)) else "staged",
        "material": {"reference": f"rotated:{successor_id}:{secrets.token_hex(8)}"},
        "rotates": target_id,
        "retire_after": getattr(args, "retire_after", None) or current.get("retire_after"),
    })
    retired = _merge_record(current, {"status": "retired", "retired_at": _utc_now()})
    if not bool(getattr(args, "dry_run", False)):
        store[target_id] = retired
        store[successor_id] = successor
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, {"command": "keys.rotate", "resource": "keys", "previous_record": retired, "record": successor, "dry_run": bool(getattr(args, "dry_run", False)), "persisted": not bool(getattr(args, "dry_run", False)), "state_path": str(state_path), "published_jwks": published_path}, rc=0)
