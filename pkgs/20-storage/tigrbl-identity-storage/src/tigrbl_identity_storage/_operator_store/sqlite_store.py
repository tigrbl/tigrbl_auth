from __future__ import annotations

from .paths import *
from .paths import (
    _OPERATOR_DB_FILENAME,
    _append_jsonl_file,
    _connect_state_root,
    _jsonl_rows,
    _upsert_metadata,
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


