from __future__ import annotations

from uuid import uuid4

from tigrbl_identity_contracts.admin_resources import (
    AdminResource,
    AdminResourceKind,
    AdminResourceStatus,
    _clean_tuple,
)
from tigrbl_identity_contracts.applications import App
from tigrbl_identity_core import utc_now_iso as _utc_now


class AdminControlPlaneError(RuntimeError):
    pass


def _new_id(prefix: str) -> str:
    return f"{prefix}:{uuid4().hex}"


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
