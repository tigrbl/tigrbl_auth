"""Legacy import facade for canonical database engine wiring.

The authoritative implementation lives in ``tigrbl_auth.tables.engine``.
"""

from tigrbl_auth.tables.engine import ENGINE, dsn, get_db

__all__ = ["ENGINE", "dsn", "get_db"]
