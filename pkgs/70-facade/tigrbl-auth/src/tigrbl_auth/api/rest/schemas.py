"""Deprecated compatibility facade for table-owned REST schemas."""

from __future__ import annotations

import warnings

from tigrbl_identity_server.admin_auth import (
    AdminPasswordChangeIn,
    AdminPasswordResetCompleteIn,
    AdminPasswordResetRequestIn,
    AdminSessionOut,
    CredsIn,
)
from tigrbl_identity_storage.schemas import (
    AuthorizationCodeGrantForm,
    DeviceAuthorizationIn,
    DeviceAuthorizationOut,
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
    IntrospectOut,
    LogoutIn,
    LogoutOut,
    PasswordGrantForm,
    PushedAuthorizationRequestIn,
    PushedAuthorizationResponse,
    RefreshIn,
    RevocationIn,
    RevocationOut,
    TokenPair,
)

LoginTokenPair = TokenPair


warnings.warn(
    "tigrbl_auth.api.rest.schemas is deprecated; import REST schemas from the owning "
    "the owning API/runtime modules.",
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
