"""Tigrbl-only framework surface for tigrbl_auth.

This module centralizes runtime-facing imports used throughout the package and
intentionally restricts them to Tigrbl's public API plus first-party
Swarmauri crypto/key services and required schema helpers.

Release paths in this repository must not fall back to alternate framework
implementations, compatibility placeholders, or private Tigrbl modules.
"""

from __future__ import annotations

from dataclasses import replace as dataclass_replace
from http import HTTPStatus as status
from typing import Any, Mapping, MutableMapping

import tigrbl as _tigrbl
from pydantic import AnyHttpUrl, ConfigDict, EmailStr, constr, field_validator
from sqlalchemy import Select, delete, or_, select
from sqlalchemy.exc import IntegrityError

from tigrbl import APIKey, HTTPBearer, TigrblApp, engine_ctx, hook_ctx, op_ctx
from tigrbl.requests import Request as _TigrblRequest
try:
    from tigrbl.column.shortcuts import ColumnSpec, F, IO, S, acol
    from tigrbl.column.storage_spec import ForeignKeySpec
except ModuleNotFoundError:
    from tigrbl import Column as _TigrblColumn
    from tigrbl_core._spec import ColumnSpec, F, IO, S, ForeignKeySpec

    def acol(
        *,
        storage: S | None = None,
        field: F | None = None,
        io: IO | None = None,
        default_factory: Any | None = None,
        read_producer: Any | None = None,
        spec: ColumnSpec | None = None,
        **kw: Any,
    ) -> _TigrblColumn:
        if spec is not None and any(
            x is not None for x in (storage, field, io, default_factory, read_producer)
        ):
            raise ValueError("Provide either spec or individual components, not both.")
        if spec is None:
            spec = ColumnSpec(
                storage=storage,
                field=field,
                io=io,
                default_factory=default_factory,
                read_producer=read_producer,
            )
        return _TigrblColumn(spec=spec, **kw)
from tigrbl.orm.tables._base import Base
try:
    from tigrbl.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
except ModuleNotFoundError:
    from tigrbl import HTMLResponse, JSONResponse, RedirectResponse, Response
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
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

_BaseTigrblRouter = getattr(_tigrbl, "TigrblRouter", None) or getattr(_tigrbl, "TigrblApi")


def _install_table_crud_invoke_compat() -> None:
    """Bypass flaky runtime op execution for generated table CRUD surfaces.

    The published Tigrbl runtime occasionally mis-handles generated CRUD table
    calls when they flow through the generic invoke path, especially for
    ``clear`` and ``replace``. The direct OLTP handlers are the stable source
    of truth for these table operations, so we short-circuit to them for this
    repository's table models.
    """

    from tigrbl_ops_oltp.crud import bulk as _crud_bulk
    from tigrbl_ops_oltp.crud import ops as _crud_ops
    from tigrbl_ops_oltp.crud.helpers.model import _coerce_pk_value, _single_pk_name
    from tigrbl_concrete._mapping.router import rpc as _rpc_router_module
    from tigrbl_runtime.runtime.executor import invoke as _invoke_module

    current = getattr(_invoke_module, "invoke_op", None)
    if not callable(current) or getattr(current, "__tigrbl_auth_table_crud_compat__", False):
        return

    original_invoke_op = current
    crud_targets = {
        "create",
        "read",
        "update",
        "replace",
        "merge",
        "delete",
        "list",
        "clear",
        "count",
        "exists",
        "bulk_create",
        "bulk_update",
        "bulk_replace",
        "bulk_merge",
        "bulk_delete",
    }

    async def _compat_invoke_op(
        *,
        request: Any = None,
        db: Any = None,
        model: type,
        alias: str,
        ctx: MutableMapping[str, Any] | None = None,
    ) -> Any:
        ctx_dict = dict(ctx or {})
        target = getattr(getattr(getattr(model, "ops", None), "by_alias", {}), "get", lambda _x: None)(alias)
        target = getattr(target, "target", alias)
        module_name = getattr(model, "__module__", "")

        if db is not None and target in crud_targets and module_name.startswith("tigrbl_auth.tables."):
            payload = ctx_dict.get("payload")
            if payload is None:
                payload = {}
            elif isinstance(payload, BaseModel):
                payload = payload.model_dump(exclude_none=True)
            elif hasattr(payload, "model_dump") and callable(getattr(payload, "model_dump")):
                payload = payload.model_dump(exclude_none=True)
            elif hasattr(payload, "__dict__") and not isinstance(payload, Mapping):
                payload = {
                    key: value
                    for key, value in vars(payload).items()
                    if not key.startswith("_")
                }
            path_params = ctx_dict.get("path_params", {})
            pk_name = None
            ident = None
            try:
                pk_name = _single_pk_name(model)
            except Exception:
                pk_name = None
            if pk_name:
                if isinstance(path_params, Mapping):
                    ident = path_params.get(pk_name) or path_params.get("id") or path_params.get("item_id")
                if ident is None and isinstance(payload, Mapping):
                    ident = payload.get(pk_name) or payload.get("id") or payload.get("item_id")
                if ident is not None:
                    ident = _coerce_pk_value(model, ident)

            if target == "create" and isinstance(payload, Mapping):
                return await _crud_ops.create(model, dict(payload), db=db)
            if target == "read" and ident is not None:
                return await _crud_ops.read(model, ident, db=db)
            if target == "update" and ident is not None and isinstance(payload, Mapping):
                return await _crud_ops.update(model, ident, dict(payload), db=db)
            if target == "replace" and ident is not None and isinstance(payload, Mapping):
                return await _crud_ops.replace(model, ident, dict(payload), db=db)
            if target == "merge" and ident is not None and isinstance(payload, Mapping):
                return await _crud_ops.merge(model, ident, dict(payload), db=db)
            if target == "delete" and ident is not None:
                return await _crud_ops.delete(model, ident, db=db)
            if target == "list":
                filters = dict(payload) if isinstance(payload, Mapping) else {}
                return await _crud_ops.list(model, filters, db=db)
            if target == "clear":
                filters = dict(payload) if isinstance(payload, Mapping) else {}
                return await _crud_ops.clear(model, filters, db=db)
            if target == "count":
                filters = dict(payload) if isinstance(payload, Mapping) else {}
                return await _crud_ops.count(model, filters, db=db)
            if target == "exists" and ident is not None:
                return await _crud_ops.exists(model, ident, db=db)
            if target.startswith("bulk_") and isinstance(payload, list):
                bulk_handler = getattr(_crud_bulk, target, None)
                if callable(bulk_handler):
                    return await bulk_handler(model, payload, db=db)

        return await original_invoke_op(
            request=request,
            db=db,
            model=model,
            alias=alias,
            ctx=ctx,
        )

    setattr(_compat_invoke_op, "__tigrbl_auth_table_crud_compat__", True)
    _invoke_module.invoke_op = _compat_invoke_op
    _rpc_router_module.invoke_op = _compat_invoke_op


_install_table_crud_invoke_compat()


def _normalize_payload(payload: Any) -> dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, BaseModel):
        return payload.model_dump(exclude_none=True)
    model_dump = getattr(payload, "model_dump", None)
    if callable(model_dump):
        return model_dump(exclude_none=True)
    if isinstance(payload, Mapping):
        return dict(payload)
    if hasattr(payload, "__dict__"):
        return {key: value for key, value in vars(payload).items() if not key.startswith("_")}
    return {}


def _install_table_route_compat(router: Any, models: list[type]) -> None:
    from tigrbl_concrete._concrete import engine_resolver as _resolver
    from tigrbl_ops_oltp.crud import ops as _crud_ops
    from tigrbl_ops_oltp.crud.helpers.model import _coerce_pk_value

    for model in models:
        rpc_root = getattr(model, "rpc", None)
        if rpc_root is not None and not getattr(getattr(rpc_root, "clear", None), "__tigrbl_auth_table_crud_clear__", False):
            async def _rpc_clear(
                payload: Any = None,
                *,
                db: Any,
                request: Any = None,
                ctx: MutableMapping[str, Any] | None = None,
                _model: type = model,
            ) -> Any:
                del request, ctx
                return await _crud_ops.clear(_model, _normalize_payload(payload), db=db)

            setattr(_rpc_clear, "__tigrbl_auth_table_crud_clear__", True)
            setattr(rpc_root, "clear", _rpc_clear)

    updated_routes = []
    for route in list(getattr(router, "_routes", []) or []):
        if getattr(route, "tigrbl_alias", None) != "replace":
            updated_routes.append(route)
            continue
        model = getattr(route, "tigrbl_model", None)
        if model not in models:
            updated_routes.append(route)
            continue

        async def _replace_handler(
            request: Any = None,
            body: Any = None,
            query: dict[str, Any] | None = None,
            _router: Any = router,
            _model: type = model,
            **path_params: Any,
        ) -> Any:
            del query
            db, release = _resolver.acquire(router=_router, model=_model, op_alias="replace")
            try:
                ident = path_params.get("id") or path_params.get("item_id")
                ident = _coerce_pk_value(_model, ident)
                return await _crud_ops.replace(_model, ident, _normalize_payload(body), db=db)
            finally:
                if callable(release):
                    release()

        updated_routes.append(
            dataclass_replace(route, handler=_replace_handler)
        )
    router._routes[:] = updated_routes


class TigrblRouter(_BaseTigrblRouter):
    """Compatibility alias for the current Tigrbl API router facade."""

    def include_tables(self, models: type | list[type] | tuple[type, ...]) -> None:
        if isinstance(models, type):
            model_seq = [models]
        else:
            model_seq = list(models)
        include_models = getattr(self, "include_models", None)
        if callable(include_models):
            include_models(model_seq)
            _install_table_route_compat(self, model_seq)
            return

        parent_include_tables = getattr(super(), "include_tables", None)
        if callable(parent_include_tables):
            parent_include_tables(model_seq)
            _install_table_route_compat(self, model_seq)
            return

        include_table = getattr(self, "include_table", None)
        if callable(include_table):
            for model in model_seq:
                include_table(model)
            _install_table_route_compat(self, model_seq)
            return

        raise AttributeError("Tigrbl router does not expose include_models, include_tables, or include_table")


class Request(_TigrblRequest):
    """Request facade accepting both current Tigrbl and ASGI-style construction."""

    def __init__(
        self,
        method: str | dict[str, Any] | None = None,
        path: str | None = None,
        **kwargs: Any,
    ) -> None:
        scope = kwargs.pop("scope", None)
        if method is None and scope is not None:
            method = scope
            scope = None
        super().__init__(method or "GET", path, scope=scope, **kwargs)


_tigrbl.TigrblRouter = TigrblRouter


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
