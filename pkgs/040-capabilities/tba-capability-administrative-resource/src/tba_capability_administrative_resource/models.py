from __future__ import annotations

from tba_contracts_identity.admin_resources import (
    AdminResource,
    AdminResourceKind,
    AdminResourceRecord,
    AdminResourceStatus,
    _clean_tuple,
)
from tba_contracts_identity.applications import App
from tba_primitives_identity.clock import utc_now_iso as _utc_now
from tba_primitives_identity.primitives import new_prefixed_id as _new_id


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
