"""Storage-owned Tigrbl framework surface.

This module keeps storage tables independent from server/runtime composition.
Only Tigrbl primitives and storage-local table compatibility helpers belong
here.
"""

from __future__ import annotations

from datetime import date, datetime, time
from http import HTTPStatus as status
import inspect
from typing import Any, Mapping
from uuid import UUID as UUIDValue

import tigrbl as _tigrbl
from pydantic import EmailStr, constr

from swarmauri_core.crypto.types import JWAAlg
from tigrbl import TigrblApp, hook_ctx
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
from tigrbl.orm.tables._base import Base
from tigrbl.requests import Request as _TigrblRequest
try:
    from tigrbl.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
except ModuleNotFoundError:  # pragma: no cover - older Tigrbl distributions
    from tigrbl import HTMLResponse, JSONResponse, RedirectResponse, Response
from tigrbl.runtime.status import HTTPException
from tigrbl.security import Depends
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

try:
    from tigrbl.column.shortcuts import ColumnSpec, F, IO, S, acol
    from tigrbl.column.storage_spec import ForeignKeySpec
except ModuleNotFoundError:  # pragma: no cover - older Tigrbl distributions
    from tigrbl import Column as _TigrblColumn
    from tigrbl_core._spec import ColumnSpec, F, ForeignKeySpec, IO, S

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


_BaseTigrblRouter = getattr(_tigrbl, "TigrblRouter", None) or getattr(_tigrbl, "TigrblApi")


class TigrblRouter(_BaseTigrblRouter):
    """Storage table router facade with local handler compatibility."""

    def include_tables(
        self,
        tables: list[type] | tuple[type, ...],
        *,
        base_prefix: str | None = None,
        mount_router: bool = True,
    ) -> Any:
        result = super().include_tables(
            tables,
            base_prefix=base_prefix,
            mount_router=mount_router,
        )
        for model in tables:
            _install_local_handler_dict_compat(model)
        return result

    def include_table(
        self,
        model: type,
        *,
        prefix: str | None = None,
        mount_router: bool = True,
    ) -> Any:
        result = super().include_table(
            model,
            prefix=prefix,
            mount_router=mount_router,
        )
        _install_local_handler_dict_compat(model)
        return result


class Request(_TigrblRequest):
    """Request facade accepting current Tigrbl and ASGI-style construction."""

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


def _is_local_table_module(module_name: str) -> bool:
    return module_name.startswith("tigrbl_identity_storage.tables.")


def _is_local_table_model(model: Any) -> bool:
    return isinstance(model, type) and _is_local_table_module(getattr(model, "__module__", ""))


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


def _legacy_handler_filters(payload: Any) -> Any:
    normalized = _normalize_payload(payload)
    filters = normalized.get("filters")
    if isinstance(filters, Mapping):
        return dict(filters)
    return normalized


def _install_local_handler_dict_compat(model: type) -> None:
    handlers_root = getattr(model, "handlers", None)
    if handlers_root is None:
        return

    for alias, handler_ns in vars(handlers_root).items():
        if handler_ns is None:
            continue
        raw = getattr(handler_ns, "core_raw", None) or getattr(handler_ns, "raw", None) or getattr(handler_ns, "core", None)
        if not callable(raw) or getattr(getattr(handler_ns, "core", None), "__tigrbl_auth_dict_style_compat__", False):
            continue

        def _raw_expects_envelope(callable_obj: Any) -> bool:
            try:
                params = list(inspect.signature(callable_obj).parameters.values())
            except (TypeError, ValueError):
                return False
            positional = [
                param
                for param in params
                if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            ]
            return len(positional) == 1 and not any(
                param.kind == inspect.Parameter.VAR_POSITIONAL for param in params
            )

        def _compat_envelope(alias_name: str, payload_obj: Any, db_obj: Any) -> dict[str, Any]:
            ident = _legacy_handler_ident(model, payload_obj)
            path_params: dict[str, Any] | None = None
            if alias_name == "create":
                next_payload: Any = _normalize_payload(payload_obj)
            elif alias_name in {"read", "delete", "exists"}:
                next_payload = {}
                if ident is not None:
                    path_params = {"id": ident}
            elif alias_name in {"update", "merge", "replace"}:
                next_payload = _table_payload_without_identifiers(model, payload_obj)
                if ident is not None:
                    path_params = {"id": ident}
            elif alias_name in {"list", "count", "clear"}:
                next_payload = _legacy_handler_filters(payload_obj)
            elif alias_name.startswith("bulk_"):
                next_payload = payload_obj or []
            else:
                next_payload = payload_obj
            envelope = {"payload": next_payload, "db": db_obj}
            if path_params is not None:
                envelope["path_params"] = path_params
            return envelope

        async def _compat_core(*args: Any, _alias: str = alias, _raw: Any = raw, **kwargs: Any) -> Any:
            if len(args) == 1 and isinstance(args[0], Mapping) and not kwargs:
                envelope = dict(args[0])
                payload = envelope.get("payload")
                db = envelope.get("db")
                path_params = envelope.get("path_params")
                if _alias in {"read", "delete", "exists", "update", "merge", "replace"} and isinstance(path_params, Mapping):
                    ident_from_path = path_params.get("id") or path_params.get("item_id")
                    if ident_from_path is not None:
                        if isinstance(payload, Mapping):
                            payload = {**dict(payload), "id": ident_from_path}
                        else:
                            payload = {"id": ident_from_path}

                compat_payload = payload
                if _alias == "replace":
                    ident = _legacy_handler_ident(model, payload)
                    read_handler = getattr(model.handlers, "read")
                    read_raw = getattr(read_handler, "core_raw", getattr(read_handler, "raw"))
                    existing = await read_raw(_compat_envelope("read", {"id": ident}, db))
                    compat_payload = _table_replace_payload(model, existing, payload)
                    compat_payload["ident"] = ident

                compat_envelope = _compat_envelope(_alias, compat_payload, db)

                if _raw_expects_envelope(_raw):
                    call = _raw(compat_envelope)
                else:
                    if _alias == "create":
                        direct_call = lambda: _raw(model, _normalize_payload(payload), db=db)
                    elif _alias in {"read", "delete", "exists"}:
                        direct_call = lambda: _raw(model, _legacy_handler_ident(model, payload), db=db)
                    elif _alias in {"update", "merge"}:
                        direct_call = lambda: _raw(model, _legacy_handler_ident(model, payload), _table_payload_without_identifiers(model, payload), db=db)
                    elif _alias == "replace":
                        direct_call = lambda: _raw(model, ident, _table_replace_payload(model, existing, payload), db=db)
                    elif _alias in {"list", "count", "clear"}:
                        direct_call = lambda: _raw(model, _legacy_handler_filters(payload), db=db)
                    elif _alias.startswith("bulk_"):
                        direct_call = lambda: _raw(model, payload or [], db=db)
                    else:
                        direct_call = lambda: _raw(*args, **kwargs)

                    try:
                        call = direct_call()
                    except TypeError:
                        call = _raw(compat_envelope)
            else:
                call = _raw(*args, **kwargs)
            if inspect.isawaitable(call):
                return await call
            return call

        setattr(_compat_core, "__tigrbl_auth_dict_style_compat__", True)
        setattr(handler_ns, "core", _compat_core)


_tigrbl.TigrblRouter = TigrblRouter


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
    "_install_local_handler_dict_compat",
    "acol",
    "build_engine",
    "constr",
    "hook_ctx",
    "relationship",
    "status",
]
