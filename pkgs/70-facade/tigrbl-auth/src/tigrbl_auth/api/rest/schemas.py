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
from tigrbl_auth_protocol_oauth.schemas import (
    AuthorizationCodeGrantForm,
    DeviceAuthorizationIn,
    DeviceAuthorizationOut,
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
    IntrospectOut,
    PasswordGrantForm,
    PushedAuthorizationRequestIn,
    PushedAuthorizationResponse,
    RefreshIn,
    RevocationIn,
    RevocationOut,
    TokenPair,
)
from tigrbl_auth_protocol_oidc.schemas import LogoutIn, LogoutOut

LoginTokenPair = TokenPair


warnings.warn(
    "tigrbl_auth.api.rest.schemas is deprecated; import wire schemas from the "
    "owning protocol or API package.",
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
