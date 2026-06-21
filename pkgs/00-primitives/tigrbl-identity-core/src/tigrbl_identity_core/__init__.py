"""Core identity primitives for the Tigrbl identity package suite."""

from __future__ import annotations

from .base64url import base64url_decode, base64url_encode
from .clock import Clock, FrozenClock, SystemClock, unix_seconds, utc_now, utc_now_iso
from .errors import (
    IdentityAuthorizationError,
    IdentityConfigurationError,
    IdentityError,
    IdentityValidationError,
    InvalidKeyError,
    InvalidTokenError,
)
from .liveness import ConvergenceEvent, ConvergenceState, LivenessConvergenceReport
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
from .standards import StandardOwner, describe_owner
from .json_canonicalization import canonical_json_bytes, canonicalize
from .normalization import normal_tuple
from .typing import JWTPayload, Principal, StrUUID, uuid_str
from .versions import semver_key, version_in_range

__all__ = [
    "Audience",
    "Clock",
    "ClientId",
    "ClientRef",
    "ConvergenceEvent",
    "ConvergenceState",
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
    "LivenessConvergenceReport",
    "Principal",
    "PrincipalId",
    "PrincipalRef",
    "RealmId",
    "RealmRef",
    "Scope",
    "ScopeValue",
    "StandardOwner",
    "StrUUID",
    "Subject",
    "SystemClock",
    "TenantId",
    "TenantRef",
    "base64url_decode",
    "base64url_encode",
    "canonicalize",
    "canonical_json_bytes",
    "describe_owner",
    "normal_tuple",
    "safe_display_path",
    "sanitize_local_paths",
    "new_client_id",
    "new_credential_id",
    "new_principal_id",
    "new_realm_id",
    "new_tenant_id",
    "unix_seconds",
    "utc_now",
    "utc_now_iso",
    "uuid_str",
    "semver_key",
    "version_in_range",
]
