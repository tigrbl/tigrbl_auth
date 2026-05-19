from __future__ import annotations

"""Durable SQLite-backed operator-plane persistence helpers."""

import copy
import hashlib
import json
import os
import secrets
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from tigrbl_auth.path_safety import safe_display_path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


OPERATOR_STORE_SCHEMA_VERSION = 1
PORTABILITY_SCHEMA_VERSION = 3
_OPERATOR_DB_FILENAME = "operator_plane.sqlite3"


@dataclass(slots=True, frozen=True)
class OperationContext:
    repo_root: Path
    command: str
    resource: str
    dry_run: bool = False
    actor: str = "system"
    profile: str | None = None
    tenant: str | None = None
    issuer: str | None = None


@dataclass(slots=True, frozen=True)
class FilterSpec:
    status_filter: str | None = None
    filter_expr: str | None = None
    sort: str = "id"
    offset: int = 0
    limit: int = 50


@dataclass(slots=True)
class TransactionResult:
    transaction_id: str
    command: str
    resource: str
    status: str
    dry_run: bool
    persisted: bool
    record: dict[str, Any] | None = None
    items: list[dict[str, Any]] | None = None
    changed_ids: list[str] = field(default_factory=list)
    summary: dict[str, Any] | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "transaction_id": self.transaction_id,
            "command": self.command,
            "resource": self.resource,
            "status": self.status,
            "dry_run": self.dry_run,
            "persisted": self.persisted,
        }
        if self.record is not None:
            payload["record"] = self.record
        if self.items is not None:
            payload["items"] = self.items
            payload["count"] = len(self.items)
        if self.changed_ids:
            payload["changed_ids"] = list(self.changed_ids)
        if self.summary is not None:
            payload["summary"] = self.summary
        return payload


@dataclass(slots=True)
class ArtifactResult:
    command: str
    resource: str
    status: str
    path: str
    summary: dict[str, Any] = field(default_factory=dict)
    checksum: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "command": self.command,
            "resource": self.resource,
            "status": self.status,
            "artifact_path": self.path,
            "summary": dict(self.summary),
        }
        if self.checksum is not None:
            payload["checksum"] = self.checksum
        return payload


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def synthetic_id(prefix: str) -> str:
    return f"{prefix}-{secrets.token_hex(6)}"


def _hash_repo_root(repo_root: Path) -> str:
    try:
        value = str(repo_root.resolve())
    except Exception:
        value = str(repo_root)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _state_home() -> Path:
    override = os.getenv("TIGRBL_AUTH_OPERATOR_STATE_DIR")
    if override:
        return Path(override).expanduser()
    xdg = os.getenv("XDG_STATE_HOME")
    if xdg:
        return Path(xdg).expanduser() / "tigrbl_auth" / "operator-plane"
    return Path.home() / ".local" / "state" / "tigrbl_auth" / "operator-plane"


def operator_state_root(repo_root: Path) -> Path:
    namespace = f"{repo_root.name or 'repo'}-{_hash_repo_root(repo_root)}"
    path = _state_home() / namespace
    path.mkdir(parents=True, exist_ok=True)
    (path / "logs").mkdir(parents=True, exist_ok=True)
    (path / "snapshots").mkdir(parents=True, exist_ok=True)
    return path


def operator_database_path(repo_root: Path) -> Path:
    return operator_state_root(repo_root) / _OPERATOR_DB_FILENAME


def operator_state_metadata_path(repo_root: Path) -> Path:
    return operator_state_root(repo_root) / "metadata.json"


def resource_state_path(repo_root: Path, resource: str) -> Path:
    return operator_state_root(repo_root) / "snapshots" / f"{resource}.json"


def transaction_log_path(repo_root: Path) -> Path:
    return operator_state_root(repo_root) / "logs" / "transactions.jsonl"


def audit_log_path(repo_root: Path) -> Path:
    return operator_state_root(repo_root) / "logs" / "audit-events.jsonl"


def activity_log_path(repo_root: Path) -> Path:
    return operator_state_root(repo_root) / "logs" / "activity.jsonl"


def display_path(path: Path, repo_root: Path) -> str:
    return safe_display_path(path, repo_root)


def sha256_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_checksum(path: Path) -> str:
    return sha256_path(path)


def load_structured(path: Path, *, default: Any | None = None) -> Any:
    if not path.exists():
        return copy.deepcopy(default)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("YAML support is unavailable")
        loaded = yaml.safe_load(text)
        return loaded if loaded is not None else copy.deepcopy(default)
    loaded = json.loads(text)
    return loaded if loaded is not None else copy.deepcopy(default)


def write_structured(path: Path, payload: Any, *, fmt: str = "json") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "yaml" or path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("YAML support is unavailable")
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    else:
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _jsonl_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _append_jsonl_file(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), sort_keys=True) + "\n")


def _connect_state_root(state_root: Path) -> sqlite3.Connection:
    state_root.mkdir(parents=True, exist_ok=True)
    (state_root / "logs").mkdir(parents=True, exist_ok=True)
    (state_root / "snapshots").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(state_root / _OPERATOR_DB_FILENAME), timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=30000")
    _initialize_schema(conn, state_root)
    return conn


def _connect(repo_root: Path) -> sqlite3.Connection:
    return _connect_state_root(operator_state_root(repo_root))


def _metadata_payload(repo_root: Path) -> dict[str, Any]:
    root = operator_state_root(repo_root)
    return {
        "schema_version": OPERATOR_STORE_SCHEMA_VERSION,
        "backend": "sqlite-authoritative",
        "state_root": safe_display_path(root, repo_root, external_label="<operator-state>"),
        "database_path": safe_display_path(operator_database_path(repo_root), repo_root, external_label="<operator-state>"),
        "snapshot_root": safe_display_path(root / "snapshots", repo_root, external_label="<operator-state>"),
        "log_root": safe_display_path(root / "logs", repo_root, external_label="<operator-state>"),
        "repo_mutation_dependency": False,
        "concurrency_model": "sqlite-wal-begin-immediate",
        "tenancy_enforced": True,
        "portability_schema_version": PORTABILITY_SCHEMA_VERSION,
    }


def _write_metadata_snapshot(repo_root: Path) -> None:
    write_structured(operator_state_metadata_path(repo_root), _metadata_payload(repo_root))


def _upsert_metadata(conn: sqlite3.Connection, key: str, value: Any) -> None:
    conn.execute(
        "INSERT INTO metadata(key, value_json, updated_at) VALUES(?, ?, ?) ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json, updated_at=excluded.updated_at",
        (key, json.dumps(value, sort_keys=True), utc_now()),
    )


def _initialize_schema(conn: sqlite3.Connection, state_root: Path) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value_json TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS records (
            resource TEXT NOT NULL,
            id TEXT NOT NULL,
            status TEXT NOT NULL,
            enabled INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            actor TEXT,
            profile TEXT,
            tenant TEXT,
            issuer TEXT,
            revision INTEGER NOT NULL DEFAULT 1,
            data_json TEXT NOT NULL DEFAULT '{}',
            PRIMARY KEY (resource, id)
        );
        CREATE INDEX IF NOT EXISTS idx_records_resource_status ON records(resource, status);
        CREATE INDEX IF NOT EXISTS idx_records_resource_tenant ON records(resource, tenant);
        CREATE TABLE IF NOT EXISTS transaction_log (
            transaction_id TEXT PRIMARY KEY,
            ts TEXT NOT NULL,
            command TEXT NOT NULL,
            resource TEXT NOT NULL,
            status TEXT NOT NULL,
            record_id TEXT,
            changed_ids_json TEXT NOT NULL,
            summary_json TEXT NOT NULL,
            actor TEXT,
            profile TEXT,
            tenant TEXT,
            issuer TEXT,
            before_checksum TEXT,
            after_checksum TEXT
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY,
            tenant_id TEXT,
            actor_user_id TEXT,
            actor_client_id TEXT,
            session_id TEXT,
            event_type TEXT NOT NULL,
            target_type TEXT NOT NULL,
            target_id TEXT,
            outcome TEXT NOT NULL,
            request_id TEXT,
            occurred_at TEXT NOT NULL,
            details_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS activity_log (
            seq INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            kind TEXT NOT NULL,
            resource TEXT NOT NULL,
            record_id TEXT,
            status TEXT,
            transaction_id TEXT
        );
        """
    )
    _upsert_metadata(conn, "backend", "sqlite-authoritative")
    _upsert_metadata(conn, "schema_version", OPERATOR_STORE_SCHEMA_VERSION)
    _upsert_metadata(conn, "portability_schema_version", PORTABILITY_SCHEMA_VERSION)
    _upsert_metadata(conn, "state_root", str(state_root))


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    data = json.loads(row["data_json"] or "{}")
    if not isinstance(data, Mapping):
        data = {}
    return {
        "id": str(row["id"]),
        "resource": str(row["resource"]),
        "status": str(row["status"]),
        "enabled": bool(row["enabled"]),
        "created_at": str(row["created_at"]),
        "updated_at": str(row["updated_at"]),
        "actor": row["actor"],
        "profile": row["profile"],
        "tenant": row["tenant"],
        "issuer": row["issuer"],
        "revision": int(row["revision"]),
        "data": copy.deepcopy(dict(data)),
    }


def _normalize_record(resource: str, record_id: str, record: Mapping[str, Any], *, fallback_actor: str | None = None) -> dict[str, Any]:
    data = record.get("data") if isinstance(record.get("data"), Mapping) else {}
    normalized = {
        "id": str(record_id),
        "resource": resource,
        "status": str(record.get("status") or default_status(resource)),
        "enabled": bool(record.get("enabled", str(record.get("status") or default_status(resource)) not in {"disabled", "revoked", "retired", "locked"})),
        "created_at": str(record.get("created_at") or utc_now()),
        "updated_at": str(record.get("updated_at") or utc_now()),
        "actor": record.get("actor") or fallback_actor,
        "profile": record.get("profile"),
        "tenant": record.get("tenant"),
        "issuer": record.get("issuer"),
        "revision": int(record.get("revision") or 1),
        "data": copy.deepcopy(dict(data)),
    }
    return normalized


def _insert_record(conn: sqlite3.Connection, record: Mapping[str, Any]) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO records(
            resource, id, status, enabled, created_at, updated_at,
            actor, profile, tenant, issuer, revision, data_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["resource"],
            record["id"],
            record["status"],
            1 if bool(record.get("enabled", True)) else 0,
            record["created_at"],
            record["updated_at"],
            record.get("actor"),
            record.get("profile"),
            record.get("tenant"),
            record.get("issuer"),
            int(record.get("revision") or 1),
            json.dumps(record.get("data", {}), sort_keys=True),
        ),
    )


def _insert_transaction(conn: sqlite3.Connection, payload: Mapping[str, Any]) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO transaction_log(
            transaction_id, ts, command, resource, status, record_id,
            changed_ids_json, summary_json, actor, profile, tenant, issuer,
            before_checksum, after_checksum
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload.get("transaction_id"),
            payload.get("ts"),
            payload.get("command"),
            payload.get("resource"),
            payload.get("status"),
            payload.get("record_id"),
            json.dumps(list(payload.get("changed_ids") or []), sort_keys=True),
            json.dumps(dict(payload.get("summary") or {}), sort_keys=True),
            payload.get("actor"),
            payload.get("profile"),
            payload.get("tenant"),
            payload.get("issuer"),
            payload.get("before_checksum"),
            payload.get("after_checksum"),
        ),
    )


def _insert_audit(conn: sqlite3.Connection, payload: Mapping[str, Any]) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO audit_log(
            id, tenant_id, actor_user_id, actor_client_id, session_id,
            event_type, target_type, target_id, outcome, request_id,
            occurred_at, details_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload.get("id"),
            payload.get("tenant_id"),
            payload.get("actor_user_id"),
            payload.get("actor_client_id"),
            payload.get("session_id"),
            payload.get("event_type"),
            payload.get("target_type"),
            payload.get("target_id"),
            payload.get("outcome"),
            payload.get("request_id"),
            payload.get("occurred_at"),
            json.dumps(dict(payload.get("details") or {}), sort_keys=True),
        ),
    )


def _insert_activity(conn: sqlite3.Connection, payload: Mapping[str, Any]) -> None:
    conn.execute(
        "INSERT INTO activity_log(ts, kind, resource, record_id, status, transaction_id) VALUES (?, ?, ?, ?, ?, ?)",
        (
            payload.get("ts"),
            payload.get("kind"),
            payload.get("resource"),
            payload.get("id"),
            payload.get("status"),
            payload.get("transaction_id"),
        ),
    )


def _operator_root_from_path(path: Path) -> Path | None:
    if path.parent.name == "logs":
        return path.parent.parent
    if path.parent.name == "snapshots":
        return path.parent.parent
    return None


def _operator_table_for_log(path: Path) -> str | None:
    mapping = {
        "transactions.jsonl": "transaction_log",
        "audit-events.jsonl": "audit_log",
        "activity.jsonl": "activity_log",
    }
    return mapping.get(path.name)


def _fetch_log_rows(conn: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    if table == "transaction_log":
        rows = conn.execute(
            "SELECT transaction_id, ts, command, resource, status, record_id, changed_ids_json, summary_json, actor, profile, tenant, issuer, before_checksum, after_checksum FROM transaction_log ORDER BY ts, transaction_id"
        ).fetchall()
        return [
            {
                "transaction_id": row["transaction_id"],
                "ts": row["ts"],
                "command": row["command"],
                "resource": row["resource"],
                "status": row["status"],
                "record_id": row["record_id"],
                "changed_ids": json.loads(row["changed_ids_json"] or "[]"),
                "summary": json.loads(row["summary_json"] or "{}"),
                "actor": row["actor"],
                "profile": row["profile"],
                "tenant": row["tenant"],
                "issuer": row["issuer"],
                "before_checksum": row["before_checksum"],
                "after_checksum": row["after_checksum"],
            }
            for row in rows
        ]
    if table == "audit_log":
        rows = conn.execute(
            "SELECT id, tenant_id, actor_user_id, actor_client_id, session_id, event_type, target_type, target_id, outcome, request_id, occurred_at, details_json FROM audit_log ORDER BY occurred_at, id"
        ).fetchall()
        return [
            {
                "id": row["id"],
                "tenant_id": row["tenant_id"],
                "actor_user_id": row["actor_user_id"],
                "actor_client_id": row["actor_client_id"],
                "session_id": row["session_id"],
                "event_type": row["event_type"],
                "target_type": row["target_type"],
                "target_id": row["target_id"],
                "outcome": row["outcome"],
                "request_id": row["request_id"],
                "occurred_at": row["occurred_at"],
                "details": json.loads(row["details_json"] or "{}"),
            }
            for row in rows
        ]
    rows = conn.execute("SELECT seq, ts, kind, resource, record_id, status, transaction_id FROM activity_log ORDER BY seq").fetchall()
    return [
        {
            "seq": int(row["seq"]),
            "ts": row["ts"],
            "kind": row["kind"],
            "resource": row["resource"],
            "id": row["record_id"],
            "status": row["status"],
            "transaction_id": row["transaction_id"],
        }
        for row in rows
    ]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    root = _operator_root_from_path(path)
    table = _operator_table_for_log(path)
    if root is not None and table is not None and (root / _OPERATOR_DB_FILENAME).exists():
        with _connect_state_root(root) as conn:
            return _fetch_log_rows(conn, table)
    return _jsonl_rows(path)


def append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    root = _operator_root_from_path(path)
    table = _operator_table_for_log(path)
    if root is not None and table is not None:
        with _connect_state_root(root) as conn:
            conn.execute("BEGIN IMMEDIATE")
            if table == "transaction_log":
                _insert_transaction(conn, payload)
            elif table == "audit_log":
                _insert_audit(conn, payload)
            else:
                _insert_activity(conn, payload)
            conn.commit()
        _append_jsonl_file(path, payload)
        return
    _append_jsonl_file(path, payload)


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
