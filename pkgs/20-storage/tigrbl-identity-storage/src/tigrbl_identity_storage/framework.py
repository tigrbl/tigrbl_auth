"""Storage-owned direct Tigrbl framework surface."""

from __future__ import annotations

from http import HTTPStatus as status

from pydantic import EmailStr, constr
from swarmauri_core.crypto.types import JWAAlg
from tigrbl import ForeignKeySpec, HTMLResponse, JSONResponse, RedirectResponse, Response, RestOltpTable as Base
from tigrbl import TigrblApp, TigrblRouter, hook_ctx
from tigrbl.config.constants import TIGRBL_AUTH_CONTEXT_ATTR
from tigrbl.core.crud.params import Header
from tigrbl.engine import HybridSession as AsyncSession, engine as build_engine
from tigrbl.orm.mixins import (
    ActiveToggle,
    Bootstrappable,
    Created,
    GUIDPk,
    KeyDigest,
    LastUsed,
    Principal,
    TenantBound,
    TenantColumn,
    Timestamped,
    UserColumn,
    ValidityWindow,
)
from tigrbl.orm.tables import Client as ClientBase
from tigrbl.orm.tables import Tenant as TenantBase
from tigrbl.orm.tables import User as UserBase
from tigrbl.requests import Request
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
from tigrbl.shortcuts.column import ColumnSpec, F, IO, S, acol
from tigrbl.types import (
    BaseModel,
    Boolean,
    Field,
    Integer,
    JSON,
    LargeBinary,
    Mapped,
    PgUUID,
    String,
    TZDateTime,
    UUID,
    ValidationError,
    relationship,
)

__all__ = [
    "ActiveToggle",
    "AsyncSession",
    "Base",
    "BaseModel",
    "Boolean",
    "Bootstrappable",
    "ClientBase",
    "ColumnSpec",
    "Created",
    "Depends",
    "EmailStr",
    "F",
    "Field",
    "ForeignKeySpec",
    "GUIDPk",
    "HTMLResponse",
    "HTTPException",
    "Header",
    "IO",
    "Integer",
    "JSON",
    "JSONResponse",
    "JWAAlg",
    "KeyDigest",
    "LargeBinary",
    "LastUsed",
    "Mapped",
    "PgUUID",
    "Principal",
    "RedirectResponse",
    "Request",
    "Response",
    "S",
    "String",
    "TIGRBL_AUTH_CONTEXT_ATTR",
    "TZDateTime",
    "TenantBase",
    "TenantBound",
    "TenantColumn",
    "TigrblApp",
    "TigrblRouter",
    "Timestamped",
    "UUID",
    "UserBase",
    "UserColumn",
    "ValidationError",
    "ValidityWindow",
    "acol",
    "build_engine",
    "constr",
    "hook_ctx",
    "relationship",
    "status",
]
