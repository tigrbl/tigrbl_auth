from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from tigrbl_identity_contracts.admin_resources import (
    AdminResource,
    AdminResourceKind,
    AdminResourceStatus,
    _clean_tuple,
)
from tigrbl_identity_contracts.applications import App
class AdminControlPlaneError(RuntimeError):
    pass


def _new_id(prefix: str) -> str:
    return f"{prefix}:{uuid4().hex}"


def _utc_now() -> str:
    """Return an aware UTC timestamp without importing primitive internals."""

    return datetime.now(timezone.utc).isoformat()


__all__ = [
    "AdminControlPlaneError",
    "AdminResource",
    "AdminResourceKind",
    "AdminResourceStatus",
    "App",
    "_clean_tuple",
    "_new_id",
    "_utc_now",
]
