"""Compatibility export for layer-30 database engine ownership."""

from tba_runtime_identity_storage.engine import (
    ENGINE,
    bootstrap_runtime_engine,
    dsn,
    get_db,
)

__all__ = ["ENGINE", "bootstrap_runtime_engine", "dsn", "get_db"]
