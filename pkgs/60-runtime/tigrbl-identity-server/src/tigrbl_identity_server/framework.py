"""Direct Tigrbl framework public surface."""

from __future__ import annotations

from http import HTTPStatus as status

from pydantic import AnyHttpUrl, ConfigDict, EmailStr, constr, field_validator
from swarmauri_core.crypto.types import ExportPolicy, JWAAlg, KeyUse
from swarmauri_core.key_providers.types import KeyAlg, KeyClass, KeySpec
from swarmauri_crypto_jwe import JweCrypto
from swarmauri_keyprovider_file import FileKeyProvider
from swarmauri_keyprovider_local import LocalKeyProvider
from swarmauri_signing_ed25519 import Ed25519EnvelopeSigner
from swarmauri_signing_jws import JwsSignerVerifier
from swarmauri_tokens_jwt import JWTTokenService
from tigrbl import (
    APIKey,
    ForeignKeySpec,
    HTTPBearer,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    RestOltpTable as Base,
    Response,
    TigrblApp,
    TigrblRouter,
    engine_ctx,
    hook_ctx,
    op_ctx,
)
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
from tigrbl.security import Depends, Security
from tigrbl.shortcuts.column import ColumnSpec, F, IO, S, acol
from tigrbl.types import (
    AuthNProvider,
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
    "APIKey",
    "ActiveToggle",
    "AnyHttpUrl",
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
    "HTTPBearer",
    "HTMLResponse",
    "HTTPException",
    "Header",
    "IO",
    "Integer",
    "JSON",
    "JSONResponse",
    "JWAAlg",
    "JWTTokenService",
    "JweCrypto",
    "JwsSignerVerifier",
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
    "engine_ctx",
    "field_validator",
    "hook_ctx",
    "op_ctx",
    "relationship",
    "status",
]
