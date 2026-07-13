from __future__ import annotations

from tigrbl_identity_contracts.admin_resources import (
    AdminResource,
    AdminResourceKind,
    AdminResourceStatus,
    _clean_tuple,
)
from tigrbl_identity_contracts.applications import App
from tigrbl_capability import new_prefixed_id as _new_id
from tigrbl_capability import utc_now_iso as _utc_now


class AdminControlPlaneError(RuntimeError):
    pass


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
