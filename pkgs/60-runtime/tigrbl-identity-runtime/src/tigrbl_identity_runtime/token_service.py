"""Runtime token-service composition across provider and storage packages."""

from __future__ import annotations

from tigrbl_identity_contracts.tokens import (
    DEFAULT_ACCESS_TOKEN_TTL,
    DEFAULT_REFRESH_TOKEN_TTL,
    InvalidRefreshTokenError,
    RefreshTokenError,
    RefreshTokenReuseError,
)
from tigrbl_identity_jose.jwt_coder import InvalidTokenError, JWTCoder
from tigrbl_identity_jose.jwt_runtime import (
    _ACCESS_TTL,
    _REFRESH_TTL,
    _header_alg,
    _load_runtime,
    _run,
    _svc,
    _svc_async,
)
from tigrbl_identity_storage_runtime.session_service import (
    exchange_token_for_context,
    get_token_for_context,
    introspect_token_for_context,
    list_tokens_for_context,
    revoke_all_tokens_for_context,
    revoke_token_for_context,
)
from tigrbl_identity_storage.tables.token_record._op import (
    TokenCoder,
    issue_persisted_token_pair,
    redeem_refresh_token,
)

__all__ = [
    "DEFAULT_ACCESS_TOKEN_TTL",
    "DEFAULT_REFRESH_TOKEN_TTL",
    "InvalidRefreshTokenError",
    "InvalidTokenError",
    "JWTCoder",
    "RefreshTokenError",
    "RefreshTokenReuseError",
    "TokenCoder",
    "exchange_token_for_context",
    "get_token_for_context",
    "introspect_token_for_context",
    "issue_persisted_token_pair",
    "list_tokens_for_context",
    "redeem_refresh_token",
    "revoke_all_tokens_for_context",
    "revoke_token_for_context",
    "_ACCESS_TTL",
    "_REFRESH_TTL",
    "_header_alg",
    "_load_runtime",
    "_run",
    "_svc",
    "_svc_async",
]
