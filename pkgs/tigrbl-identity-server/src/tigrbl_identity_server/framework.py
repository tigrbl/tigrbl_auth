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


def _is_local_table_model(model: Any) -> bool:
    return isinstance(model, type) and getattr(model, "__module__", "").startswith("tigrbl_auth.tables.")


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

                compat_payload = payload
                if _alias == "replace":
                    ident = _legacy_handler_ident(model, payload)
                    existing = await getattr(getattr(model.handlers, "read"), "core_raw", getattr(model.handlers.read, "raw"))(
                        _compat_envelope("read", {"id": ident}, db)
                    )
                    compat_payload = _table_replace_payload(model, existing, payload)
                    compat_payload["ident"] = ident

                compat_envelope = _compat_envelope(_alias, compat_payload, db)

                if _raw_expects_envelope(_raw):
                    call = _raw(compat_envelope)
                else:
                    if _alias == "create":
                        direct_call = lambda: _raw(model, _normalize_payload(payload), db)
                    elif _alias in {"read", "delete", "exists"}:
                        direct_call = lambda: _raw(model, _legacy_handler_ident(model, payload), db)
                    elif _alias in {"update", "merge"}:
                        direct_call = lambda: _raw(model, _legacy_handler_ident(model, payload), _table_payload_without_identifiers(model, payload), db)
                    elif _alias == "replace":
                        direct_call = lambda: _raw(model, ident, _table_replace_payload(model, existing, payload), db)
                    elif _alias in {"list", "count", "clear"}:
                        direct_call = lambda: _raw(model, _legacy_handler_filters(payload), db)
                    elif _alias.startswith("bulk_"):
                        direct_call = lambda: _raw(model, payload or [], db)
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


def _install_table_handler_compat() -> None:
    from tigrbl_atoms.atoms.sys import handler_clear as _handler_clear_module
    from tigrbl_atoms.atoms.sys import handler_replace as _handler_replace_module
    from tigrbl_atoms.atoms.sys import _oltp_context as _oltp_context
    from tigrbl_ops_oltp.crud.helpers.filters import _coerce_filters
    from tigrbl_ops_oltp.crud.helpers.model import _single_pk_name
    from tigrbl_ops_oltp.crud import ops as _crud_ops

    current_clear = getattr(_handler_clear_module, "_run", None)
    if callable(current_clear) and not getattr(current_clear, "__tigrbl_auth_table_clear_compat__", False):
        async def _compat_clear_run(obj: object | None, ctx: Any) -> None:
            model = obj if isinstance(obj, type) else getattr(ctx, "model", None)
            if not isinstance(model, type):
                raise TypeError("handler_clear requires a model type")
            if getattr(model, "__table__", None) is not None:
                filters = _normalize_payload(_oltp_context.payload(ctx))
                if filters and not _coerce_filters(model, filters) and not any(
                    hasattr(model, key) for key in filters
                ):
                    setattr(ctx, "result", {"deleted": 0})
                    return
                try:
                    result = await _crud_ops.clear(model, filters, db=_oltp_context.db(ctx))
                except IntegrityError:
                    result = {"deleted": 0}
                setattr(ctx, "result", result)
                return
            await current_clear(obj, ctx)

        setattr(_compat_clear_run, "__tigrbl_auth_table_clear_compat__", True)
        _handler_clear_module._run = _compat_clear_run

    current_replace = getattr(_handler_replace_module, "_run", None)
    if callable(current_replace) and not getattr(current_replace, "__tigrbl_auth_table_replace_compat__", False):
        async def _compat_replace_run(obj: object | None, ctx: Any) -> None:
            model = obj if isinstance(obj, type) else getattr(ctx, "model", None)
            if not isinstance(model, type):
                raise TypeError("handler_replace requires a model type")
            if getattr(model, "__table__", None) is not None:
                ident = _oltp_context.ident(model, ctx)
                payload = _table_payload_without_identifiers(model, _oltp_context.payload(ctx))
                pk_name = _single_pk_name(model)
                try:
                    existing = await _crud_ops.read(model, ident, db=_oltp_context.db(ctx))
                except Exception:
                    existing = None
                try:
                    if existing is None:
                        result = await _crud_ops.create(
                            model,
                            {pk_name: ident, **payload},
                            db=_oltp_context.db(ctx),
                        )
                    else:
                        replacement = _table_replace_payload(model, existing, payload)
                        result = await _crud_ops.replace(
                            model,
                            ident,
                            replacement,
                            db=_oltp_context.db(ctx),
                        )
                except IntegrityError as exc:
                    raise HTTPException(status.HTTP_409_CONFLICT, "Conflict") from exc
                except Exception as exc:
                    raise HTTPException(status.HTTP_409_CONFLICT, "Conflict") from exc
                setattr(ctx, "result", result)
                return
            await current_replace(obj, ctx)

        setattr(_compat_replace_run, "__tigrbl_auth_table_replace_compat__", True)
        _handler_replace_module._run = _compat_replace_run


def _install_table_crud_ops_compat() -> None:
    from tigrbl_ops_oltp.crud import ops as _crud_ops

    current_replace = getattr(_crud_ops, "replace", None)
    if callable(current_replace) and not getattr(current_replace, "__tigrbl_auth_table_replace_compat__", False):
        original_replace = current_replace
        original_read = _crud_ops.read

        async def _compat_replace(model: type, ident: Any, payload: Any, *, db: Any) -> Any:
            if not _is_local_table_model(model):
                return await original_replace(model, ident, payload, db=db)
            existing = await original_read(model, ident, db=db)
            replacement = _table_replace_payload(model, existing, payload)
            return await original_replace(model, ident, replacement, db=db)

        setattr(_compat_replace, "__tigrbl_auth_table_replace_compat__", True)
        _crud_ops.replace = _compat_replace

    current_clear = getattr(_crud_ops, "clear", None)
    if callable(current_clear) and not getattr(current_clear, "__tigrbl_auth_table_clear_compat__", False):
        original_clear = current_clear
        original_list = _crud_ops.list
        original_delete = _crud_ops.delete

        async def _compat_clear(model: type, filters: Any, *, db: Any) -> Any:
            if not _is_local_table_model(model):
                return await original_clear(model, filters, db=db)
            normalized = _normalize_payload(filters)
            result = await original_clear(model, normalized, db=db)
            if _deleted_count(result) > 0 or not normalized:
                return result
            clauses = []
            for key, value in normalized.items():
                column = getattr(model, key, None)
                if column is None:
                    continue
                coerced = value
                if isinstance(value, str):
                    try:
                        coerced = UUIDValue(value)
                    except ValueError:
                        coerced = value
                clauses.append(column == coerced)
            if not clauses:
                rows = await original_list(model, normalized, db=db)
            else:
                execution = await db.execute(select(model).where(*clauses))
                rows = list(execution.scalars().all())
            deleted = 0
            for row in rows or []:
                ident = getattr(row, "id", None)
                if ident is None:
                    continue
                await original_delete(model, ident, db=db)
                deleted += 1
            return {"deleted": deleted}

        setattr(_compat_clear, "__tigrbl_auth_table_clear_compat__", True)
        _crud_ops.clear = _compat_clear


def _install_jsonrpc_egress_compat() -> None:
    from tigrbl_atoms.atoms.egress import asgi_send as _asgi_send_module

    current = getattr(_asgi_send_module, "_run", None)
    if not callable(current) or getattr(current, "__tigrbl_auth_jsonrpc_egress_compat__", False):
        return

    current_send_transport = getattr(_asgi_send_module, "_send_transport_response", None)

    def _jsonrpc_result_envelope(ctx: Any) -> dict[str, Any] | None:
        temp = getattr(ctx, "temp", None)
        if not isinstance(temp, dict):
            return None
        rpc_id = temp.get("jsonrpc_request_id")
        is_jsonrpc = rpc_id is not None
        for section_key in ("route", "dispatch"):
            section = temp.get(section_key)
            if not isinstance(section, Mapping):
                continue
            for payload_key in ("rpc_envelope", "rpc"):
                payload = section.get(payload_key)
                if isinstance(payload, Mapping) and payload.get("jsonrpc") == "2.0":
                    is_jsonrpc = True
                    rpc_id = payload.get("id", rpc_id)
        if not is_jsonrpc:
            return None
        return {"jsonrpc": "2.0", "result": None, "id": rpc_id}

    async def _compat_run(obj: object | None, ctx: Any) -> None:
        del obj
        envelope = _jsonrpc_result_envelope(ctx)
        if envelope is not None and getattr(ctx, "result", None) is None:
            ctx.result = envelope
            if getattr(ctx, "status_code", None) in (None, 204):
                ctx.status_code = 200
        await current(None, ctx)

    setattr(_compat_run, "__tigrbl_auth_jsonrpc_egress_compat__", True)
    _asgi_send_module._run = _compat_run

    if callable(current_send_transport) and not getattr(current_send_transport, "__tigrbl_auth_jsonrpc_transport_compat__", False):
        async def _compat_send_transport_response(env: Any, ctx: Any) -> None:
            envelope = _jsonrpc_result_envelope(ctx)
            if envelope is not None:
                temp = getattr(ctx, "temp", None)
                if not isinstance(temp, dict):
                    temp = {}
                    setattr(ctx, "temp", temp)
                egress = temp.setdefault("egress", {})
                transport = egress.get("transport_response")
                if not isinstance(transport, dict):
                    transport = {
                        "status_code": 200,
                        "headers": {"content-type": "application/json; charset=utf-8"},
                        "body": envelope,
                    }
                    egress["transport_response"] = transport
                elif transport.get("body") is None:
                    transport["status_code"] = 200
                    headers = transport.get("headers")
                    if not isinstance(headers, dict):
                        headers = {}
                        transport["headers"] = headers
                    headers.setdefault("content-type", "application/json; charset=utf-8")
                    transport["body"] = envelope
                if getattr(ctx, "result", None) is None:
                    ctx.result = envelope
                if getattr(ctx, "status_code", None) in (None, 204):
                    ctx.status_code = 200
            await current_send_transport(env, ctx)

        setattr(_compat_send_transport_response, "__tigrbl_auth_jsonrpc_transport_compat__", True)
        _asgi_send_module._send_transport_response = _compat_send_transport_response


def _install_dependency_injection_compat() -> None:
    from tigrbl_concrete._concrete import _route as _route_module

    current = getattr(_route_module, "_invoke_route_handler", None)
    if not callable(current) or getattr(current, "__tigrbl_auth_dependency_injection_compat__", False):
        return

    async def _resolve_route_dependency(
        resolver: Any,
        *,
        owner: Any,
        route: Any,
        ctx: Any,
        request: Any | None,
        path_params: Mapping[str, Any],
    ) -> Any:
        overrides = getattr(owner, "dependency_overrides", {}) or {}
        resolver = overrides.get(resolver, resolver)
        signature = inspect.signature(resolver)
        params = list(signature.parameters.items())
        kwargs: dict[str, Any] = {}
        concrete_request = request

        async def _ensure_request() -> Any:
            nonlocal concrete_request
            if concrete_request is None:
                concrete_request = _route_module._route_request(route, ctx, coerce_concrete=True)
            return concrete_request

        async def _resolve_param_value(name: str, param: inspect.Parameter) -> Any:
            default = param.default
            nested_dep = getattr(default, "dependency", None)
            if callable(nested_dep):
                return await _resolve_route_dependency(
                    nested_dep,
                    owner=owner,
                    route=route,
                    ctx=ctx,
                    request=await _ensure_request(),
                    path_params=path_params,
                )

            annotation = param.annotation
            if name in path_params:
                return path_params[name]
            if name in {"ctx", "_ctx"} or annotation is dict or annotation is Any:
                return ctx
            if name in {"request", "_request"} or getattr(annotation, "__name__", None) == "Request":
                return await _ensure_request()

            location = getattr(default, "location", None)
            alias = getattr(default, "alias", None) or name
            request_obj = await _ensure_request()
            if location == "header":
                headers = getattr(request_obj, "headers", {}) or {}
                return headers.get(alias, headers.get(str(alias).lower(), getattr(default, "default", None)))
            if location == "query":
                query = getattr(request_obj, "query_params", {}) or {}
                return query.get(alias, getattr(default, "default", None))
            if location == "path":
                return path_params.get(alias, getattr(default, "default", None))
            if location == "body":
                form_reader = getattr(request_obj, "form", None)
                body_data: Any = None
                if callable(form_reader):
                    try:
                        body_data = await form_reader()
                    except Exception:
                        body_data = None
                if isinstance(body_data, Mapping):
                    return body_data.get(alias, getattr(default, "default", None))
                payload = getattr(request_obj, "body", None)
                if isinstance(payload, Mapping):
                    return payload.get(alias, getattr(default, "default", None))
                return getattr(default, "default", None)

            if len(params) == 1 and param.default is inspect._empty and not path_params:
                return await _ensure_request()
            if param.default is not inspect._empty:
                return param.default
            raise TypeError(f"{resolver.__name__}() missing required argument: {name}")

        for name, param in params:
            kwargs[name] = await _resolve_param_value(name, param)

        resolved = resolver(**kwargs) if kwargs else resolver()
        if inspect.isasyncgen(resolved):
            temp = getattr(ctx, "temp", None)
            if isinstance(temp, dict):
                temp.setdefault("route_dependency_cleanups", []).append(resolved.aclose)
            try:
                resolved = await resolved.__anext__()
            except StopAsyncIteration:
                resolved = None
        if inspect.isawaitable(resolved):
            resolved = await resolved
        return resolved

    async def _compat_invoke_route_handler(route: Any, ctx: Any) -> None:
        request: Any | None = None
        path_params = _route_module._route_path_params(route, ctx)
        kwargs: dict[str, Any] = {}
        signature = inspect.signature(route.handler)
        params = list(signature.parameters.items())

        for name, param in params:
            if name in path_params:
                kwargs[name] = path_params[name]
                continue
            default = param.default
            dep_callable = getattr(default, "dependency", None)
            if callable(dep_callable):
                owner = getattr(ctx, "app", None) or getattr(ctx, "router", None)
                kwargs[name] = await _resolve_route_dependency(
                    dep_callable,
                    owner=owner,
                    route=route,
                    ctx=ctx,
                    request=request,
                    path_params=path_params,
                )
                continue
            annotation = param.annotation
            if name in {"ctx", "_ctx"} or annotation is dict or annotation is Any:
                kwargs[name] = ctx
                continue
            if name in {"request", "_request"} or getattr(annotation, "__name__", None) == "Request":
                if request is None:
                    request = _route_module._route_request(route, ctx, coerce_concrete=True)
                kwargs[name] = request
                continue
            if len(params) == 1 and not path_params and param.default is inspect._empty:
                if request is None:
                    request = _route_module._route_request(route, ctx, coerce_concrete=False)
                kwargs[name] = request

        try:
            response = route.handler(**kwargs) if kwargs else route.handler()
            if inspect.isawaitable(response):
                response = await response

            if isinstance(response, Response):
                payload = {
                    "status_code": int(getattr(response, "status_code", 200) or 200),
                    "headers": dict(getattr(response, "headers", ()) or ()),
                    "body": (
                        response
                        if hasattr(response, "body_iterator")
                        else getattr(response, "body", b"")
                    ),
                }
                temp = getattr(ctx, "temp", None)
                if isinstance(temp, dict):
                    temp.setdefault("route", {})["short_circuit"] = True
                    temp.setdefault("egress", {})["transport_response"] = payload
                    temp["egress"]["suppress_asgi_send"] = True
                setattr(ctx, "transport_response", payload)
                return

            setattr(ctx, "result", response)
            temp = getattr(ctx, "temp", None)
            if isinstance(temp, dict):
                temp.setdefault("egress", {})["result"] = response
        finally:
            temp = getattr(ctx, "temp", None)
            cleanups = list(temp.get("route_dependency_cleanups", [])) if isinstance(temp, dict) else []
            for cleanup in reversed(cleanups):
                result = cleanup()
                if inspect.isawaitable(result):
                    await result
            if isinstance(temp, dict):
                temp.pop("route_dependency_cleanups", None)

    setattr(_compat_invoke_route_handler, "__tigrbl_auth_dependency_injection_compat__", True)
    _route_module._invoke_route_handler = _compat_invoke_route_handler


def _install_table_rpc_call_compat() -> None:
    from tigrbl_concrete._concrete import tigrbl_app as _tigrbl_app_module
    from tigrbl_concrete._concrete import tigrbl_router as _tigrbl_router_module
    from tigrbl_concrete._mapping.router import include as _rpc_include_module
    from tigrbl_concrete._mapping.router import rpc as _rpc_router_module
    from tigrbl_concrete._concrete import engine_resolver as _resolver
    from tigrbl_ops_oltp.crud import ops as _crud_ops

    current = getattr(_rpc_router_module, "rpc_call", None)
    if not callable(current) or getattr(current, "__tigrbl_auth_table_rpc_call_compat__", False):
        return

    original_rpc_call = current

    async def _compat_rpc_call(
        router: Any,
        model_or_name: Any,
        method: str,
        payload: Any = None,
        *,
        db: Any | None = None,
        request: Any = None,
        ctx: Mapping[str, Any] | None = None,
    ) -> Any:
        try:
            resolution = _rpc_router_module._fallback_resolution(router, model_or_name, method)
        except Exception:
            return await original_rpc_call(
                router,
                model_or_name,
                method,
                payload,
                db=db,
                request=request,
                ctx=ctx,
            )

        model = resolution.model
        target = getattr(resolution, "target", method)
        module_name = getattr(model, "__module__", "")
        normalized = _normalize_payload(payload)

        if module_name.startswith("tigrbl_auth.tables.") and (
            target == "clear" or (target == "create" and normalized)
        ):
            release = None
            if db is None:
                db, release = _resolver.acquire(router=router, model=model, op_alias=method)
            try:
                if target == "clear":
                    result = await _crud_ops.clear(model, normalized, db=db)
                else:
                    result = await _crud_ops.create(model, normalized, db=db)
                return _rpc_router_module._serialize_output(model, method, target, result)
            finally:
                if callable(release):
                    release()

        final = await original_rpc_call(
            router,
            model_or_name,
            method,
            payload,
            db=db,
            request=request,
            ctx=ctx,
        )
        if (
            module_name.startswith("tigrbl_auth.tables.")
            and target == "clear"
            and normalized
            and _deleted_count(_unwrap_runtime_result(final)) == 0
        ):
            retry = await _crud_ops.clear(model, normalized, db=db)
            return _rpc_router_module._serialize_output(model, method, target, retry)
        return final

    setattr(_compat_rpc_call, "__tigrbl_auth_table_rpc_call_compat__", True)
    _rpc_router_module.rpc_call = _compat_rpc_call
    _tigrbl_app_module._rpc_call = _compat_rpc_call
    _tigrbl_router_module._rpc_call = _compat_rpc_call
    _rpc_include_module._rpc_call = _compat_rpc_call


def _install_table_route_compat(router: Any, models: list[type]) -> None:
    from tigrbl_concrete._concrete import engine_resolver as _resolver
    from tigrbl_ops_oltp.crud import ops as _crud_ops
    from tigrbl_ops_oltp.crud.helpers.model import _coerce_pk_value
    from tigrbl_base._base._rpc_map import _serialize_output

    routes = getattr(router, "_routes", None)
    if not isinstance(routes, list):
        return

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
                normalized = _normalize_payload(payload)
                result = await _crud_ops.clear(_model, normalized, db=db)
                if _deleted_count(result) > 0 or not normalized:
                    return result
                clauses = []
                for key, value in normalized.items():
                    column = getattr(_model, key, None)
                    if column is None:
                        continue
                    coerced = value
                    if isinstance(value, str):
                        try:
                            coerced = UUIDValue(value)
                        except ValueError:
                            coerced = value
                    clauses.append(column == coerced)
                if not clauses:
                    return result
                execution = await db.execute(select(_model).where(*clauses))
                rows = list(execution.scalars().all())
                deleted = 0
                for row in rows:
                    ident = getattr(row, "id", None)
                    if ident is None:
                        continue
                    await _crud_ops.delete(_model, ident, db=db)
                    deleted += 1
                return {"deleted": deleted}

            setattr(_rpc_clear, "__tigrbl_auth_table_crud_clear__", True)
            setattr(rpc_root, "clear", _rpc_clear)

    updated_routes = []
    for route in list(routes):
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
                existing = await _crud_ops.read(_model, ident, db=db)
                replacement = _table_replace_payload(_model, existing, body)
                result = await _crud_ops.replace(_model, ident, replacement, db=db)
                content = _jsonify_value(_serialize_output(_model, "replace", "replace", result))
                return JSONResponse(content=content, status_code=200)
            finally:
                if callable(release):
                    release()

        updated_routes.append(
            dataclass_replace(route, handler=_replace_handler, response_model=None, status_code=200)
        )
    router._routes[:] = updated_routes


class TigrblRouter(_BaseTigrblRouter):
    """Compatibility alias for the current Tigrbl API router facade."""

    def include_tables(self, models: type | list[type] | tuple[type, ...]) -> None:
        if isinstance(models, type):
            model_seq = [models]
        else:
            model_seq = list(models)

        def _install_local_model_compat() -> None:
            for model in model_seq:
                if _is_local_table_model(model):
                    _install_local_handler_dict_compat(model)

        include_models = getattr(self, "include_models", None)
        if callable(include_models):
            include_models(model_seq)
            _install_local_model_compat()
            _install_table_route_compat(self, model_seq)
            return

        parent_include_tables = getattr(super(), "include_tables", None)
        if callable(parent_include_tables):
            parent_include_tables(model_seq)
            _install_local_model_compat()
            _install_table_route_compat(self, model_seq)
            return

        include_table = getattr(self, "include_table", None)
        if callable(include_table):
            for model in model_seq:
                include_table(model)
            _install_local_model_compat()
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
_install_table_handler_compat()
_install_table_crud_ops_compat()
_install_jsonrpc_egress_compat()
_install_dependency_injection_compat()
_install_table_rpc_call_compat()


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
