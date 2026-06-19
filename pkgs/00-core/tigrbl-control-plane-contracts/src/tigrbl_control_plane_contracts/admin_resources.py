from __future__ import annotations

from enum import Enum


class AdminResourceKind(str, Enum):
    PRINCIPAL = "principal"
    CREDENTIAL = "credential"
    APP = "app"
    SERVICE_IDENTITY = "service_identity"
    RESOURCE_SERVER = "resource_server"
    POLICY = "policy"


class AdminResourceStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"


class AdminUiState(str, Enum):
    LOADING = "loading"
    EMPTY = "empty"
    READY = "ready"
    ERROR = "error"


__all__ = ["AdminResourceKind", "AdminResourceStatus", "AdminUiState"]
