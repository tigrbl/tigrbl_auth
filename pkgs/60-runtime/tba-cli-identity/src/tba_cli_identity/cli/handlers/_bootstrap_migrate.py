from __future__ import annotations

def handle_export_run(args: Any) -> int:
    output_path = Path(getattr(args, "output", None) or (_repo_root(getattr(args, "repo_root", None)) / "dist" / "exports" / "export.json")).resolve()
    context = _svc_context(args, "export", "export.run")
    result = _svc_run_export_file(context, path=output_path, redact=bool(getattr(args, "redact", False)))
    return _svc_emit(args, result)


def handle_export_status(args: Any) -> int:
    payload = {"command": "export.status", **_svc_export_status(_repo_root(getattr(args, "repo_root", None)))}
    return _emit(args, payload)


# refresh the dispatch table so surface variants resolve to the service layer
HANDLER_MAP.update(
    {
        "client.rotate_secret": handle_client_rotate_secret,
        "identity.set_password": handle_identity_set_password,
        "identity.lock": lambda args: _lock_identity(args, True),
        "identity.unlock": lambda args: _lock_identity(args, False),
        "session.revoke": lambda args: _revoke_resource(args, "session"),
        "session.revoke_all": handle_session_revoke_all,
        "token.introspect": handle_token_introspect,
        "token.revoke": lambda args: _revoke_resource(args, "token"),
        "token.exchange": handle_token_exchange,
        "keys.generate": handle_keys_generate,
        "keys.import": handle_keys_import,
        "keys.export": handle_keys_export,
        "keys.rotate": handle_keys_rotate,
        "keys.retire": handle_keys_retire,
        "keys.publish_jwks": handle_keys_publish_jwks,
        "discovery.show": handle_discovery_show,
        "discovery.validate": handle_discovery_validate,
        "discovery.publish": handle_discovery_publish,
        "discovery.diff": handle_discovery_diff,
        "import.validate": handle_import_validate,
        "import.run": handle_import_run,
        "import.status": handle_import_status,
        "export.validate": handle_export_validate,
        "export.run": handle_export_run,
        "export.status": handle_export_status,
    }
)
for _resource in ("tenant", "client", "identity", "flow"):
    for _action in ("create", "update", "delete", "get", "list", "enable", "disable"):
        HANDLER_MAP[f"{_resource}.{_action}"] = _generic_resource_handler(_resource, _action)
for _resource in ("session", "token"):
    for _action in ("get", "list"):
        HANDLER_MAP[f"{_resource}.{_action}"] = _generic_resource_handler(_resource, _action)
for _action in ("get", "list", "delete"):
    HANDLER_MAP[f"keys.{_action}"] = _generic_resource_handler("keys", _action)
