"""Compatibility export for layer-30 database engine ownership."""

from tigrbl_identity_storage_runtime.engine import (
    ENGINE,
    bootstrap_runtime_engine,
    dsn,
    get_db,
)

__all__ = ["ENGINE", "bootstrap_runtime_engine", "dsn", "get_db"]
