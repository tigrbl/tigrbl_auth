from __future__ import annotations

import importlib
from pathlib import Path


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
        User,
    )
    from tigrbl_identity_storage.tables.auth_session import CredsIn, TokenPair as LoginTokenPair
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
    from tigrbl_identity_storage.tables.user import AdminSessionOut, CredsIn as AdminCredsIn

    assert AuthSession.schemas.login.in_ is CredsIn
    assert AuthSession.schemas.login.out is LoginTokenPair
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
    assert User.schemas.admin_login.in_ is AdminCredsIn
    assert User.schemas.admin_session.out is AdminSessionOut


def test_every_exported_storage_table_exports_bound_schema_namespace() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    auth_tables = importlib.import_module("tigrbl_auth.tables")

    schema_exports: list[str] = []
    for name in storage_tables.__all__:
        if name.endswith("Schemas"):
            continue
        exported = getattr(storage_tables, name)
        if getattr(exported, "__table__", None) is None:
            continue

        schema_name = f"{name}Schemas"
        schema_exports.append(schema_name)
        assert schema_name in storage_tables.__all__
        assert getattr(storage_tables, schema_name) is exported.schemas
        assert getattr(auth_tables, schema_name) is getattr(storage_tables, schema_name)

    assert "ServiceKeySchemas" in schema_exports
    assert "OperatorRecordSchemas" in schema_exports


def test_exported_schema_aliases_use_openapi_component_model_names() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")

    for name in storage_tables.__all__:
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
                schema_alias = getattr(storage_tables, schema_name)

                assert schema_name in storage_tables.__all__
                if schema_alias is not schema:
                    assert schema_alias.model_json_schema() == schema.model_json_schema()

    assert storage_tables.ServiceKeyCreateRequest is storage_tables.ServiceKey.schemas.create.in_
    assert storage_tables.OperatorRecordCreateRequest is storage_tables.OperatorRecord.schemas.create.in_


def test_table_schema_alias_exports_cover_router_openapi_components() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    from tigrbl_identity_runtime.deployment import resolve_deployment
    from tigrbl_identity_server.surfaces import build_public_router

    surface_api = build_public_router(
        deployment=resolve_deployment(plugin_mode="mixed")
    )

    component_names = set(surface_api.openapi().get("components", {}).get("schemas", {}))
    missing = sorted(name for name in component_names if not hasattr(storage_tables, name))

    assert missing == []
    assert storage_tables.ServiceKeyCreateRequest.__name__ in component_names
    assert storage_tables.TokenPair.__name__ in component_names


def test_storage_package_does_not_import_identity_contract_schemas() -> None:
    offenders = []
    for path in STORAGE_SRC.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        if "tigrbl_identity_contracts" in source:
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


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
