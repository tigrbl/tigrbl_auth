"""Persistence models and engine exports for the Tigrbl-native package tree."""

from tigrbl import bind

from tigrbl_identity_storage.framework import Base, _install_local_handler_dict_compat
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
from ._schema_ctx import set_schema


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


def _attach_custom_op_schemas() -> None:
    set_schema(AuthSession, "login", in_=CredsIn, out=LoginTokenPair)
    set_schema(AuthSession, "list_account_sessions", out=list[MyAccountSessionOut])
    set_schema(AuthSession, "revoke_account_session", out=MyAccountMutationOut)

    set_schema(TokenRecord, "token", in_=None, out=TokenPair)
    set_schema(TokenRecord, "authorization_code_grant", in_=AuthorizationCodeGrantForm, out=TokenPair)
    set_schema(TokenRecord, "password_grant", in_=PasswordGrantForm, out=TokenPair)
    set_schema(TokenRecord, "refresh", in_=RefreshIn, out=TokenPair)
    set_schema(TokenRecord, "introspect", out=IntrospectOut)

    set_schema(ClientRegistration, "register", in_=DynamicClientRegistrationIn, out=DynamicClientRegistrationOut)
    set_schema(ClientRegistration, "register_get", out=DynamicClientRegistrationOut)
    set_schema(
        ClientRegistration,
        "register_put",
        in_=DynamicClientRegistrationManagementIn,
        out=DynamicClientRegistrationOut,
    )
    set_schema(ClientRegistration, "register_delete", out=dict)

    set_schema(DeviceCode, "device_authorization", in_=DeviceAuthorizationIn, out=DeviceAuthorizationOut)
    set_schema(PushedAuthorizationRequest, "par", in_=PushedAuthorizationRequestIn, out=PushedAuthorizationResponse)
    set_schema(RevokedToken, "revoke", in_=RevocationIn, out=RevocationOut)
    set_schema(LogoutState, "logout", in_=LogoutIn, out=LogoutOut)

    set_schema(User, "admin_login", in_=AdminCredsIn, out=AdminSessionOut)
    set_schema(User, "admin_session", out=AdminSessionOut)
    set_schema(User, "admin_logout", out=AdminSessionOut)
    set_schema(User, "admin_forgot_password", in_=AdminPasswordResetRequestIn, out=AdminSessionOut)
    set_schema(User, "admin_reset_password", in_=AdminPasswordResetCompleteIn, out=AdminSessionOut)
    set_schema(User, "admin_change_password", in_=AdminPasswordChangeIn, out=AdminSessionOut)
    set_schema(User, "admin_create_identity", in_=AdminIdentityProvisionIn, out=AdminIdentityOut)
    set_schema(User, "admin_update_identity", in_=AdminIdentityUpdateIn, out=AdminIdentityOut)
    set_schema(User, "admin_delete_identity", out=AdminIdentityOut)
    set_schema(User, "get_account_profile", out=MyAccountProfileOut)
    set_schema(User, "update_account_profile", in_=MyAccountProfileUpdateIn, out=MyAccountProfileOut)
    set_schema(User, "change_account_password", in_=MyAccountPasswordChangeIn, out=MyAccountMutationOut)

    set_schema(Tenant, "admin_create_tenant", in_=AdminTenantProvisionIn, out=AdminTenantOut)
    set_schema(Tenant, "admin_update_tenant", in_=AdminTenantUpdateIn, out=AdminTenantOut)
    set_schema(Tenant, "admin_delete_tenant", out=AdminTenantOut)
    set_schema(Realm, "admin_create_realm", in_=AdminRealmProvisionIn, out=AdminRealmOut)
    set_schema(Realm, "admin_update_realm", in_=AdminRealmUpdateIn, out=AdminRealmOut)
    set_schema(Realm, "admin_delete_realm", out=AdminRealmOut)


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
