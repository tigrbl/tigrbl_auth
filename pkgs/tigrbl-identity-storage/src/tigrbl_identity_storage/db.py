"""Canonical database engine wiring for identity storage."""

from tigrbl_identity_storage.tables.engine import ENGINE, dsn, get_db

__all__ = ["ENGINE", "dsn", "get_db"]
