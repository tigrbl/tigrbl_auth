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
    "admin_tenants.py": "tigrbl_auth_backend_app_platform_admin.tenants",
    "auth_flows.py": "tigrbl_identity_storage.tables.auth_session",
    "authorize.py": "tigrbl_identity_storage.tables.auth_code",
    "device_authorization.py": "tigrbl_identity_storage.tables.device_code",
    "login.py": "tigrbl_auth_router_session_login",
    "logout.py": "tigrbl_identity_storage.tables.logout_state",
    "my_account.py": "tigrbl_identity_storage.tables.user",
    "par.py": "tigrbl_auth_router_oauth_par",
    "register.py": "tigrbl_identity_storage.tables.client_registration",
    "revoke.py": "tigrbl_identity_storage.tables.revoked_token",
    "token.py": "tigrbl_identity_storage.tables.token_record",
}


def test_server_has_no_rest_schema_bucket_module() -> None:
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_server.routers.schemas")


def test_rest_schema_facade_points_to_protocol_and_api_owned_schemas() -> None:
    with pytest.warns(DeprecationWarning):
        schemas = importlib.reload(importlib.import_module("tigrbl_auth.api.rest.schemas"))
    from tigrbl_auth_protocol_oauth.schemas import TokenPair
    assert not hasattr(schemas, "CredsIn")
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
    assert target.startswith(
        (
            "tigrbl_identity_storage.tables",
                "tigrbl_identity_storage_runtime",
                "tigrbl_auth_router_",
                "tigrbl_auth_backend_app_",
            )
        )
    assert not path.exists()


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


def test_realm_admin_routes_live_in_platform_backend_app_package() -> None:
    app_module = importlib.import_module("tigrbl_auth_backend_app_platform_admin.realms")
    storage_module = importlib.import_module("tigrbl_identity_storage.tables.realm")
    route_names = {
        "admin_list_realms",
        "admin_create_realm",
        "admin_get_realm",
        "admin_update_realm",
        "admin_delete_realm",
        "admin_list_realm_tenants",
        "admin_create_realm_tenant",
    }

    assert hasattr(app_module, "router")
    assert not hasattr(app_module, "api")
    assert sorted(name for name in route_names if not hasattr(app_module, name)) == []
    assert not hasattr(storage_module, "admin_api")
    assert not hasattr(storage_module, "admin_router")
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module.Realm, name)) == []


def test_tenant_admin_routes_and_dtos_live_in_platform_backend_app_package() -> None:
    runtime_module = importlib.import_module("tigrbl_auth_backend_app_platform_admin.tenants")
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
    assert not hasattr(runtime_module, "api")
    assert not hasattr(storage_module, "admin_api")
    assert not hasattr(storage_module, "admin_router")
    assert sorted(name for name in route_names if not hasattr(runtime_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    assert sorted(name for name in route_names if hasattr(table_class, name)) == []
    for dto_name in {
        "AdminTenantOut",
        "AdminTenantProvisionIn",
        "AdminTenantUpdateIn",
    }:
        assert hasattr(runtime_module, dto_name)
        assert not hasattr(storage_module, dto_name)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_storage_runtime.tenant_admin")


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
    assert runtime_module.admin_api is runtime_module.admin_router
    assert not hasattr(storage_module, "admin_api")
    assert not hasattr(storage_module, "admin_router")
    assert sorted(name for name in route_names if not hasattr(runtime_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    for dto_name in {
        "AdminPasswordChangeIn",
        "AdminPasswordResetCompleteIn",
        "AdminPasswordResetRequestIn",
        "AdminSessionOut",
        "CredsIn",
    }:
        assert hasattr(runtime_module, dto_name)
        assert not hasattr(storage_module, dto_name)


def test_identity_admin_routes_live_in_platform_backend_app_package() -> None:
    app_module = importlib.import_module("tigrbl_auth_backend_app_platform_admin.identities")
    storage_module = importlib.import_module("tigrbl_identity_storage.tables.user")
    route_names = {
        "admin_list_identities",
        "admin_create_identity",
        "admin_update_identity",
        "admin_delete_identity",
    }

    assert hasattr(app_module, "router")
    assert not hasattr(app_module, "api")
    assert sorted(name for name in route_names if not hasattr(app_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module.User, name)) == []


def test_my_account_profile_routes_live_in_backend_app_package() -> None:
    app_module = importlib.import_module("tigrbl_auth_backend_app_my_account.profiles")
    storage_module = importlib.import_module("tigrbl_identity_storage.tables.user")
    route_names = {"get_account_profile", "update_account_profile", "change_account_password"}

    assert hasattr(app_module, "router")
    assert not hasattr(app_module, "api")
    assert sorted(name for name in route_names if not hasattr(app_module, name)) == []
    assert not hasattr(storage_module, "account_api")
    assert not hasattr(storage_module, "account_router")
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    assert sorted(name for name in route_names if hasattr(storage_module.User, name)) == []


def test_my_account_session_routes_live_in_backend_app_package() -> None:
    app_module = importlib.import_module("tigrbl_auth_backend_app_my_account.sessions")
    storage_module = importlib.import_module(
        "tigrbl_identity_storage.tables.auth_session"
    )
    table_class = storage_module.AuthSession
    route_names = {"list_account_sessions", "revoke_account_session"}

    assert hasattr(app_module, "router")
    assert not hasattr(app_module, "api")
    assert hasattr(app_module, "MyAccountSessionOut")
    assert sorted(name for name in route_names if not hasattr(app_module, name)) == []
    assert not hasattr(storage_module, "account_api")
    assert not hasattr(storage_module, "account_router")
    assert not hasattr(storage_module, "MyAccountSessionOut")
    assert sorted(name for name in route_names if hasattr(storage_module, name)) == []
    assert sorted(name for name in route_names if hasattr(table_class, name)) == []


def test_token_endpoint_carrier_and_runtime_live_above_storage() -> None:
    storage_module = importlib.import_module(
        "tigrbl_identity_storage.tables.token_record"
    )
    carrier_module = importlib.import_module("tigrbl_auth_router_oauth_token")
    runtime_module = importlib.import_module("tigrbl_identity_server.token_surface")

    assert hasattr(carrier_module, "build_token_router")
    assert hasattr(runtime_module, "router")
    assert hasattr(runtime_module, "token_request")
    assert not hasattr(storage_module, "api")
    assert not hasattr(storage_module, "router")
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_storage_runtime.token_endpoint")


@pytest.mark.parametrize(
    ("runtime_module_name", "storage_module_name", "class_name", "route_names"),
    [
        (
            "tigrbl_identity_server.login_surface",
            "tigrbl_identity_storage.tables.auth_session",
            "AuthSession",
            set(),
        ),
        (
            "tigrbl_identity_server.authorization_surface",
            "tigrbl_identity_storage.tables.auth_code",
            "AuthCode",
            set(),
        ),
        (
            "tigrbl_identity_server.client_registration_surface",
            "tigrbl_identity_storage.tables.client_registration",
            "ClientRegistration",
            set(),
        ),
        (
            "tigrbl_identity_server.device_authorization_surface",
            "tigrbl_identity_storage.tables.device_code",
            "DeviceCode",
            {"device_authorization"},
        ),
        (
            "tigrbl_identity_server.par_surface",
            "tigrbl_identity_storage.tables.pushed_authorization_request",
            "PushedAuthorizationRequest",
            set(),
        ),
        (
            "tigrbl_identity_server.logout_surface",
            "tigrbl_identity_storage.tables.logout_state",
            "LogoutState",
            {"logout"},
        ),
        (
            "tigrbl_identity_server.userinfo_surface",
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
        "tigrbl_identity_server.authorization_surface",
        "tigrbl_identity_server.login_surface",
        "tigrbl_identity_server.client_registration_surface",
        "tigrbl_identity_server.par_surface",
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


def test_consent_account_routes_live_above_storage_table_module() -> None:
    runtime_module = importlib.import_module("tigrbl_auth_backend_app_my_account.consents")
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

    assert hasattr(runtime_module, "router")
    assert not hasattr(runtime_module, "api")
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
