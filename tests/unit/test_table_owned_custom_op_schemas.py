from __future__ import annotations

import importlib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
STORAGE_SRC = (
    ROOT
    / "pkgs"
    / "01-storage"
    / "tigrbl-identity-storage"
    / "src"
    / "tigrbl_identity_storage"
)


def test_protocol_wire_schemas_are_not_owned_by_storage_tables() -> None:
    from tigrbl_auth_protocol_oauth import schemas as oauth_schemas
    from tigrbl_auth_protocol_oidc import schemas as oidc_schemas
    from tigrbl_identity_storage.tables import (
        AuthSession,
        ClientRegistration,
        DeviceCode,
        LogoutState,
        PushedAuthorizationRequest,
        RevokedToken,
        TokenRecord,
    )

    assert oauth_schemas.TokenPair.__module__ == oauth_schemas.__name__
    assert oauth_schemas.DynamicClientRegistrationIn.__module__ == oauth_schemas.__name__
    assert oauth_schemas.DeviceAuthorizationOut.__module__ == oauth_schemas.__name__
    assert oauth_schemas.PushedAuthorizationResponse.__module__ == oauth_schemas.__name__
    assert oauth_schemas.RevocationOut.__module__ == oauth_schemas.__name__
    assert oidc_schemas.LogoutIn.__module__ == oidc_schemas.__name__

    custom_operations = {
        AuthSession: ("login",),
        TokenRecord: ("token", "refresh", "introspect"),
        ClientRegistration: ("register", "register_put"),
        DeviceCode: ("device_authorization",),
        PushedAuthorizationRequest: ("par",),
        RevokedToken: ("revoke",),
        LogoutState: ("logout",),
    }
    for table, operation_names in custom_operations.items():
        for operation_name in operation_names:
            assert not hasattr(table.schemas, operation_name)

    storage_modules = (
        "auth_session",
        "client_registration",
        "device_code",
        "logout_state",
        "pushed_authorization_request",
        "revoked_token",
        "token_record",
    )
    forbidden_schema_names = set(oauth_schemas.__all__) | set(oidc_schemas.__all__) | {"CredsIn"}
    for module_name in storage_modules:
        module = importlib.import_module(f"tigrbl_identity_storage.tables.{module_name}")
        assert forbidden_schema_names.isdisjoint(vars(module))


def test_admin_auth_schemas_are_owned_by_the_server_runtime() -> None:
    from tigrbl_identity_server import admin_auth
    from tigrbl_identity_storage.tables import User
    from tigrbl_identity_storage.tables import user as storage_user

    assert admin_auth.CredsIn.__module__ == admin_auth.__name__
    assert admin_auth.AdminSessionOut.__module__ == admin_auth.__name__
    assert not hasattr(storage_user, "CredsIn")
    assert not hasattr(storage_user, "AdminSessionOut")
    assert not hasattr(User.schemas, "admin_login")
    assert not hasattr(User.schemas, "admin_session")


def test_storage_tables_export_table_inventory_without_schema_namespaces() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    auth_tables = importlib.import_module("tigrbl_auth.tables")

    assert storage_tables.Role in storage_tables.TABLE_MODELS
    assert storage_tables.TABLE_MODEL_BY_NAME["Role"] is storage_tables.Role
    assert storage_tables.TABLE_MODEL_BY_TABLENAME["roles"] is storage_tables.Role
    assert auth_tables.Role is storage_tables.Role
    assert auth_tables.TABLE_MODELS is storage_tables.TABLE_MODELS

    assert "RoleSchemas" not in storage_tables.__all__
    assert "UserSchemas" not in storage_tables.__all__
    assert "DelegationGrantRecordSchemas" not in storage_tables.__all__
    assert "RoleCreateRequest" not in storage_tables.__all__

    with pytest.raises(ImportError):
        exec("from tigrbl_identity_storage.tables import RoleSchemas", {})


def test_storage_package_has_no_openapi_schema_registry() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.schemas") is None
    assert importlib.util.find_spec("tigrbl_identity_storage.schema_registry") is None


def test_protocol_schema_owner_covers_mounted_token_component() -> None:
    from tigrbl_auth_protocol_oauth.schemas import TokenPair
    from tigrbl_identity_runtime.deployment import resolve_deployment
    from tigrbl_identity_server.surfaces import build_public_router

    surface_api = build_public_router(
        deployment=resolve_deployment(plugin_mode="mixed")
    )

    component_names = set(surface_api.openapi().get("components", {}).get("schemas", {}))
    assert "AdminSessionOut" in component_names
    assert TokenPair.__name__ in component_names


def test_storage_package_does_not_import_identity_contract_schemas() -> None:
    offenders = []
    for path in STORAGE_SRC.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if "tigrbl_identity_contracts" in source:
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_storage_package_metadata_does_not_depend_on_higher_layers() -> None:
    pyproject = ROOT / "pkgs" / "01-storage" / "tigrbl-identity-storage" / "pyproject.toml"
    source = pyproject.read_text(encoding="utf-8")

    assert "tigrbl-authz-resource-server" not in source
    assert "tigrbl-identity-contracts" not in source
    assert "tigrbl-identity-storage-runtime" not in source


def test_storage_does_not_define_a_parallel_directional_schema_helper() -> None:
    offenders = []
    forbidden = ("class DirectionalSchema", "DirectionalSchema(")
    for path in STORAGE_SRC.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if any(token in source for token in forbidden):
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_storage_table_helpers_are_nested_under_table_owners() -> None:
    tables_root = STORAGE_SRC / "tables"
    flat_helper_prefixes = (
        "_account",
        "_auth_flows",
        "_auth_session",
        "_authz",
        "_device_code",
        "_logout_state",
        "_oauth",
        "_oidc",
        "_resource_validation",
        "_rp",
        "_user",
    )
    offenders = [
        path.relative_to(ROOT).as_posix()
        for path in tables_root.glob("_*.py")
        if path.name != "_ops.py"
        and path.name.startswith(flat_helper_prefixes)
    ]

    assert offenders == []
