"""Persistence models and engine exports for the Tigrbl-native package tree."""

from types import SimpleNamespace

from tigrbl import bind

from tigrbl_identity_server.framework import Base, _install_local_handler_dict_compat
from tigrbl_identity_runtime.settings import settings

from .realm import AdminRealmOut, AdminRealmProvisionIn, AdminRealmUpdateIn, Realm
from .tenant import AdminTenantOut, AdminTenantProvisionIn, AdminTenantUpdateIn, Tenant
from .user import (
    AdminIdentityOut,
    AdminIdentityProvisionIn,
    AdminIdentityUpdateIn,
    AdminPasswordChangeIn,
    AdminPasswordResetCompleteIn,
    AdminPasswordResetRequestIn,
    AdminSessionOut,
    CredsIn as AdminCredsIn,
    MyAccountMutationOut,
    MyAccountPasswordChangeIn,
    MyAccountProfileOut,
    MyAccountProfileUpdateIn,
    User,
)
from .client import Client, _CLIENT_ID_RE
from .client_registration import (
    ClientRegistration,
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
)
from .service import Service
from .api_key import ApiKey
from .service_key import ServiceKey
from .auth_session import AuthSession, CredsIn, MyAccountSessionOut, TokenPair as LoginTokenPair
from .auth_code import AuthCode
from .device_code import DeviceAuthorizationIn, DeviceAuthorizationOut, DeviceCode
from .revoked_token import RevocationIn, RevocationOut, RevokedToken
from .token_record import (
    AuthorizationCodeGrantForm,
    IntrospectOut,
    PasswordGrantForm,
    RefreshIn,
    TokenPair,
    TokenRecord,
)
from .delegation_grant import (
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantRecord,
    DelegationGrantScope,
    DelegationGrantTokenLink,
)
from .pushed_authorization_request import (
    PushedAuthorizationRequest,
    PushedAuthorizationRequestIn,
    PushedAuthorizationResponse,
)
from .consent import Consent, MyAccountAuthorizedAppOut, MyAccountConsentOut
from .audit_event import AuditEvent
from .logout_state import LogoutIn, LogoutOut, LogoutState
from .key_rotation_event import KeyRotationEvent
from .engine import ENGINE, dsn, get_db


def _ensure_runtime_bindings() -> None:
    """Materialize model handlers/schemas through Tigrbl's public bind API."""

    for model in (
        Realm,
        Tenant,
        User,
        Client,
        ClientRegistration,
        Service,
        ApiKey,
        ServiceKey,
        AuthSession,
        AuthCode,
        DeviceCode,
        RevokedToken,
        TokenRecord,
        DelegationGrantRecord,
        DelegationGrantScope,
        DelegationGrantProof,
        DelegationGrantEdge,
        DelegationGrantTokenLink,
        PushedAuthorizationRequest,
        Consent,
        AuditEvent,
        LogoutState,
        KeyRotationEvent,
    ):
        handlers = getattr(model, "handlers", None)
        if getattr(handlers, "read", None) is None:
            bind(model)
        _install_local_handler_dict_compat(model)


def _set_schema(model: type, op_name: str, *, in_: object | None = None, out: object | None = None) -> None:
    schemas = getattr(model, "schemas", None)
    if schemas is None:
        schemas = SimpleNamespace()
        setattr(model, "schemas", schemas)
    setattr(schemas, op_name, SimpleNamespace(in_=in_, out=out))


def _attach_custom_op_schemas() -> None:
    _set_schema(AuthSession, "login", in_=CredsIn, out=LoginTokenPair)
    _set_schema(AuthSession, "list_account_sessions", out=list[MyAccountSessionOut])
    _set_schema(AuthSession, "revoke_account_session", out=MyAccountMutationOut)

    _set_schema(TokenRecord, "token", in_=None, out=TokenPair)
    _set_schema(TokenRecord, "authorization_code_grant", in_=AuthorizationCodeGrantForm, out=TokenPair)
    _set_schema(TokenRecord, "password_grant", in_=PasswordGrantForm, out=TokenPair)
    _set_schema(TokenRecord, "refresh", in_=RefreshIn, out=TokenPair)
    _set_schema(TokenRecord, "introspect", out=IntrospectOut)

    _set_schema(ClientRegistration, "register", in_=DynamicClientRegistrationIn, out=DynamicClientRegistrationOut)
    _set_schema(ClientRegistration, "register_get", out=DynamicClientRegistrationOut)
    _set_schema(
        ClientRegistration,
        "register_put",
        in_=DynamicClientRegistrationManagementIn,
        out=DynamicClientRegistrationOut,
    )
    _set_schema(ClientRegistration, "register_delete", out=dict)

    _set_schema(DeviceCode, "device_authorization", in_=DeviceAuthorizationIn, out=DeviceAuthorizationOut)
    _set_schema(PushedAuthorizationRequest, "par", in_=PushedAuthorizationRequestIn, out=PushedAuthorizationResponse)
    _set_schema(RevokedToken, "revoke", in_=RevocationIn, out=RevocationOut)
    _set_schema(LogoutState, "logout", in_=LogoutIn, out=LogoutOut)

    _set_schema(User, "admin_login", in_=AdminCredsIn, out=AdminSessionOut)
    _set_schema(User, "admin_session", out=AdminSessionOut)
    _set_schema(User, "admin_logout", out=AdminSessionOut)
    _set_schema(User, "admin_forgot_password", in_=AdminPasswordResetRequestIn, out=AdminSessionOut)
    _set_schema(User, "admin_reset_password", in_=AdminPasswordResetCompleteIn, out=AdminSessionOut)
    _set_schema(User, "admin_change_password", in_=AdminPasswordChangeIn, out=AdminSessionOut)
    _set_schema(User, "admin_create_identity", in_=AdminIdentityProvisionIn, out=AdminIdentityOut)
    _set_schema(User, "admin_update_identity", in_=AdminIdentityUpdateIn, out=AdminIdentityOut)
    _set_schema(User, "admin_delete_identity", out=AdminIdentityOut)
    _set_schema(User, "get_account_profile", out=MyAccountProfileOut)
    _set_schema(User, "update_account_profile", in_=MyAccountProfileUpdateIn, out=MyAccountProfileOut)
    _set_schema(User, "change_account_password", in_=MyAccountPasswordChangeIn, out=MyAccountMutationOut)

    _set_schema(Tenant, "admin_create_tenant", in_=AdminTenantProvisionIn, out=AdminTenantOut)
    _set_schema(Tenant, "admin_update_tenant", in_=AdminTenantUpdateIn, out=AdminTenantOut)
    _set_schema(Tenant, "admin_delete_tenant", out=AdminTenantOut)
    _set_schema(Realm, "admin_create_realm", in_=AdminRealmProvisionIn, out=AdminRealmOut)
    _set_schema(Realm, "admin_update_realm", in_=AdminRealmUpdateIn, out=AdminRealmOut)
    _set_schema(Realm, "admin_delete_realm", out=AdminRealmOut)


_ensure_runtime_bindings()
_attach_custom_op_schemas()

__all__ = [
    "Base",
    "settings",
    "ENGINE",
    "dsn",
    "get_db",
    "Tenant",
    "AdminTenantOut",
    "AdminTenantProvisionIn",
    "AdminTenantUpdateIn",
    "Realm",
    "AdminRealmOut",
    "AdminRealmProvisionIn",
    "AdminRealmUpdateIn",
    "User",
    "AdminIdentityOut",
    "AdminIdentityProvisionIn",
    "AdminIdentityUpdateIn",
    "AdminPasswordChangeIn",
    "AdminPasswordResetCompleteIn",
    "AdminPasswordResetRequestIn",
    "AdminSessionOut",
    "MyAccountMutationOut",
    "MyAccountPasswordChangeIn",
    "MyAccountProfileOut",
    "MyAccountProfileUpdateIn",
    "Client",
    "_CLIENT_ID_RE",
    "ClientRegistration",
    "DynamicClientRegistrationIn",
    "DynamicClientRegistrationManagementIn",
    "DynamicClientRegistrationOut",
    "Service",
    "ApiKey",
    "ServiceKey",
    "AuthSession",
    "CredsIn",
    "MyAccountSessionOut",
    "LoginTokenPair",
    "AuthCode",
    "DeviceCode",
    "DeviceAuthorizationIn",
    "DeviceAuthorizationOut",
    "RevokedToken",
    "RevocationIn",
    "RevocationOut",
    "TokenRecord",
    "AuthorizationCodeGrantForm",
    "IntrospectOut",
    "PasswordGrantForm",
    "RefreshIn",
    "TokenPair",
    "DelegationGrantEdge",
    "DelegationGrantProof",
    "DelegationGrantRecord",
    "DelegationGrantScope",
    "DelegationGrantTokenLink",
    "PushedAuthorizationRequest",
    "PushedAuthorizationRequestIn",
    "PushedAuthorizationResponse",
    "Consent",
    "MyAccountAuthorizedAppOut",
    "MyAccountConsentOut",
    "AuditEvent",
    "LogoutState",
    "LogoutIn",
    "LogoutOut",
    "KeyRotationEvent",
]
