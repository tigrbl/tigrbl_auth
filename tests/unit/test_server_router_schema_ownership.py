from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"


def package_root(name: str) -> Path:
    matches = sorted(PKGS.glob(f"**/{name}/pyproject.toml"))
    assert matches, f"missing package root for {name}"
    return matches[0].parent


SERVER_ROOT = package_root("tigrbl-identity-server") / "src"
AUTH_FACADE_ROOT = package_root("tigrbl-auth") / "src"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _imports_from(path: Path) -> set[str]:
    tree = ast.parse(_source(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


ROUTER_DEPRECATION_TARGETS = {
    "__init__.py": "tigrbl_identity_storage.tables.*",
    "admin_auth.py": "tigrbl_identity_storage.tables.user",
    "admin_identities.py": "tigrbl_identity_storage.tables.user",
    "admin_realms.py": "tigrbl_identity_storage.tables.realm",
    "admin_tenants.py": "tigrbl_identity_storage_runtime.tenant_admin",
    "auth_flows.py": "tigrbl_identity_storage.tables.auth_session",
    "authorize.py": "tigrbl_identity_storage.tables.auth_code",
    "device_authorization.py": "tigrbl_identity_storage.tables.device_code",
    "login.py": "tigrbl_identity_storage_runtime.login",
    "logout.py": "tigrbl_identity_storage.tables.logout_state",
    "my_account.py": "tigrbl_identity_storage.tables.user",
    "par.py": "tigrbl_identity_storage.tables.pushed_authorization_request",
    "register.py": "tigrbl_identity_storage.tables.client_registration",
    "revoke.py": "tigrbl_identity_storage.tables.revoked_token",
    "token.py": "tigrbl_identity_storage.tables.token_record",
}


def test_server_has_no_rest_schema_bucket_module() -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_server.routers.schemas")


def test_rest_schema_facade_points_to_table_owned_schemas() -> None:
    with pytest.warns(DeprecationWarning):
        schemas = importlib.reload(importlib.import_module("tigrbl_auth.api.rest.schemas"))
    from tigrbl_identity_storage.schemas import CredsIn, TokenPair

    assert schemas.CredsIn is CredsIn
    assert schemas.TokenPair is TokenPair


def test_no_package_imports_removed_server_schema_bucket() -> None:
    offenders: list[str] = []
    for root in (SERVER_ROOT, AUTH_FACADE_ROOT):
        for path in root.rglob("*.py"):
            source = _source(path)
            if (
                "tigrbl_identity_server.routers.schemas" in source
                or "routers.schemas" in source
            ):
                offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


@pytest.mark.parametrize(
    ("route_file", "target"),
    sorted(ROUTER_DEPRECATION_TARGETS.items()),
)
def test_server_rest_router_bridges_warn_to_storage_owner(
    route_file: str,
    target: str,
) -> None:
    path = SERVER_ROOT / "tigrbl_identity_server" / "rest" / "routers" / route_file
    assert target.startswith(("tigrbl_identity_storage.tables", "tigrbl_identity_storage_runtime"))
    assert not path.exists()


@pytest.mark.parametrize(
    ("module_name", "names"),
    [
        (
            "tigrbl_identity_storage.tables.user",
            {
                "AdminPasswordChangeIn",
                "AdminPasswordResetCompleteIn",
                "AdminPasswordResetRequestIn",
                "AdminSessionOut",
                "AdminIdentityOut",
                "AdminIdentityProvisionIn",
                "AdminIdentityUpdateIn",
                "MyAccountMutationOut",
                "MyAccountPasswordChangeIn",
                "MyAccountProfileOut",
                "MyAccountProfileUpdateIn",
            },
        ),
        (
            "tigrbl_identity_storage.tables.tenant",
            {"AdminTenantOut", "AdminTenantProvisionIn", "AdminTenantUpdateIn"},
        ),
        (
            "tigrbl_identity_storage.tables.realm",
            {"AdminRealmOut", "AdminRealmProvisionIn", "AdminRealmUpdateIn"},
        ),
        ("tigrbl_identity_storage.tables.auth_session", {"MyAccountSessionOut"}),
    ],
)
def test_table_backed_rest_schemas_live_on_table_modules(
    module_name: str, names: set[str]
) -> None:
    module = importlib.import_module(module_name)

    missing = sorted(name for name in names if not hasattr(module, name))
    assert missing == []


@pytest.mark.parametrize(
    ("route_file", "required_imports"),
    [
        (
            "my_account.py",
            {
                "tigrbl_identity_storage.tables.auth_session",
                "tigrbl_identity_storage.tables.consent",
                "tigrbl_identity_storage.tables.user",
            },
        ),
    ],
)
def test_remaining_table_backed_rest_routers_import_schemas_from_table_modules(
    route_file: str, required_imports: set[str]
) -> None:
    path = SERVER_ROOT / "tigrbl_identity_server" / "rest" / "routers" / route_file
    assert route_file == "my_account.py"
    assert required_imports == {
        "tigrbl_identity_storage.tables.auth_session",
        "tigrbl_identity_storage.tables.consent",
        "tigrbl_identity_storage.tables.user",
    }
    assert not path.exists()


@pytest.mark.parametrize(
    ("module_name", "route_names"),
    [
        (
            "tigrbl_identity_storage.tables.user",
            {
                "admin_list_identities",
                "admin_create_identity",
                "admin_update_identity",
                "admin_delete_identity",
            },
        ),
        (
            "tigrbl_identity_storage.tables.realm",
            {
                "admin_list_realms",
                "admin_create_realm",
                "admin_get_realm",
                "admin_update_realm",
                "admin_delete_realm",
                "admin_list_realm_tenants",
                "admin_create_realm_tenant",
            },
        ),
    ],
)
def test_admin_route_handlers_live_on_storage_table_modules(
    module_name: str, route_names: set[str]
) -> None:
    module = importlib.import_module(module_name)
    table_name = module_name.rsplit(".", 1)[-1]
    class_name = {
        "realm": "Realm",
        "tenant": "Tenant",
        "user": "User",
    }[table_name]
    table_class = getattr(module, class_name)

    assert hasattr(module, "admin_api")
    assert hasattr(module, "admin_router")
    missing = sorted(name for name in route_names if not hasattr(module, name))
    assert missing == []
    missing_class_routes = sorted(
        name for name in route_names if not hasattr(table_class, name)
    )
    assert missing_class_routes == []


def test_tenant_admin_route_handlers_live_above_storage_table_module() -> None:
    runtime_module = importlib.import_module("tigrbl_identity_storage_runtime.tenant_admin")
    storage_module = importlib.import_module("tigrbl_identity_storage.tables.tenant")
    table_class = storage_module.Tenant
    route_names = {
        "admin_list_tenants",
        "admin_create_tenant",
        "admin_update_tenant",
        "admin_delete_tenant",
    }

    assert hasattr(runtime_module, "admin_router")
    assert hasattr(runtime_module, "router")
    assert not hasattr(runtime_module, "admin_api")
    assert not hasattr(storage_module, "admin_api")
    assert not hasattr(storage_module, "admin_router")
    assert sorted(name for name in route_names if not hasattr(runtime_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    assert sorted(name for name in route_names if hasattr(table_class, name)) == []


def test_admin_auth_routes_live_in_server_runtime() -> None:
    runtime_module = importlib.import_module("tigrbl_identity_server.admin_auth")
    storage_module = importlib.import_module("tigrbl_identity_storage.tables.user")
    route_names = {
        "admin_change_password",
        "admin_forgot_password",
        "admin_login",
        "admin_login_browser_redirect",
        "admin_logout",
        "admin_reset_password",
        "admin_session",
    }
    assert runtime_module.admin_api is storage_module.admin_api
    assert sorted(name for name in route_names if not hasattr(runtime_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []


@pytest.mark.parametrize(
    ("module_name", "class_name", "route_names"),
    [
        (
            "tigrbl_identity_storage.tables.user",
            "User",
            {
                "get_account_profile",
                "update_account_profile",
                "change_account_password",
            },
        ),
        (
            "tigrbl_identity_storage.tables.auth_session",
            "AuthSession",
            {
                "list_account_sessions",
                "revoke_account_session",
            },
        ),
    ],
)
def test_my_account_route_handlers_live_on_storage_table_modules(
    module_name: str, class_name: str, route_names: set[str]
) -> None:
    module = importlib.import_module(module_name)
    table_class = getattr(module, class_name)

    assert hasattr(module, "account_api")
    assert hasattr(module, "account_router")
    missing = sorted(name for name in route_names if not hasattr(module, name))
    assert missing == []
    missing_class_ops = sorted(name for name in route_names if not hasattr(table_class, name))
    assert missing_class_ops == []


@pytest.mark.parametrize(
    ("module_name", "class_name", "route_names"),
    [
        (
            "tigrbl_identity_storage.tables.token_record",
            "TokenRecord",
            {"token"},
        ),
    ],
)
def test_remaining_oauth_route_handlers_live_on_storage_table_modules(
    module_name: str,
    class_name: str,
    route_names: set[str],
) -> None:
    storage_module = importlib.import_module(module_name)
    runtime_module = importlib.import_module("tigrbl_identity_storage_runtime.token_endpoint")

    assert hasattr(runtime_module, "router")
    missing = sorted(name for name in route_names if not hasattr(runtime_module, name))
    assert missing == []
    assert not hasattr(storage_module, "api")
    assert not hasattr(storage_module, "router")


@pytest.mark.parametrize(
    ("runtime_module_name", "storage_module_name", "class_name", "route_names"),
    [
        (
            "tigrbl_identity_storage_runtime.login",
            "tigrbl_identity_storage.tables.auth_session",
            "AuthSession",
            {"login"},
        ),
        (
            "tigrbl_identity_storage_runtime.authorization",
            "tigrbl_identity_storage.tables.auth_code",
            "AuthCode",
            {"authorize"},
        ),
        (
            "tigrbl_identity_storage_runtime.client_registration",
            "tigrbl_identity_storage.tables.client_registration",
            "ClientRegistration",
            {"register", "register_get", "register_put", "register_delete"},
        ),
        (
            "tigrbl_identity_storage_runtime.device_authorization",
            "tigrbl_identity_storage.tables.device_code",
            "DeviceCode",
            {"device_authorization"},
        ),
        (
            "tigrbl_identity_storage_runtime.par",
            "tigrbl_identity_storage.tables.pushed_authorization_request",
            "PushedAuthorizationRequest",
            {"par"},
        ),
        (
            "tigrbl_identity_storage_runtime.revocation",
            "tigrbl_identity_storage.tables.revoked_token",
            "RevokedToken",
            {"revoke"},
        ),
        (
            "tigrbl_identity_storage_runtime.logout",
            "tigrbl_identity_storage.tables.logout_state",
            "LogoutState",
            {"logout"},
        ),
        (
            "tigrbl_identity_storage_runtime.userinfo",
            "tigrbl_identity_storage.tables.user",
            "User",
            {"userinfo"},
        ),
    ],
)
def test_moved_oauth_publishers_live_above_storage_table_modules(
    runtime_module_name: str,
    storage_module_name: str,
    class_name: str,
    route_names: set[str],
) -> None:
    runtime_module = importlib.import_module(runtime_module_name)
    storage_module = importlib.import_module(storage_module_name)
    table_class = getattr(storage_module, class_name)

    assert hasattr(runtime_module, "router")
    if runtime_module_name in {
        "tigrbl_identity_storage_runtime.authorization",
        "tigrbl_identity_storage_runtime.login",
    }:
        assert not hasattr(runtime_module, "api")
    else:
        assert hasattr(runtime_module, "api")
    missing = sorted(name for name in route_names if not hasattr(runtime_module, name))
    assert missing == []
    assert not hasattr(storage_module, "api")
    assert not hasattr(storage_module, "router")
    missing_class_ops = sorted(name for name in route_names if hasattr(table_class, name))
    assert missing_class_ops == []
    if runtime_module_name == "tigrbl_identity_storage_runtime.authorization":
        from tigrbl_identity_storage_runtime import AuthCodeRuntimeSpec

        runtime_ops = {operation.alias for operation in AuthCodeRuntimeSpec.ops}
        assert route_names <= runtime_ops


def test_consent_account_routes_live_above_storage_table_module() -> None:
    runtime_module = importlib.import_module("tigrbl_identity_storage_runtime.account_consent")
    storage_module = importlib.import_module("tigrbl_identity_storage.tables.consent")
    table_class = storage_module.Consent
    route_names = {
        "list_account_consents",
        "revoke_account_consent",
        "list_account_authorized_apps",
        "revoke_account_authorized_app",
    }
    table_op_names = {
        "list_for_user",
        "revoke_for_user",
        "revoke_for_client",
    }

    assert hasattr(runtime_module, "api")
    assert hasattr(runtime_module, "router")
    assert not hasattr(storage_module, "account_api")
    assert not hasattr(storage_module, "account_router")
    assert sorted(name for name in route_names if not hasattr(runtime_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    assert sorted(name for name in table_op_names if hasattr(table_class, name)) == []
    from tigrbl_identity_storage_runtime import ConsentRuntimeSpec

    runtime_ops = {operation.alias for operation in ConsentRuntimeSpec.ops}
    assert table_op_names <= runtime_ops


@pytest.mark.parametrize(
    "route_file",
    [
        "admin_identities.py",
        "admin_tenants.py",
        "admin_realms.py",
        "my_account.py",
        "login.py",
        "logout.py",
        "auth_flows.py",
        "authorize.py",
        "device_authorization.py",
        "par.py",
        "register.py",
        "revoke.py",
        "token.py",
        "admin_auth.py",
    ],
)
def test_relocated_table_backed_server_rest_routers_are_bridge_only(route_file: str) -> None:
    path = SERVER_ROOT / "tigrbl_identity_server" / "rest" / "routers" / route_file
    assert not path.exists()


@pytest.mark.parametrize(
    "path",
    [
        SERVER_ROOT / "tigrbl_identity_server" / "routers" / "auth_flows.py",
        SERVER_ROOT / "tigrbl_identity_server" / "routers" / "authz" / "oidc.py",
    ],
)
def test_legacy_router_modules_are_bridge_only(path: Path) -> None:
    assert not path.exists()
