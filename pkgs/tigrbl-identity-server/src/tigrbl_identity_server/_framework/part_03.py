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

        if _is_local_table_module(module_name) and (
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
            _is_local_table_module(module_name)
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


