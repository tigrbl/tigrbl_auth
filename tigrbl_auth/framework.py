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

from tigrbl import (
    APIKey,
    ColumnSpec,
    Depends,
    ForeignKeySpec,
    HTMLResponse,
    HTTPBearer,
    HTTPException,
    JSONResponse,
    RedirectResponse,
    Request,
    Response,
    TigrblApp,
    TigrblRouter,
    engine_ctx,
    hook_ctx,
    op_ctx,
)
from tigrbl.orm.tables._base import Base
from tigrbl.shortcuts.column import F, IO, S, acol
from tigrbl.config.constants import TIGRBL_AUTH_CONTEXT_ATTR
from tigrbl.core.crud.params import Header
from tigrbl.engine import HybridSession as AsyncSession, engine as build_engine
from tigrbl.security import Security
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
    "HTTPBearer",
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
