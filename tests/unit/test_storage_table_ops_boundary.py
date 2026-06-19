from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"
STORAGE_ROOT = PKGS / "tigrbl-identity-storage" / "src"
NON_STORAGE_SOURCE_ROOTS = [
    PKGS / "tigrbl-auth-api-my-account" / "src",
    PKGS / "tigrbl-auth-api-public" / "src",
    PKGS / "tigrbl-auth-protocol-oauth" / "src",
    PKGS / "tigrbl-authn-credentials" / "src",
    PKGS / "tigrbl-identity-operator" / "src",
    PKGS / "tigrbl-identity-server" / "src",
]

RAW_HANDLER_TOKENS = (
    ".handlers.create.core",
    ".handlers.update.core",
    ".handlers.delete.core",
    ".handlers.clear.core",
)

RAW_HANDLER_ALLOWLIST = {
    "pkgs/tigrbl-identity-server/src/tigrbl_identity_server/security/handler_records.py",
}

TABLE_ROUTE_FUNCTION_ALLOWLIST = {
    "_user_account_routes.py": {
        "change_account_password",
        "get_account_profile",
        "update_account_profile",
    },
    "_user_admin_auth_routes.py": {
        "admin_change_password",
        "admin_forgot_password",
        "admin_login",
        "admin_login_browser_redirect",
        "admin_logout",
        "admin_reset_password",
        "admin_session",
    },
    "_user_admin_identity_routes.py": {
        "admin_create_identity",
        "admin_delete_identity",
        "admin_list_identities",
        "admin_update_identity",
    },
    "auth_session.py": {
        "list_account_sessions",
        "login",
        "revoke_account_session",
    },
    "auth_code.py": {
        "authorize",
    },
    "consent.py": {
        "list_account_authorized_apps",
        "list_account_consents",
        "revoke_account_authorized_app",
        "revoke_account_consent",
    },
    "client_registration.py": {
        "register",
        "register_delete",
        "register_get",
        "register_put",
    },
    "device_code.py": {
        "device_authorization",
    },
    "pushed_authorization_request.py": {
        "par",
    },
    "realm.py": {
        "admin_create_realm",
        "admin_create_realm_tenant",
        "admin_delete_realm",
        "admin_get_realm",
        "admin_list_realm_tenants",
        "admin_list_realms",
        "admin_update_realm",
    },
    "tenant.py": {
        "admin_create_tenant",
        "admin_delete_tenant",
        "admin_list_tenants",
        "admin_update_tenant",
    },
    "user.py": {
        "admin_change_password",
        "admin_create_identity",
        "admin_delete_identity",
        "admin_forgot_password",
        "admin_list_identities",
        "admin_login",
        "admin_login_browser_redirect",
        "admin_logout",
        "admin_reset_password",
        "admin_session",
        "admin_update_identity",
        "change_account_password",
        "get_account_profile",
        "update_account_profile",
    },
    "logout_state.py": {
        "logout",
    },
    "revoked_token.py": {
        "revoke",
    },
    "token_record.py": {
        "token",
    },
}


def _python_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.py") if "__pycache__" not in path.parts]


def test_non_storage_packages_do_not_own_raw_durable_table_mutations() -> None:
    offenders: list[str] = []
    for root in NON_STORAGE_SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in _python_files(root):
            rel = path.relative_to(ROOT).as_posix()
            if rel in RAW_HANDLER_ALLOWLIST:
                continue
            source = path.read_text(encoding="utf-8")
            for token in RAW_HANDLER_TOKENS:
                if token in source:
                    offenders.append(f"{rel} uses {token}")

    assert offenders == []


def test_no_rpc_support_is_reintroduced_in_product_api_packages() -> None:
    offenders: list[str] = []
    for root in [PKGS / "tigrbl-auth-api-my-account" / "src", PKGS / "tigrbl-auth-api-public" / "src"]:
        if not root.exists():
            continue
        for path in _python_files(root):
            source = path.read_text(encoding="utf-8")
            if "openrpc" in source.lower() or '"/rpc"' in source or "'/rpc'" in source:
                offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_storage_table_ops_are_not_hidden_in_module_level_free_functions() -> None:
    offenders: list[str] = []
    for path in (STORAGE_ROOT / "tigrbl_identity_storage" / "tables").glob("*.py"):
        if path.name in {"__init__.py", "_ops.py", "engine.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                if node.name in TABLE_ROUTE_FUNCTION_ALLOWLIST.get(path.name, set()):
                    continue
                offenders.append(f"{path.relative_to(ROOT).as_posix()}::{node.name}")

    assert offenders == []
