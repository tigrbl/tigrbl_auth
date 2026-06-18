"""Core identity primitives for the Tigrbl identity package suite."""

from __future__ import annotations

from .clock import Clock, FrozenClock, SystemClock, unix_seconds
from .errors import (
    IdentityAuthorizationError,
    IdentityConfigurationError,
    IdentityError,
    IdentityValidationError,
    InvalidKeyError,
    InvalidTokenError,
)
from .path_safety import safe_display_path, sanitize_local_paths
from .primitives import (
    Audience,
    ClientId,
    ClientRef,
    CredentialId,
    Issuer,
    PrincipalId,
    PrincipalRef,
    RealmId,
    RealmRef,
    Scope,
    ScopeValue,
    Subject,
    TenantId,
    TenantRef,
    new_client_id,
    new_credential_id,
    new_principal_id,
    new_realm_id,
    new_tenant_id,
)
from .json_canonicalization import canonicalize
from .typing import JWTPayload, Principal, StrUUID, uuid_str

__all__ = [
    "Audience",
    "Clock",
    "ClientId",
    "ClientRef",
    "CredentialId",
    "FrozenClock",
    "IdentityAuthorizationError",
    "IdentityConfigurationError",
    "IdentityError",
    "IdentityValidationError",
    "InvalidKeyError",
    "InvalidTokenError",
    "Issuer",
    "JWTPayload",
    "Principal",
    "PrincipalId",
    "PrincipalRef",
    "RealmId",
    "RealmRef",
    "Scope",
    "ScopeValue",
    "StrUUID",
    "Subject",
    "SystemClock",
    "TenantId",
    "TenantRef",
    "canonicalize",
    "safe_display_path",
    "sanitize_local_paths",
    "new_client_id",
    "new_credential_id",
    "new_principal_id",
    "new_realm_id",
    "new_tenant_id",
    "unix_seconds",
    "uuid_str",
]
