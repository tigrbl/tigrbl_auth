from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STORAGE_SRC = (
    ROOT
    / "pkgs"
    / "20-storage"
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

