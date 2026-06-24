"""Durable SQLite-backed operator-plane persistence helpers."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from tigrbl_identity_core.path_safety import safe_display_path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


OPERATOR_STORE_SCHEMA_VERSION = 1
PORTABILITY_SCHEMA_VERSION = 3
_OPERATOR_DB_FILENAME = "operator_plane.sqlite3"


def default_status(resource: str) -> str:
    if resource in {"keys"}:
        return "staged"
    return "active"


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
    state_home = _state_home()
    try:
        resolved_repo = repo_root.resolve()
        resolved_home = state_home.resolve()
        if resolved_home == resolved_repo or resolved_home.is_relative_to(resolved_repo):
            state_home = resolved_repo.parent / "operator-plane-state"
    except OSError:
        pass
    namespace = f"{repo_root.name or 'repo'}-{_hash_repo_root(repo_root)}"
    path = state_home / namespace
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


