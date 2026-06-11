def _load_records_from_snapshot(path: Path, *, tenant: str | None = None) -> dict[str, dict[str, Any]]:
    loaded = load_structured(path, default={})
    rows: dict[str, dict[str, Any]] = {}
    if isinstance(loaded, Mapping):
        items = loaded.values()
    elif isinstance(loaded, list):
        items = loaded
    else:
        items = []
    for item in items:
        if not isinstance(item, Mapping):
            continue
        record_id = item.get("id")
        if not record_id:
            continue
        if tenant is not None and item.get("tenant") != tenant:
            continue
        rows[str(record_id)] = copy.deepcopy(dict(item))
    return rows


def load_records(repo_root: Path, resource: str, tenant: str | None = None) -> dict[str, dict[str, Any]]:
    db_path = operator_database_path(repo_root)
    with _connect(repo_root) as conn:
        sql = "SELECT resource, id, status, enabled, created_at, updated_at, actor, profile, tenant, issuer, revision, data_json FROM records WHERE resource = ?"
        params: list[Any] = [resource]
        if tenant is not None:
            sql += " AND tenant = ?"
            params.append(tenant)
        sql += " ORDER BY id"
        rows = conn.execute(sql, params).fetchall()
    if rows or db_path.exists():
        return {str(row["id"]): _row_to_record(row) for row in rows}
    return _load_records_from_snapshot(resource_state_path(repo_root, resource), tenant=tenant)


def default_status(resource: str) -> str:
    if resource in {"keys"}:
        return "staged"
    return "active"


def deep_merge(base: Mapping[str, Any], patch: Mapping[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(dict(base))
    for key, value in patch.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def make_record(resource: str, record_id: str, context: OperationContext, patch: Mapping[str, Any] | None = None) -> dict[str, Any]:
    patch = dict(patch or {})
    now = utc_now()
    data = copy.deepcopy(dict(patch))
    if context.tenant is None and data.get("tenant") is not None:
        tenant = str(data.pop("tenant"))
    else:
        tenant = context.tenant
    status = str(data.pop("status", default_status(resource)))
    enabled = bool(data.pop("enabled", status not in {"disabled", "revoked", "retired", "locked"}))
    return {
        "id": str(record_id),
        "resource": resource,
        "status": status,
        "enabled": enabled,
        "created_at": now,
        "updated_at": now,
        "actor": context.actor,
        "profile": context.profile,
        "tenant": tenant,
        "issuer": context.issuer,
        "revision": 1,
        "data": data,
    }


def matches_record(record: Mapping[str, Any], spec: FilterSpec) -> bool:
    if spec.status_filter and str(record.get("status")) != str(spec.status_filter):
        return False
    if spec.filter_expr:
        term = str(spec.filter_expr).strip().lower()
        haystacks = [
            str(record.get("id", "")).lower(),
            str(record.get("status", "")).lower(),
            str(record.get("tenant", "")).lower(),
            json.dumps(record.get("data", {}), sort_keys=True).lower(),
        ]
        data = record.get("data") or {}
        if isinstance(data, Mapping):
            for key in ("name", "display_name", "tenant_id", "client_id", "username", "email", "kid", "software_id"):
                haystacks.append(str(data.get(key, "")).lower())
        if not any(term in item for item in haystacks):
            return False
    return True


def sort_records(records: list[dict[str, Any]], sort_key: str = "id") -> list[dict[str, Any]]:
    def _sort_value(item: Mapping[str, Any]) -> tuple[str, str]:
        data = item.get("data") if isinstance(item.get("data"), Mapping) else {}
        primary = data.get(sort_key, item.get(sort_key, ""))
        return (str(primary or ""), str(item.get("id", "")))
    return [copy.deepcopy(dict(item)) for item in sorted(records, key=_sort_value)]


def list_records(repo_root: Path, resource: str, spec: FilterSpec | None = None, tenant: str | None = None) -> list[dict[str, Any]]:
    spec = spec or FilterSpec()
    records = load_records(repo_root, resource, tenant=tenant).values()
    filtered = [copy.deepcopy(dict(item)) for item in records if matches_record(item, spec)]
    sorted_items = sort_records(filtered, spec.sort)
    return sorted_items[spec.offset : spec.offset + spec.limit]


def latest_event(repo_root: Path, *, predicate=None) -> dict[str, Any] | None:
    items = sorted(read_jsonl(audit_log_path(repo_root)), key=lambda item: str(item.get("occurred_at", "")), reverse=True)
    if predicate is None:
        return items[0] if items else None
    for item in items:
        try:
            if predicate(item):
                return item
        except Exception:
            continue
    return None


def build_transaction_entry(
    context: OperationContext,
    *,
    status: str,
    record_id: str | None = None,
    changed_ids: list[str] | None = None,
    summary: Mapping[str, Any] | None = None,
    before_checksum: str | None = None,
    after_checksum: str | None = None,
) -> dict[str, Any]:
    return {
        "transaction_id": synthetic_id("txn"),
        "ts": utc_now(),
        "command": context.command,
        "resource": context.resource,
        "status": status,
        "record_id": record_id,
        "changed_ids": list(changed_ids or ([] if record_id is None else [record_id])),
        "summary": dict(summary or {}),
        "actor": context.actor,
        "profile": context.profile,
        "tenant": context.tenant,
        "issuer": context.issuer,
        "before_checksum": before_checksum,
        "after_checksum": after_checksum,
    }


def build_audit_entry(
    context: OperationContext,
    *,
    transaction_id: str,
    status: str,
    target_id: str | None = None,
    details: Mapping[str, Any] | None = None,
    source_surface: str = "operator",
) -> dict[str, Any]:
    return {
        "id": synthetic_id("audit"),
        "tenant_id": context.tenant,
        "actor_user_id": context.actor,
        "actor_client_id": None,
        "session_id": None,
        "event_type": context.command,
        "target_type": context.resource,
        "target_id": target_id,
        "outcome": status,
        "request_id": transaction_id,
        "occurred_at": utc_now(),
        "details": {**dict(details or {}), "source_surface": source_surface},
    }


def _sync_resource_snapshot(repo_root: Path, resource: str) -> None:
    rows = load_records(repo_root, resource, tenant=None)
    write_structured(resource_state_path(repo_root, resource), rows, fmt="json")
    _write_metadata_snapshot(repo_root)


def _record_equal_without_revision(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    def _strip(payload: Mapping[str, Any]) -> dict[str, Any]:
        cleaned = copy.deepcopy(dict(payload))
        cleaned.pop("revision", None)
        return cleaned
    return _strip(left) == _strip(right)


def commit_mutation(context: OperationContext, *, records: Mapping[str, Mapping[str, Any]], transaction: Mapping[str, Any], audit_entry: Mapping[str, Any] | None = None) -> None:
    root = operator_state_root(context.repo_root)
    changed_ids = {str(item) for item in list(transaction.get("changed_ids") or [])}
    with _connect(context.repo_root) as conn:
        conn.execute("BEGIN IMMEDIATE")
        existing_all_rows = conn.execute(
            "SELECT resource, id, status, enabled, created_at, updated_at, actor, profile, tenant, issuer, revision, data_json FROM records WHERE resource = ? ORDER BY id",
            (context.resource,),
        ).fetchall()
        existing_all = {str(row["id"]): _row_to_record(row) for row in existing_all_rows}
        if context.tenant is None:
            full_records = {str(key): _normalize_record(context.resource, str(key), value, fallback_actor=context.actor) for key, value in records.items()}
        else:
            preserved = {record_id: record for record_id, record in existing_all.items() if record.get("tenant") != context.tenant}
            scoped = {str(key): _normalize_record(context.resource, str(key), value, fallback_actor=context.actor) for key, value in records.items()}
            for row in scoped.values():
                row["tenant"] = context.tenant
            full_records = {**preserved, **scoped}
        if not context.dry_run:
            conn.execute("DELETE FROM records WHERE resource = ?", (context.resource,))
            for record_id in sorted(full_records):
                record = copy.deepcopy(full_records[record_id])
                previous = existing_all.get(record_id)
                incoming_revision = int(record.get("revision") or 1)
                if previous is None:
                    record["revision"] = max(1, incoming_revision)
                elif record_id in changed_ids and not _record_equal_without_revision(previous, record):
                    record["revision"] = max(int(previous.get("revision") or 0) + 1, incoming_revision)
                else:
                    record["revision"] = max(int(previous.get("revision") or 1), incoming_revision)
                _insert_record(conn, record)
        _insert_transaction(conn, transaction)
        if audit_entry is not None:
            _insert_audit(conn, audit_entry)
        _insert_activity(
            conn,
            {
                "ts": utc_now(),
                "kind": context.command,
                "resource": context.resource,
                "id": transaction.get("record_id"),
                "status": transaction.get("status"),
                "transaction_id": transaction.get("transaction_id"),
            },
        )
        _upsert_metadata(conn, "last_transaction_id", transaction.get("transaction_id"))
        _upsert_metadata(conn, "last_transaction_status", transaction.get("status"))
        _upsert_metadata(conn, "repo_mutation_dependency", False)
        conn.commit()
    if not context.dry_run:
        _sync_resource_snapshot(context.repo_root, context.resource)
    _append_jsonl_file(transaction_log_path(context.repo_root), transaction)
    if audit_entry is not None:
        _append_jsonl_file(audit_log_path(context.repo_root), audit_entry)
    _append_jsonl_file(
        activity_log_path(context.repo_root),
        {
            "ts": utc_now(),
            "kind": context.command,
            "resource": context.resource,
            "id": transaction.get("record_id"),
            "status": transaction.get("status"),
            "transaction_id": transaction.get("transaction_id"),
        },
    )
    _write_metadata_snapshot(context.repo_root)


def operator_store_summary(repo_root: Path) -> dict[str, Any]:
    operator_state_root(repo_root)
    _write_metadata_snapshot(repo_root)
    payload = _metadata_payload(repo_root)
    payload.update(
        {
            "database_present": operator_database_path(repo_root).exists(),
            "audit_log_path": safe_display_path(audit_log_path(repo_root), repo_root, external_label="<operator-state>"),
            "transaction_log_path": safe_display_path(transaction_log_path(repo_root), repo_root, external_label="<operator-state>"),
            "activity_log_path": safe_display_path(activity_log_path(repo_root), repo_root, external_label="<operator-state>"),
        }
    )
    return payload


__all__ = [
    "ArtifactResult",
    "FilterSpec",
    "OPERATOR_STORE_SCHEMA_VERSION",
    "PORTABILITY_SCHEMA_VERSION",
    "OperationContext",
    "TransactionResult",
    "activity_log_path",
    "append_jsonl",
    "audit_log_path",
    "build_audit_entry",
    "build_transaction_entry",
    "commit_mutation",
    "deep_merge",
    "default_status",
    "display_path",
    "latest_event",
    "list_records",
    "load_records",
    "load_structured",
    "make_record",
    "matches_record",
    "operator_database_path",
    "operator_state_metadata_path",
    "operator_state_root",
    "operator_store_summary",
    "read_jsonl",
    "resource_state_path",
    "sha256_json",
    "sha256_path",
    "sort_records",
    "synthetic_id",
    "transaction_log_path",
    "utc_now",
    "validate_checksum",
    "write_structured",
]
