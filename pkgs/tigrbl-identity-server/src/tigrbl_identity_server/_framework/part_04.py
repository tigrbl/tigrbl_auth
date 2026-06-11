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
