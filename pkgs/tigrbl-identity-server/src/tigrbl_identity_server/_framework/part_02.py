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


