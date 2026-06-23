"""Storage adapters and Tigrbl/SQLAlchemy tables for the Tigrbl identity package suite."""

from __future__ import annotations

from .migrations.contract import (
    MigrationContract,
    MigrationRevision,
    build_migration_contract,
    collect_migration_revisions,
)


def ensure_identity_storage_importable() -> None:
    """Compatibility hook for callers that previously used facade path setup."""

    return None


__all__ = [
    "ensure_identity_storage_importable",
    "MigrationContract",
    "MigrationRevision",
    "build_migration_contract",
    "collect_migration_revisions",
]
