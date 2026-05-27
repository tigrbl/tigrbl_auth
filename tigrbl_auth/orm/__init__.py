"""Compatibility facade for canonical identity storage ORM imports."""

from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.orm import (
    ENGINE,
    Base,
    ApiKey,
    AuditEvent,
    AuthCode,
    AuthSession,
    Client,
    ClientRegistration,
    Consent,
    DeviceCode,
    KeyRotationEvent,
    LogoutState,
    PushedAuthorizationRequest,
    RevokedToken,
    Service,
    ServiceKey,
    Tenant,
    TokenRecord,
    User,
    _CLIENT_ID_RE,
    dsn,
    get_db,
    settings,
)

__all__ = [
    "ENGINE",
    "Base",
    "ApiKey",
    "AuditEvent",
    "AuthCode",
    "AuthSession",
    "Client",
    "ClientRegistration",
    "Consent",
    "DeviceCode",
    "KeyRotationEvent",
    "LogoutState",
    "PushedAuthorizationRequest",
    "RevokedToken",
    "Service",
    "ServiceKey",
    "Tenant",
    "TokenRecord",
    "User",
    "_CLIENT_ID_RE",
    "dsn",
    "get_db",
    "settings",
]
