"""Deprecated compatibility facade for table-owned REST schemas."""

from __future__ import annotations

import warnings

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
    AuthorizationCodeGrantForm,
    IntrospectOut,
    PasswordGrantForm,
    RefreshIn,
    TokenPair,
)
from tigrbl_identity_storage.tables.user import (
    AdminPasswordChangeIn,
    AdminPasswordResetCompleteIn,
    AdminPasswordResetRequestIn,
    AdminSessionOut,
)


warnings.warn(
    "tigrbl_auth.api.rest.schemas is deprecated; import REST schemas from the owning "
    "tigrbl_identity_storage table module and access custom op schemas via "
    "<Table>.schemas.<op>.in_ or <Table>.schemas.<op>.out.",
    DeprecationWarning,
    stacklevel=2,
)


__all__ = [
    "AdminPasswordChangeIn",
    "AdminPasswordResetCompleteIn",
    "AdminPasswordResetRequestIn",
    "AdminSessionOut",
    "AuthorizationCodeGrantForm",
    "CredsIn",
    "DeviceAuthorizationIn",
    "DeviceAuthorizationOut",
    "DynamicClientRegistrationIn",
    "DynamicClientRegistrationManagementIn",
    "DynamicClientRegistrationOut",
    "IntrospectOut",
    "LoginTokenPair",
    "LogoutIn",
    "LogoutOut",
    "PasswordGrantForm",
    "PushedAuthorizationRequestIn",
    "PushedAuthorizationResponse",
    "RefreshIn",
    "RevocationIn",
    "RevocationOut",
    "TokenPair",
]
