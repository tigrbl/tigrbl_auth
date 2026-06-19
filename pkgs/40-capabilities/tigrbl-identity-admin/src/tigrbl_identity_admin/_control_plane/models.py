from __future__ import annotations

from uuid import uuid4

from tigrbl_management_plane_contracts.admin_resources import (
    AdminAuditEvent,
    AdminResource,
    AdminResourceKind,
    AdminResourceStatus,
    AdminUiState,
    AdminUiView,
    AppRecord,
    CredentialRecord,
    PolicyRecord,
    PrincipalRecord,
    ResourceServerRecord,
    ServiceIdentityRecord,
    _clean_tuple,
    _utc_now,
)


class AdminControlPlaneError(RuntimeError):
    pass


def _new_id(prefix: str) -> str:
    return f"{prefix}:{uuid4().hex}"


__all__ = [
    "AdminAuditEvent",
    "AdminControlPlaneError",
    "AdminResource",
    "AdminResourceKind",
    "AdminResourceStatus",
    "AdminUiState",
    "AdminUiView",
    "AppRecord",
    "CredentialRecord",
    "PolicyRecord",
    "PrincipalRecord",
    "ResourceServerRecord",
    "ServiceIdentityRecord",
    "_clean_tuple",
    "_new_id",
    "_utc_now",
]
