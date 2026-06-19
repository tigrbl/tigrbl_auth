from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Mapping, Protocol


class StorageDialect(str, Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class StorageStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class StorageError(RuntimeError):
    pass


class StorageConflictError(StorageError):
    pass


class StorageNotFoundError(StorageError):
    pass


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class StorageRecord:
    collection: str
    id: str
    tenant_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    version: int = 1
    status: StorageStatus = StorageStatus.ACTIVE
    created_at: str = field(default_factory=_utc_now)
    updated_at: str = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.collection or not self.id or not self.tenant_id:
            raise ValueError("storage record requires collection, id, and tenant_id")
        if self.version <= 0:
            raise ValueError("storage record version must be positive")
        object.__setattr__(self, "status", StorageStatus(self.status))
        object.__setattr__(self, "payload", dict(self.payload))


class RepositoryPort(Protocol):
    def create(self, record: StorageRecord) -> StorageRecord: ...

    def get(self, collection: str, record_id: str, *, tenant_id: str) -> StorageRecord: ...

    def update(
        self,
        collection: str,
        record_id: str,
        *,
        tenant_id: str,
        payload: Mapping[str, Any],
        expected_version: int | None = None,
    ) -> StorageRecord: ...

    def delete(self, collection: str, record_id: str, *, tenant_id: str) -> StorageRecord: ...

    def list(self, collection: str, *, tenant_id: str) -> tuple[StorageRecord, ...]: ...


class InMemoryRepository:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], StorageRecord] = {}

    @property
    def records(self) -> Mapping[tuple[str, str], StorageRecord]:
        return dict(self._records)

    def create(self, record: StorageRecord) -> StorageRecord:
        key = (record.collection, record.id)
        if key in self._records and self._records[key].status != StorageStatus.DELETED:
            raise StorageConflictError("storage record already exists")
        self._records[key] = record
        return record

    def get(self, collection: str, record_id: str, *, tenant_id: str) -> StorageRecord:
        record = self._records.get((collection, record_id))
        if record is None or record.status == StorageStatus.DELETED:
            raise StorageNotFoundError("storage record not found")
        if record.tenant_id != tenant_id:
            raise StorageNotFoundError("storage record not found")
        return record

    def update(
        self,
        collection: str,
        record_id: str,
        *,
        tenant_id: str,
        payload: Mapping[str, Any],
        expected_version: int | None = None,
    ) -> StorageRecord:
        record = self.get(collection, record_id, tenant_id=tenant_id)
        if expected_version is not None and record.version != expected_version:
            raise StorageConflictError("storage record version conflict")
        updated = replace(
            record,
            payload=dict(payload),
            version=record.version + 1,
            updated_at=_utc_now(),
        )
        self._records[(collection, record_id)] = updated
        return updated

    def delete(self, collection: str, record_id: str, *, tenant_id: str) -> StorageRecord:
        record = self.get(collection, record_id, tenant_id=tenant_id)
        deleted = replace(record, status=StorageStatus.DELETED, version=record.version + 1, updated_at=_utc_now())
        self._records[(collection, record_id)] = deleted
        return deleted

    def list(self, collection: str, *, tenant_id: str) -> tuple[StorageRecord, ...]:
        return tuple(
            sorted(
                (
                    record
                    for record in self._records.values()
                    if record.collection == collection
                    and record.tenant_id == tenant_id
                    and record.status != StorageStatus.DELETED
                ),
                key=lambda record: record.id,
            )
        )


class SqlAlchemyRepositoryAdapter:
    """Duck-typed SQLAlchemy repository adapter.

    The adapter intentionally depends on a session-like object and a model
    factory instead of importing SQLAlchemy at module import time. That keeps the
    public storage package importable in minimal environments while preserving a
    concrete adapter contract for SQLAlchemy/Tigrbl table integrations.
    """

    def __init__(self, session: Any, model_factory: Any) -> None:
        self.session = session
        self.model_factory = model_factory

    def create(self, record: StorageRecord) -> StorageRecord:
        row = self.model_factory.from_storage_record(record)
        self.session.add(row)
        self.session.commit()
        return self.model_factory.to_storage_record(row)

    def get(self, collection: str, record_id: str, *, tenant_id: str) -> StorageRecord:
        row = self.session.get(self.model_factory, (collection, record_id))
        if row is None:
            raise StorageNotFoundError("storage record not found")
        record = self.model_factory.to_storage_record(row)
        if record.tenant_id != tenant_id or record.status == StorageStatus.DELETED:
            raise StorageNotFoundError("storage record not found")
        return record

    def update(
        self,
        collection: str,
        record_id: str,
        *,
        tenant_id: str,
        payload: Mapping[str, Any],
        expected_version: int | None = None,
    ) -> StorageRecord:
        record = self.get(collection, record_id, tenant_id=tenant_id)
        if expected_version is not None and record.version != expected_version:
            raise StorageConflictError("storage record version conflict")
        updated = replace(record, payload=dict(payload), version=record.version + 1, updated_at=_utc_now())
        row = self.model_factory.from_storage_record(updated)
        self.session.merge(row)
        self.session.commit()
        return updated

    def delete(self, collection: str, record_id: str, *, tenant_id: str) -> StorageRecord:
        record = self.get(collection, record_id, tenant_id=tenant_id)
        deleted = replace(record, status=StorageStatus.DELETED, version=record.version + 1, updated_at=_utc_now())
        row = self.model_factory.from_storage_record(deleted)
        self.session.merge(row)
        self.session.commit()
        return deleted

    def list(self, collection: str, *, tenant_id: str) -> tuple[StorageRecord, ...]:
        rows = self.session.list(self.model_factory, collection=collection, tenant_id=tenant_id)
        records = [self.model_factory.to_storage_record(row) for row in rows]
        return tuple(sorted((record for record in records if record.status != StorageStatus.DELETED), key=lambda item: item.id))


@dataclass(frozen=True, slots=True)
class StorageMatrixEntry:
    dialect: StorageDialect
    dsn_prefixes: tuple[str, ...]
    supports_transactions: bool
    supports_json: bool
    supports_schema_namespace: bool


STORAGE_MATRIX: tuple[StorageMatrixEntry, ...] = (
    StorageMatrixEntry(
        dialect=StorageDialect.SQLITE,
        dsn_prefixes=("sqlite://", "sqlite+aiosqlite://"),
        supports_transactions=True,
        supports_json=True,
        supports_schema_namespace=False,
    ),
    StorageMatrixEntry(
        dialect=StorageDialect.POSTGRESQL,
        dsn_prefixes=("postgresql://", "postgresql+psycopg://", "postgresql+asyncpg://"),
        supports_transactions=True,
        supports_json=True,
        supports_schema_namespace=True,
    ),
)


def dialect_for_dsn(dsn: str) -> StorageDialect:
    for entry in STORAGE_MATRIX:
        if any(dsn.startswith(prefix) for prefix in entry.dsn_prefixes):
            return entry.dialect
    raise ValueError("unsupported storage DSN dialect")


def matrix_entry_for_dialect(dialect: StorageDialect | str) -> StorageMatrixEntry:
    normalized = StorageDialect(dialect)
    for entry in STORAGE_MATRIX:
        if entry.dialect == normalized:
            return entry
    raise ValueError("unsupported storage dialect")


def assert_repository_port(repository: RepositoryPort) -> RepositoryPort:
    required = ("create", "get", "update", "delete", "list")
    missing = [name for name in required if not callable(getattr(repository, name, None))]
    if missing:
        raise TypeError(f"repository is missing required operations: {', '.join(missing)}")
    return repository


__all__ = [
    "InMemoryRepository",
    "RepositoryPort",
    "STORAGE_MATRIX",
    "SqlAlchemyRepositoryAdapter",
    "StorageConflictError",
    "StorageDialect",
    "StorageError",
    "StorageMatrixEntry",
    "StorageNotFoundError",
    "StorageRecord",
    "StorageStatus",
    "assert_repository_port",
    "dialect_for_dsn",
    "matrix_entry_for_dialect",
]
