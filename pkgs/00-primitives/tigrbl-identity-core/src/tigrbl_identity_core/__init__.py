"""Core identity primitives for the Tigrbl identity package suite."""

from __future__ import annotations

from .base64url import base64url_decode, base64url_encode
from .clock import Clock, FrozenClock, SystemClock, parse_time, unix_seconds, utc_now, utc_now_iso
from .entity_keys import normalize_entity, tenant_key
from .digests import sha256_text_digest, token_hash
from .errors import (
    IdentityAuthorizationError,
    IdentityConfigurationError,
    IdentityError,
    IdentityValidationError,
    InvalidKeyError,
    InvalidRefreshTokenError,
    InvalidTokenError,
    RefreshTokenError,
    RefreshTokenReuseError,
)
from .path_safety import safe_display_path, sanitize_local_paths
from .http import headers_from_scope, json_response, read_http_body, replay_http_body
from .jsonrpc import jsonrpc_error
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
from .normalization import normal_tuple, pick_fields, row_active, row_value, str_tuple
from .patterns import matches_dotted_pattern
from .redaction import SECRET_FIELD_TOKENS, redact_sensitive_mapping
from .typing import StrUUID, uuid_str
from .versions import semver_key, version_in_range

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
    "InvalidRefreshTokenError",
    "InvalidTokenError",
    "Issuer",
    "parse_time",
    "PrincipalId",
    "PrincipalRef",
    "RealmId",
    "RealmRef",
    "Scope",
    "ScopeValue",
    "SECRET_FIELD_TOKENS",
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
    "headers_from_scope",
    "json_response",
    "jsonrpc_error",
    "matches_dotted_pattern",
    "normal_tuple",
    "normalize_entity",
    "pick_fields",
    "redact_sensitive_mapping",
    "RefreshTokenError",
    "RefreshTokenReuseError",
    "read_http_body",
    "replay_http_body",
    "row_active",
    "row_value",
    "safe_display_path",
    "sanitize_local_paths",
    "sha256_text_digest",
    "str_tuple",
    "new_client_id",
    "new_credential_id",
    "new_principal_id",
    "new_realm_id",
    "new_tenant_id",
    "tenant_key",
    "token_hash",
    "unix_seconds",
    "utc_now",
    "utc_now_iso",
    "uuid_str",
    "semver_key",
    "version_in_range",
]
