"""Persistence models and engine exports for the Tigrbl-native package tree."""

from tigrbl import bind

from tigrbl_identity_server.framework import Base, _install_local_handler_dict_compat
from tigrbl_identity_runtime.settings import settings

from .realm import Realm
from .tenant import Tenant
from .user import User
from .client import Client, _CLIENT_ID_RE
from .client_registration import ClientRegistration
from .service import Service
from .api_key import ApiKey
from .service_key import ServiceKey
from .auth_session import AuthSession
from .auth_code import AuthCode
from .device_code import DeviceCode
from .revoked_token import RevokedToken
from .token_record import TokenRecord
from .delegation_grant import (
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantRecord,
    DelegationGrantScope,
    DelegationGrantTokenLink,
)
from .pushed_authorization_request import PushedAuthorizationRequest
from .consent import Consent
from .audit_event import AuditEvent
from .logout_state import LogoutState
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


_ensure_runtime_bindings()

__all__ = [
    "Base",
    "settings",
    "ENGINE",
    "dsn",
    "get_db",
    "Tenant",
    "Realm",
    "User",
    "Client",
    "_CLIENT_ID_RE",
    "ClientRegistration",
    "Service",
    "ApiKey",
    "ServiceKey",
    "AuthSession",
    "AuthCode",
    "DeviceCode",
    "RevokedToken",
    "TokenRecord",
    "DelegationGrantEdge",
    "DelegationGrantProof",
    "DelegationGrantRecord",
    "DelegationGrantScope",
    "DelegationGrantTokenLink",
    "PushedAuthorizationRequest",
    "Consent",
    "AuditEvent",
    "LogoutState",
    "KeyRotationEvent",
]
