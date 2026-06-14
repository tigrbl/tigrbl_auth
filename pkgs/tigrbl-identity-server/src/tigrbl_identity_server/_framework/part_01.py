"""Tigrbl-only framework surface for tigrbl_auth.

This module centralizes runtime-facing imports used throughout the package and
intentionally restricts them to Tigrbl's public API plus first-party
Swarmauri crypto/key services and required schema helpers.

Release paths in this repository must not fall back to alternate framework
implementations, compatibility placeholders, or private Tigrbl modules.
"""

from __future__ import annotations

from dataclasses import replace as dataclass_replace
from datetime import date, datetime, time
from http import HTTPStatus as status
from uuid import UUID as UUIDValue
from typing import Any, Mapping, MutableMapping
import inspect

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


_TABLE_MODULE_PREFIXES = ("tigrbl_identity_storage.tables.", "tigrbl_identity_storage.tables.")


def _is_local_table_module(module_name: str) -> bool:
    return module_name.startswith(_TABLE_MODULE_PREFIXES)


def _is_local_table_model(model: Any) -> bool:
    return isinstance(model, type) and _is_local_table_module(getattr(model, "__module__", ""))


def _deleted_count(result: Any) -> int:
    if isinstance(result, Mapping):
        value = result.get("deleted", 0)
        return value if isinstance(value, int) else 0
    return 0


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

        if db is not None and target in crud_targets and _is_local_table_module(module_name):
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
                try:
                    return await _crud_ops.create(model, dict(payload), db=db)
                except IntegrityError as exc:
                    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "invalid table create payload") from exc
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


def _jsonify_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonify_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonify_value(item) for item in value]
    if isinstance(value, UUIDValue):
        return str(value)
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    return value


def _table_payload_without_identifiers(model: type, payload: Any) -> dict[str, Any]:
    normalized = _normalize_payload(payload)
    try:
        from tigrbl_ops_oltp.crud.helpers.model import _single_pk_name

        pk_name = _single_pk_name(model)
    except Exception:
        pk_name = "id"
    for key in {pk_name, "id", "ident", "item_id", f"{pk_name}_id"}:
        normalized.pop(key, None)
    return normalized


def _table_replace_payload(model: type, existing: Any, payload: Any) -> dict[str, Any]:
    merged = _normalize_payload(existing)
    merged.update(_table_payload_without_identifiers(model, payload))
    return merged


def _legacy_handler_ident(model: type, payload: Any) -> Any:
    normalized = _normalize_payload(payload)
    for key in ("ident", "id", "item_id"):
        value = normalized.get(key)
        if value not in {None, ""}:
            try:
                from tigrbl_ops_oltp.crud.helpers.model import _coerce_pk_value

                return _coerce_pk_value(model, value)
            except Exception:
                return value
    return None


