"""Import/export command fragments loaded into the shared handler namespace."""

from __future__ import annotations

from tigrbl_identity_storage_runtime.portability import (
    export_status as _svc_export_status,
    import_status as _svc_import_status,
    run_export_file as _svc_run_export_file,
    run_import_file as _svc_run_import_file,
    validate_export_plan as _svc_validate_export_plan,
    validate_import_file as _svc_validate_import_file,
)


def handle_import_validate(args: Any) -> int:
    input_path = getattr(args, "input", None) or getattr(args, "from_file", None)
    if not input_path:
        raise SystemExit("--input is required")
    payload = {
        "command": "import.validate",
        **_svc_validate_import_file(Path(input_path).resolve()),
    }
    return _emit(args, payload)


def handle_import_run(args: Any) -> int:
    input_path = getattr(args, "input", None) or getattr(args, "from_file", None)
    if not input_path:
        raise SystemExit("--input is required")
    context = _svc_context(args, "import", "import.run")
    result = _svc_run_import_file(context, path=Path(input_path).resolve())
    return _svc_emit(args, result)


def handle_import_status(args: Any) -> int:
    payload = {
        "command": "import.status",
        **_svc_import_status(_repo_root(getattr(args, "repo_root", None))),
    }
    return _emit(args, payload)


def handle_export_validate(args: Any) -> int:
    context = _svc_context(args, "export", "export.validate")
    payload = {
        "command": "export.validate",
        **_svc_validate_export_plan(
            context, redact=bool(getattr(args, "redact", False))
        ),
    }
    return _emit(args, payload)
