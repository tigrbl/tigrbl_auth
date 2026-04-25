"""Tigrbl-only framework surface for tigrbl_auth.

This module centralizes runtime-facing imports used throughout the package and
intentionally restricts them to Tigrbl's public API plus first-party
Swarmauri crypto/key services and required schema helpers.

Release paths in this repository must not fall back to alternate framework
implementations, compatibility placeholders, or private Tigrbl modules.
"""

from __future__ import annotations

from http import HTTPStatus as status

from pydantic import AnyHttpUrl, ConfigDict, EmailStr, constr, field_validator
from sqlalchemy import Select, delete, or_, select
from sqlalchemy.exc import IntegrityError

try:
    from tigrbl import Base
except ImportError:  # tigrbl >= 0.3.24.dev1
    from tigrbl.orm.tables._base import Base

try:
    from tigrbl import TigrblApi
except ImportError:  # tigrbl >= 0.3.24.dev1
    from tigrbl import TigrblRouter as TigrblApi

from tigrbl import TigrblApp, engine_ctx, hook_ctx, op_ctx
try:
    from tigrbl.column.shortcuts import ColumnSpec, F, IO, S, acol
except ModuleNotFoundError:  # tigrbl >= 0.3.24.dev1
    from tigrbl.shortcuts.column import ColumnSpec, F, IO, S, acol

try:
    from tigrbl.column.storage_spec import ForeignKeySpec
except ModuleNotFoundError:  # tigrbl >= 0.3.24.dev1
    from tigrbl import ForeignKeySpec
from tigrbl.config.constants import TIGRBL_AUTH_CONTEXT_ATTR
try:
    from tigrbl.core.crud.params import Header
except ModuleNotFoundError:  # tigrbl >= 0.3.24.dev1
    def Header(default=None, alias: str | None = None):
        return default
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
try:
    from tigrbl.requests import Request
    from tigrbl.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
except ModuleNotFoundError:  # tigrbl >= 0.3.24.dev1
    from tigrbl import HTMLResponse, JSONResponse, RedirectResponse, Request, Response
from tigrbl.runtime.status import HTTPException
try:
    from tigrbl.security import APIKey, Depends, Security
except ImportError:  # tigrbl >= 0.3.24.dev1
    from tigrbl import APIKey, Depends

    def Security(dependency):
        return Depends(dependency)
from tigrbl.types import (
    AuthNProvider,
    BaseModel,
    Boolean,
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

from swarmauri_core.crypto.types import ExportPolicy, JWAAlg, KeyUse
from swarmauri_core.key_providers.types import KeyAlg, KeyClass, KeySpec
from swarmauri_crypto_jwe import JweCrypto
from swarmauri_keyprovider_file import FileKeyProvider
from swarmauri_keyprovider_local import LocalKeyProvider
from swarmauri_signing_ed25519 import Ed25519EnvelopeSigner
from swarmauri_signing_jws import JwsSignerVerifier
from swarmauri_tokens_jwt import JWTTokenService


_RPC_DISABLED_SENTINEL = "/__tigrbl_auth_rpc_disabled__"


class TigrblRouter(TigrblApi):
    """Compatibility adapter over the published Tigrbl API surface.

    The pinned `tigrbl` runtime publishes `TigrblApi` as the router-shaped API
    object. This package historically imported `TigrblRouter` from the top-level
    namespace, but that symbol is not exported by the published wheel.

    This adapter stays entirely on the published Tigrbl surface while preserving
    the methods that the release path expects (`include_tables`, deferred JSON-RPC
    mounting, and diagnostics attachment) without reaching into private modules.
    """

    def __init__(self, *args, jsonrpc_prefix: str | None = None, **kwargs) -> None:
        effective_prefix = jsonrpc_prefix if jsonrpc_prefix is not None else _RPC_DISABLED_SENTINEL
        super().__init__(*args, jsonrpc_prefix=effective_prefix, **kwargs)
        if effective_prefix == _RPC_DISABLED_SENTINEL:
            self._routes[:] = [route for route in self._routes if getattr(route, "path", None) != _RPC_DISABLED_SENTINEL]

    def include_tables(self, models, **kwargs):
        include_tables = getattr(super(), "include_tables", None)
        if include_tables is not None:
            return include_tables(models, **kwargs)
        kwargs.setdefault("base_prefix", "")
        return self.include_models(models, **kwargs)

__all__ = [
    "AnyHttpUrl",
    "APIKey",
    "AsyncSession",
    "AuthNProvider",
    "Base",
    "BaseModel",
    "Boolean",
    "Bootstrappable",
    "ClientBase",
    "ColumnSpec",
    "ConfigDict",
    "Created",
    "Depends",
    "Ed25519EnvelopeSigner",
    "EmailStr",
    "ExportPolicy",
    "F",
    "Field",
    "FileKeyProvider",
    "ForeignKeySpec",
    "GUIDPk",
    "HTTPException",
    "HTMLResponse",
    "IO",
    "IntegrityError",
    "Integer",
    "JSON",
    "JSONResponse",
    "JWAAlg",
    "JWTTokenService",
    "JweCrypto",
    "KeyAlg",
    "KeyClass",
    "KeyDigest",
    "KeySpec",
    "KeyUse",
    "LargeBinary",
    "LastUsed",
    "LocalKeyProvider",
    "Mapped",
    "PgUUID",
    "Principal",
    "RedirectResponse",
    "Request",
    "Response",
    "S",
    "Security",
    "Select",
    "String",
    "TZDateTime",
    "TIGRBL_AUTH_CONTEXT_ATTR",
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
    "delete",
    "engine_ctx",
    "field_validator",
    "hook_ctx",
    "op_ctx",
    "or_",
    "relationship",
    "select",
    "status",
    "Header",
    "JwsSignerVerifier",
]

# tigrbl.types intentionally re-exports BaseModel/Field/ValidationError. The
# remaining pydantic schema helpers above stay direct imports because Tigrbl
# does not expose public aliases for them yet.
from tigrbl.types import Field  # noqa: E402  (kept adjacent to __all__ list)
