from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CAPABILITIES = ROOT / "pkgs" / "40-capabilities"

FORBIDDEN_IMPORT_PREFIXES = {
    "tigrbl_auth",
    "tigrbl_auth_api",
    "tigrbl_identity_cli",
    "tigrbl_identity_operator",
    "tigrbl_identity_runtime",
    "tigrbl_identity_server",
    "tigrbl_identity_testkit",
}

KNOWN_HIGHER_LAYER_IMPORTS = {
    "pkgs/40-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/_token_service/runtime.py": [
        "tigrbl_identity_runtime.settings",
    ],
    "pkgs/40-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/adapters/local.py": [
        "tigrbl_identity_server.security.auth",
        "tigrbl_identity_server.security.context",
    ],
    "pkgs/40-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/adapters/remote.py": [
        "tigrbl_identity_server.security.context",
    ],
    "pkgs/40-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/authenticators.py": [
        "tigrbl_identity_runtime.deployment",
        "tigrbl_identity_runtime.settings",
        "tigrbl_identity_server.security.context",
    ],
    "pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/admin_gate.py": [
        "tigrbl_identity_runtime.deployment",
    ],
    "pkgs/40-capabilities/tigrbl-identity-admin/src/tigrbl_identity_admin/bootstrap.py": [
        "tigrbl_identity_runtime.deployment",
        "tigrbl_identity_runtime.engine_resolver",
        "tigrbl_identity_runtime.settings",
        "tigrbl_identity_server.api.surfaces",
        "tigrbl_identity_server.security.handler_records",
    ],
}


def _python_files() -> list[Path]:
    return sorted(CAPABILITIES.glob("* /src/**/*.py".replace(" ", "")))


def _absolute_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imports.add(node.module)
    return imports


def test_40_capabilities_have_only_known_higher_layer_imports() -> None:
    offenders: dict[str, list[str]] = {}

    for path in _python_files():
        forbidden = [
            imported
            for imported in sorted(_absolute_imports(path))
            if any(
                imported == prefix or imported.startswith(f"{prefix}.")
                for prefix in FORBIDDEN_IMPORT_PREFIXES
            )
        ]
        if forbidden:
            offenders[path.relative_to(ROOT).as_posix()] = forbidden

    assert offenders == KNOWN_HIGHER_LAYER_IMPORTS


def test_40_capabilities_do_not_import_operator_store_directly() -> None:
    offenders: dict[str, list[str]] = {}

    for path in _python_files():
        forbidden = [
            imported
            for imported in sorted(_absolute_imports(path))
            if imported == "tigrbl_identity_storage.operator_store"
            or imported.startswith("tigrbl_identity_storage.operator_store.")
        ]
        if forbidden:
            offenders[path.relative_to(ROOT).as_posix()] = forbidden

    assert offenders == {}


def test_authn_credentials_token_service_uses_context_not_operator_actions() -> None:
    token_service_root = (
        CAPABILITIES
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "_token_service"
    )

    assert not (token_service_root / "operator.py").exists()

    init_source = (token_service_root / "__init__.py").read_text(encoding="utf-8")
    assert "operator_token" not in init_source
    assert "list_operator_tokens_for_context" not in init_source
    assert "exchange_operator_token_for_context" not in init_source
