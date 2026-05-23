"""Storage adapters and Tigrbl/SQLAlchemy tables for the Tigrbl identity package suite."""

from __future__ import annotations

from .migration_contract import (
    MigrationContract,
    MigrationRevision,
    build_migration_contract,
    collect_migration_revisions,
)
from .repository import (
    InMemoryRepository,
    RepositoryPort,
    STORAGE_MATRIX,
    SqlAlchemyRepositoryAdapter,
    StorageConflictError,
    StorageDialect,
    StorageError,
    StorageMatrixEntry,
    StorageNotFoundError,
    StorageRecord,
    StorageStatus,
    assert_repository_port,
    dialect_for_dsn,
    matrix_entry_for_dialect,
)

__all__ = [
    "InMemoryRepository",
    "MigrationContract",
    "MigrationRevision",
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
    "build_migration_contract",
    "collect_migration_revisions",
    "dialect_for_dsn",
    "matrix_entry_for_dialect",
]
