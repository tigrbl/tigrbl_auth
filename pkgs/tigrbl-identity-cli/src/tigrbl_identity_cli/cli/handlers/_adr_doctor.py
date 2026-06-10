from __future__ import annotations

from tigrbl_auth.services.session_service import (
    exchange_token_for_context as _svc_exchange_token_for_context,
    get_session_for_context as _svc_get_session_for_context,
    get_token_for_context as _svc_get_token_for_context,
    introspect_token_for_context as _svc_introspect_token_for_context,
    list_sessions_for_context as _svc_list_sessions_for_context,
    list_tokens_for_context as _svc_list_tokens_for_context,
    revoke_all_sessions_for_context as _svc_revoke_all_sessions_for_context,
    revoke_all_tokens_for_context as _svc_revoke_all_tokens_for_context,
    revoke_session_for_context as _svc_revoke_session_for_context,
    revoke_token_for_context as _svc_revoke_token_for_context,
)
from tigrbl_auth.services.discovery_service import (
    diff_discovery as _svc_diff_discovery,
    publish_discovery as _svc_publish_discovery,
    show_discovery as _svc_show_discovery,
    validate_discovery as _svc_validate_discovery,
)
from tigrbl_auth.services.import_export_service import (
    export_status as _svc_export_status,
    import_status as _svc_import_status,
    run_export_file as _svc_run_export_file,
    run_import_file as _svc_run_import_file,
    validate_export_plan as _svc_validate_export_plan,
    validate_import_file as _svc_validate_import_file,
)


def _svc_context(args: Any, resource: str, command: str | None = None) -> OperationContext:
    deployment = _resolved_from_args(args)
    return OperationContext(
        repo_root=_repo_root(getattr(args, "repo_root", None)),
        command=command or f"{resource}.{getattr(args, 'action', '')}".strip("."),
        resource=resource,
        dry_run=bool(getattr(args, "dry_run", False)),
        actor=getattr(args, "actor", None) or "system",
        profile=deployment.profile,
        tenant=getattr(args, "tenant", None),
        issuer=getattr(args, "issuer", None),
    )


def _svc_payload(result: Any) -> dict[str, Any]:
    if isinstance(result, (TransactionResult, ArtifactResult)):
        return result.to_payload()
    if isinstance(result, dict):
        return result
    return {"result": result}


def _svc_emit(args: Any, result: Any, rc: int = 0) -> int:
    return _emit_with_code(args, _svc_payload(result), rc=rc)


def _svc_failure(args: Any, context: OperationContext, exc: OperatorStateError) -> int:
    return _emit_with_code(args, exc.to_payload(context.command, context.resource), rc=exc.code)


def _svc_patch(args: Any) -> dict[str, Any]:
    return _mutation_payload(args)


def _handle_service_create(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.create")
    patch = _svc_patch(args)
    record_id = getattr(args, "id", None) or patch.get("id")
    if_exists = str(getattr(args, "if_exists", "error")).replace("fail", "error")
    if if_exists == "replace":
        if_exists = "replace"
    elif if_exists not in {"error", "skip", "update", "replace"}:
        if_exists = "error"
    try:
        result = _svc_create_resource(context, record_id=record_id, patch=patch, if_exists=if_exists)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_update(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.update")
    patch = _svc_patch(args)
    record_id = getattr(args, "id", None) or patch.get("id")
    if_missing = str(getattr(args, "if_missing", "error")).replace("fail", "error")
    try:
        result = _svc_update_resource(context, record_id=record_id, patch=patch, if_missing=if_missing)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_delete(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.delete")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_delete_resource(context, record_id=record_id, if_missing="error")
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_get(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.get")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        if resource == "session":
            result = _svc_get_session_for_context(context, record_id=record_id)
        elif resource == "token":
            result = _svc_get_token_for_context(context, record_id=record_id)
        elif resource == "keys":
            result = get_operator_key_for_context(context, record_id=record_id)
        else:
            result = _svc_get_resource(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_list(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.list")
    kwargs = {
        "status_filter": getattr(args, "status_filter", None),
        "filter_expr": getattr(args, "filter", None),
        "sort": str(getattr(args, "sort", "id")),
        "offset": int(getattr(args, "offset", 0)),
        "limit": int(getattr(args, "limit", 50)),
    }
    try:
        if resource == "session":
            result = _svc_list_sessions_for_context(context, **kwargs)
        elif resource == "token":
            result = _svc_list_tokens_for_context(context, **kwargs)
        elif resource == "keys":
            result = list_operator_keys_for_context(context, **kwargs)
        else:
            result = _svc_list_resource_result(context, **kwargs)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_toggle(args: Any, resource: str, *, enabled: bool) -> int:
    context = _svc_context(args, resource, f"{resource}.{'enable' if enabled else 'disable'}")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_toggle_resource(context, record_id=record_id, enabled=enabled)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _generic_resource_handler(resource: str, action: str):
    def _handler(args: Any) -> int:
        if action == "create":
            return _handle_service_create(args, resource)
        if action == "update":
            return _handle_service_update(args, resource)
        if action == "delete":
            return _handle_service_delete(args, resource)
        if action == "get":
            return _handle_service_get(args, resource)
        if action == "list":
            return _handle_service_list(args, resource)
        if action == "enable":
            return _handle_service_toggle(args, resource, enabled=True)
        if action == "disable":
            return _handle_service_toggle(args, resource, enabled=False)
        raise KeyError(f"Unsupported generic resource action: {resource}.{action}")

    return _handler


def handle_client_rotate_secret(args: Any) -> int:
    context = _svc_context(args, "client", "client.rotate-secret")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_rotate_client_secret(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_identity_set_password(args: Any) -> int:
    context = _svc_context(args, "identity", "identity.set-password")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    patch = _svc_patch(args)
    try:
        result = _svc_set_identity_password(context, record_id=record_id, password=patch.get("password"))
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _lock_identity(args: Any, locked: bool) -> int:
    context = _svc_context(args, "identity", f"identity.{'lock' if locked else 'unlock'}")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_lock_identity(context, record_id=record_id, locked=locked)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _revoke_resource(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.revoke")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_revoke_session_for_context(context, record_id=record_id) if resource == "session" else _svc_revoke_token_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_session_revoke_all(args: Any) -> int:
    context = _svc_context(args, "session", "session.revoke-all")
    try:
        result = _svc_revoke_all_sessions_for_context(context, status_filter=getattr(args, "status_filter", None), filter_expr=getattr(args, "filter", None))
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_token_introspect(args: Any) -> int:
    context = _svc_context(args, "token", "token.introspect")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_introspect_token_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_token_exchange(args: Any) -> int:
    context = _svc_context(args, "token", "token.exchange")
    patch = _svc_patch(args)
    try:
        result = _svc_exchange_token_for_context(
            context,
            subject_token=getattr(args, "subject_token", None) or patch.get("subject_token"),
            requested_token_type=getattr(args, "requested_token_type", None) or patch.get("requested_token_type"),
            audience=getattr(args, "audience", None) or patch.get("audience"),
            resource=getattr(args, "resource", None) or patch.get("resource"),
            actor_token=getattr(args, "actor_token", None) or patch.get("actor_token"),
            extras=patch,
        )
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_generate(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.generate")
    patch = _svc_patch(args)
    for source, target in (("kid", "kid"), ("alg", "alg"), ("use", "use"), ("kty", "kty"), ("curve", "curve")):
        value = getattr(args, source, None)
        if value is not None:
            patch[target] = value
    if bool(getattr(args, "activate", False)):
        patch["status"] = "active"
        patch["enabled"] = True
    try:
        result = generate_operator_key_for_context(context, patch=patch)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_import(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.import")
    patch = _svc_patch(args)
    try:
        result = import_operator_key_for_context(context, patch=patch)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_export(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.export")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = export_operator_key_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_rotate(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.rotate")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = rotate_operator_key_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_retire(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.retire")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = retire_operator_key_for_context(context, record_id=record_id, retire_after=getattr(args, "retire_after", None))
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_publish_jwks(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.publish-jwks")
    result = publish_operator_jwks_for_context(context, output_path=getattr(args, "output", None))
    return _svc_emit(args, result)


def handle_discovery_show(args: Any) -> int:
    deployment = _resolved_from_args(args)
    payload = {"command": "discovery.show", "profile_source": deployment.profile_source, **_svc_show_discovery(_repo_root(getattr(args, "repo_root", None)), profile=deployment.profile)}
    return _emit(args, payload)


def handle_discovery_validate(args: Any) -> int:
    deployment = _resolved_from_args(args)
    payload = {"command": "discovery.validate", "profile_source": deployment.profile_source, **_svc_validate_discovery(_repo_root(getattr(args, "repo_root", None)), profile=deployment.profile)}
    return _emit(args, payload)


def handle_discovery_publish(args: Any) -> int:
    context = _svc_context(args, "discovery", "discovery.publish")
    result = _svc_publish_discovery(context, output_dir=Path(getattr(args, "output", None)).resolve() if getattr(args, "output", None) else None)
    return _svc_emit(args, result)


def handle_discovery_diff(args: Any) -> int:
    deployment = _resolved_from_args(args)
    payload = {"command": "discovery.diff", "profile_source": deployment.profile_source, **_svc_diff_discovery(_repo_root(getattr(args, "repo_root", None)), left_profile=getattr(args, "left_profile", None) or deployment.profile, right_profile=getattr(args, "right_profile", None))}
    return _emit(args, payload)


def handle_import_validate(args: Any) -> int:
    input_path = getattr(args, "input", None) or getattr(args, "from_file", None)
    if not input_path:
        raise SystemExit("--input is required")
    payload = {"command": "import.validate", **_svc_validate_import_file(Path(input_path).resolve())}
    return _emit(args, payload)


def handle_import_run(args: Any) -> int:
    input_path = getattr(args, "input", None) or getattr(args, "from_file", None)
    if not input_path:
        raise SystemExit("--input is required")
    context = _svc_context(args, "import", "import.run")
    result = _svc_run_import_file(context, path=Path(input_path).resolve())
    return _svc_emit(args, result)


def handle_import_status(args: Any) -> int:
    payload = {"command": "import.status", **_svc_import_status(_repo_root(getattr(args, "repo_root", None)))}
    return _emit(args, payload)


def handle_export_validate(args: Any) -> int:
    context = _svc_context(args, "export", "export.validate")
    payload = {"command": "export.validate", **_svc_validate_export_plan(context, redact=bool(getattr(args, "redact", False)))}
    return _emit(args, payload)
