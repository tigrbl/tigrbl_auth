from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


def package_src(name: str) -> Path:
    matches = sorted(PKGS.glob(f"**/{name}/src"))
    assert matches, f"missing package src for {name}"
    return matches[0]


STORAGE_ROOT = package_src("tigrbl-identity-storage")
NON_STORAGE_SOURCE_ROOTS = [
    package_src("tigrbl-auth-backend-app-my-account"),
    package_src("tigrbl-auth-backend-app-public"),
    package_src("tigrbl-auth-protocol-oauth"),
    package_src("tigrbl-authn-credentials"),
    package_src("tigrbl-identity-operator"),
    package_src("tigrbl-identity-server"),
]
STORAGE_RUNTIME_ROOT = package_src("tigrbl-identity-storage-runtime")

RAW_HANDLER_TOKENS = (
    ".handlers.create.core",
    ".handlers.update.core",
    ".handlers.delete.core",
    ".handlers.clear.core",
)

RAW_HANDLER_ALLOWLIST = {
    "pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/security/handler_records.py",
}

TABLE_ROUTE_FUNCTION_ALLOWLIST = {
    "profiles.py": {
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
    "identities.py": {
        "admin_create_identity",
        "admin_delete_identity",
        "admin_list_identities",
        "admin_update_identity",
    },
    "auth_code.py": {
        "authorize",
    },
    "consents.py": {
        "list_account_authorized_apps",
        "list_account_consents",
        "revoke_account_authorized_app",
        "revoke_account_consent",
    },
    "device_code.py": {
        "device_authorization",
    },
    "pushed_authorization_request.py": {
        "par",
    },
    "realms.py": {
        "admin_create_realm",
        "admin_create_realm_tenant",
        "admin_delete_realm",
        "admin_get_realm",
        "admin_list_realm_tenants",
        "admin_list_realms",
        "admin_update_realm",
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
    for root in [package_src("tigrbl-auth-backend-app-my-account"), package_src("tigrbl-auth-backend-app-public")]:
        if not root.exists():
            continue
        for path in _python_files(root):
            source = path.read_text(encoding="utf-8")
            if "openrpc" in source.lower() or '"/rpc"' in source or "'/rpc'" in source:
                offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_protocol_and_facade_ops_packages_are_not_supported() -> None:
    assert not (package_src("tigrbl-auth-protocol-oauth") / "tigrbl_auth_protocol_oauth" / "ops").exists()
    assert not (package_src("tigrbl-auth") / "tigrbl_auth" / "ops").exists()
    assert not (package_src("tigrbl-identity-server") / "tigrbl_identity_server" / "ops").exists()
    assert not (package_src("tigrbl-identity-server") / "tigrbl_identity_server" / "rest" / "routers").exists()
    assert not (package_src("tigrbl-auth") / "tigrbl_auth" / "api" / "rest" / "routers").exists()


def test_route_and_hook_declarations_are_owned_by_executable_layers() -> None:
    offenders: list[str] = []
    storage_tables_root = package_src("tigrbl-identity-storage") / "tigrbl_identity_storage" / "tables"
    storage_runtime_root = STORAGE_RUNTIME_ROOT / "tigrbl_identity_storage_runtime"
    executable_roots = tuple(
        root.resolve()
        for layer in ("50-protocols", "60-runtime", "80-routers")
        for root in (PKGS / layer).glob("*/src")
    )
    for root in sorted(PKGS.glob("**/src")):
        for path in _python_files(root):
            source = path.read_text(encoding="utf-8")
            if "@api.route" not in source and "hook_ctx(" not in source:
                continue
            resolved = path.resolve()
            if (
                storage_tables_root not in path.parents
                and storage_runtime_root not in path.parents
                and not any(root in resolved.parents for root in executable_roots)
            ):
                rel = path.relative_to(ROOT).as_posix()
                if "@api.route" in source:
                    offenders.append(f"{rel} declares route")
                if "hook_ctx(" in source:
                    offenders.append(f"{rel} declares hook")

    assert offenders == []


def test_protocol_packages_do_not_import_removed_oauth_ops() -> None:
    offenders: list[str] = []
    for root in [
        package_src("tigrbl-auth-protocol-oauth"),
        package_src("tigrbl-auth-protocol-oidc"),
        package_src("tigrbl-auth-protocol-rp"),
    ]:
        for path in _python_files(root):
            rel = path.relative_to(ROOT).as_posix()
            source = path.read_text(encoding="utf-8")
            if "tigrbl_auth_protocol_oauth.ops" in source:
                offenders.append(f"{rel} imports removed oauth ops")

    assert offenders == []


def test_storage_table_ops_are_not_hidden_in_module_level_free_functions() -> None:
    offenders: list[str] = []
    for path in (STORAGE_ROOT / "tigrbl_identity_storage" / "tables").glob("*.py"):
        if path.name in {"__init__.py", "engine.py"} or path.name.startswith("_"):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                if node.name in TABLE_ROUTE_FUNCTION_ALLOWLIST.get(path.name, set()):
                    continue
                offenders.append(f"{path.relative_to(ROOT).as_posix()}::{node.name}")

    assert offenders == []
