from __future__ import annotations

from tigrbl_identity_contracts.admin_resources import (
    AdminResource,
    AdminResourceKind,
    AdminResourceRecord,
    AdminResourceStatus,
    _clean_tuple,
)
from tigrbl_identity_contracts.applications import App
from tigrbl_identity_core.clock import utc_now_iso as _utc_now
from tigrbl_identity_core.primitives import new_prefixed_id as _new_id


class AdminControlPlaneError(RuntimeError):
    pass


__all__ = [
    "AdminControlPlaneError",
    "AdminResource",
    "AdminResourceKind",
    "AdminResourceRecord",
    "AdminResourceStatus",
    "App",
    "_clean_tuple",
    "_new_id",
    "_utc_now",
]
