from __future__ import annotations

import importlib
from types import SimpleNamespace
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


def test_custom_op_schemas_are_reachable_from_tigrbl_table_schema_namespace() -> None:
    from tigrbl_identity_storage.tables import (
        AuthSession,
        ClientRegistration,
        DeviceCode,
        LogoutState,
        PushedAuthorizationRequest,
        RevokedToken,
        TokenRecord,
    )
    from tigrbl_identity_storage.tables.client_registration import (
        DynamicClientRegistrationIn,
        DynamicClientRegistrationManagementIn,
        DynamicClientRegistrationOut,
    )
    from tigrbl_identity_storage.tables.device_code import DeviceAuthorizationIn, DeviceAuthorizationOut
    from tigrbl_identity_storage.tables.logout_state import LogoutIn, LogoutOut
    from tigrbl_identity_storage.tables.pushed_authorization_request import (
        PushedAuthorizationRequestIn,
        PushedAuthorizationResponse,
    )
    from tigrbl_identity_storage.tables.revoked_token import RevocationIn, RevocationOut
    from tigrbl_identity_storage.tables.token_record import (
        IntrospectOut,
        RefreshIn,
        TokenPair,
    )
    from tigrbl_identity_storage.tables.auth_session import CredsIn, TokenPair as LoginTokenPair
    from tigrbl_identity_storage_runtime.login import login

    assert not hasattr(AuthSession.schemas, "login")
    assert CredsIn.__name__ == "CredsIn"
    assert "CredsIn" in str(login.__annotations__.get("creds"))
    assert LoginTokenPair.__name__ == "TokenPair"
    assert TokenRecord.schemas.token.out is TokenPair
    assert TokenRecord.schemas.refresh.in_ is RefreshIn
    assert TokenRecord.schemas.introspect.out is IntrospectOut
    assert ClientRegistration.schemas.register.in_ is DynamicClientRegistrationIn
    assert ClientRegistration.schemas.register.out is DynamicClientRegistrationOut
    assert ClientRegistration.schemas.register_put.in_ is DynamicClientRegistrationManagementIn
    assert DeviceCode.schemas.device_authorization.in_ is DeviceAuthorizationIn
    assert DeviceCode.schemas.device_authorization.out is DeviceAuthorizationOut
    assert PushedAuthorizationRequest.schemas.par.in_ is PushedAuthorizationRequestIn
    assert PushedAuthorizationRequest.schemas.par.out is PushedAuthorizationResponse
    assert RevokedToken.schemas.revoke.in_ is RevocationIn
    assert RevokedToken.schemas.revoke.out is RevocationOut
    assert LogoutState.schemas.logout.in_ is LogoutIn
    assert LogoutState.schemas.logout.out is LogoutOut


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


def test_storage_schema_module_exports_openapi_component_model_names() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    storage_schemas = importlib.import_module("tigrbl_identity_storage.schemas")
    schema_registry = importlib.import_module("tigrbl_identity_storage.schema_registry")

    for name in storage_tables.TABLE_MODEL_BY_NAME:
        exported = getattr(storage_tables, name)
        if getattr(exported, "__table__", None) is None:
            continue
        for op_name in dir(exported.schemas):
            if op_name.startswith("_"):
                continue
            op_schema = getattr(exported.schemas, op_name)
            for direction in ("in_", "out"):
                schema = getattr(op_schema, direction, None)
                if schema is None or not hasattr(schema, "model_json_schema"):
                    continue
                schema_name = schema.__name__
                schema_alias = getattr(storage_schemas, schema_name)

                assert schema_name in storage_schemas.__all__
                assert schema_registry.OPENAPI_SCHEMA_REGISTRY[schema_name] is schema_alias
                assert (
                    schema_registry.TABLE_SCHEMA_BINDINGS[(name, op_name, direction.removesuffix("_"))]
                    is schema
                )
                assert schema_alias.model_json_schema() == schema.model_json_schema()

    assert storage_schemas.RoleCreateRequest is storage_tables.Role.schemas.create.in_
    assert storage_schemas.CredentialServiceKeyCreateRequest is storage_tables.CredentialServiceKey.schemas.create.in_
    assert storage_schemas.OperatorRecordCreateRequest is storage_tables.OperatorRecord.schemas.create.in_


def test_table_schema_alias_exports_cover_router_openapi_components() -> None:
    storage_schemas = importlib.import_module("tigrbl_identity_storage.schemas")
    from tigrbl_identity_runtime.deployment import resolve_deployment
    from tigrbl_identity_server.surfaces import build_public_router

    surface_api = build_public_router(
        deployment=resolve_deployment(plugin_mode="mixed")
    )

    component_names = set(surface_api.openapi().get("components", {}).get("schemas", {}))
    external_api_components = {"AdminSessionOut"}
    missing = sorted(
        name
        for name in component_names
        if not hasattr(storage_schemas, name) and name not in external_api_components
    )

    assert missing == []
    assert "AdminSessionOut" in component_names
    assert storage_schemas.CredentialServiceKeyCreateRequest.__name__ in component_names
    assert storage_schemas.TokenPair.__name__ in component_names


def test_schema_registry_rejects_conflicting_duplicate_openapi_names() -> None:
    from tigrbl_identity_storage.schema_registry import (
        SchemaRegistryError,
        _build_schema_indexes,
    )

    DuplicateA = type(
        "DuplicateSchema",
        (),
        {"model_json_schema": classmethod(lambda cls: {"title": "DuplicateSchema", "type": "object"})},
    )
    DuplicateB = type(
        "DuplicateSchema",
        (),
        {"model_json_schema": classmethod(lambda cls: {"title": "DuplicateSchema", "type": "string"})},
    )
    FakeTable = type(
        "FakeTable",
        (),
        {"schemas": SimpleNamespace(create=SimpleNamespace(in_=DuplicateA, out=DuplicateB))},
    )

    with pytest.raises(SchemaRegistryError):
        _build_schema_indexes((FakeTable,))


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
        and path.name != "_schema_ctx.py"
        and path.name.startswith(flat_helper_prefixes)
    ]

    assert offenders == []
