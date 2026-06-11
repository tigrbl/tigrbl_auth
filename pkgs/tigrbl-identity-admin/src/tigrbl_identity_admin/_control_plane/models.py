from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Mapping
from uuid import uuid4


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


class AdminControlPlaneError(RuntimeError):
    pass


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}:{uuid4().hex}"


def _clean_tuple(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value).strip() for value in values if str(value).strip()}))


@dataclass(frozen=True, slots=True)
class AdminResource:
    id: str
    kind: AdminResourceKind
    tenant_id: str
    name: str
    status: AdminResourceStatus = AdminResourceStatus.ACTIVE
    attributes: Mapping[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now)
    updated_at: str = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.id or not self.tenant_id or not self.name:
            raise ValueError("admin resource requires id, tenant_id, and name")
        object.__setattr__(self, "kind", AdminResourceKind(self.kind))
        object.__setattr__(self, "status", AdminResourceStatus(self.status))
        object.__setattr__(self, "attributes", dict(self.attributes))


@dataclass(frozen=True, slots=True)
class PrincipalRecord(AdminResource):
    subject: str = ""
    principal_kind: str = "user"
    roles: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        AdminResource.__post_init__(self)
        if not self.subject:
            raise ValueError("principal subject is required")
        object.__setattr__(self, "roles", _clean_tuple(self.roles))


@dataclass(frozen=True, slots=True)
class CredentialRecord(AdminResource):
    principal_id: str = ""
    credential_kind: str = "password"
    rotated_from: str | None = None

    def __post_init__(self) -> None:
        AdminResource.__post_init__(self)
        if not self.principal_id:
            raise ValueError("credential principal_id is required")


@dataclass(frozen=True, slots=True)
class AppRecord(AdminResource):
    client_ids: tuple[str, ...] = ()
    owner_principal_id: str | None = None

    def __post_init__(self) -> None:
        AdminResource.__post_init__(self)
        object.__setattr__(self, "client_ids", _clean_tuple(self.client_ids))


@dataclass(frozen=True, slots=True)
class ServiceIdentityRecord(AdminResource):
    scopes: tuple[str, ...] = ()
    owner_principal_id: str | None = None

    def __post_init__(self) -> None:
        AdminResource.__post_init__(self)
        object.__setattr__(self, "scopes", _clean_tuple(self.scopes))


@dataclass(frozen=True, slots=True)
class ResourceServerRecord(AdminResource):
    audience: str = ""
    scopes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        AdminResource.__post_init__(self)
        if not self.audience:
            raise ValueError("resource server audience is required")
        object.__setattr__(self, "scopes", _clean_tuple(self.scopes))


@dataclass(frozen=True, slots=True)
class PolicyRecord(AdminResource):
    policy_kind: str = "rbac"
    version: int = 1
    rules: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        AdminResource.__post_init__(self)
        if self.version <= 0:
            raise ValueError("policy version must be positive")
        object.__setattr__(self, "rules", dict(self.rules))


@dataclass(frozen=True, slots=True)
class AdminAuditEvent:
    event_id: str
    actor: str
    action: str
    resource_kind: AdminResourceKind
    resource_id: str
    tenant_id: str
    outcome: str
    recorded_at: str = field(default_factory=_utc_now)


@dataclass(frozen=True, slots=True)
class AdminUiView:
    state: AdminUiState
    resource_kind: AdminResourceKind
    rows: tuple[AdminResource, ...] = ()
    error: str | None = None

    @property
    def is_empty(self) -> bool:
        return self.state == AdminUiState.EMPTY
