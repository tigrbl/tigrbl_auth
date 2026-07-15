"""OpenID Connect Session Management with durable browser-session handling.

This module deliberately keeps the session-management claim boundary truthful:
- durable browser sessions are persisted server-side
- ``session_state`` values are emitted and can be validated against client origins
- auth-code issuance is bound to the durable browser session
- cookie rotation / renewal / invalidation semantics are repository-owned
- a dedicated mounted ``check_session_iframe`` route is *not* currently claimed
  by discovery or contracts in this checkpoint
"""

from __future__ import annotations

from hashlib import sha256
from typing import Final

from tigrbl_identity_contracts.oidc import SessionStateValidation
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from urllib.parse import urlparse
from uuid import UUID

from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import ISSUER

STATUS: Final[str] = "browser-session-runtime"


OWNER = StandardOwner(
    label="OIDC Session Management",
    title="OpenID Connect Session Management",
    runtime_status=STATUS,
    public_surface=("/login", "/authorize", "/logout"),
    notes=(
        "Durable browser sessions own opaque session-cookie secrets, cookie rotation, "
        "client binding, auth-code linkage, and OIDC session_state generation + validation across "
        "client origins. This release path does not claim a mounted check_session_iframe endpoint, "
        "and discovery/contracts remain truthful about that omission."
    ),
)


def _origin(uri: str | None) -> str:
    if not uri:
        return ""
    parsed = urlparse(uri)
    host = parsed.hostname or ""
    port = f":{parsed.port}" if parsed.port else ""
    return f"{parsed.scheme}://{host}{port}" if parsed.scheme and host else uri


def session_client_origin(redirect_uri: str | None) -> str:
    return _origin(redirect_uri)


def compute_session_state(
    *,
    client_id: str,
    redirect_uri: str,
    session_id: UUID | str,
    salt: str,
    issuer: str | None = None,
) -> str:
    origin = _origin(redirect_uri)
    payload = f"{client_id} {origin} {session_id} {salt} {issuer or ISSUER}"
    return f"{sha256(payload.encode('utf-8')).hexdigest()}.{salt}"


def parse_session_state(value: str | None) -> tuple[str, str] | None:
    if not value or not isinstance(value, str):
        return None
    if "." not in value:
        return None
    digest, salt = value.rsplit(".", 1)
    if len(digest) != 64 or not salt:
        return None
    try:
        int(digest, 16)
    except Exception:
        return None
    return digest, salt


def validate_session_state(
    *,
    presented_session_state: str | None,
    client_id: str,
    redirect_uri: str,
    session_id: UUID | str,
    salt: str | None = None,
    expected_session_state: str | None = None,
    issuer: str | None = None,
) -> SessionStateValidation:
    origin = _origin(redirect_uri)
    parsed_presented = parse_session_state(presented_session_state)
    if parsed_presented is None:
        return SessionStateValidation(
            valid=False,
            reason="malformed_session_state",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=expected_session_state,
        )
    presented_digest, presented_salt = parsed_presented
    effective_salt = salt or presented_salt
    effective_expected = expected_session_state or compute_session_state(
        client_id=client_id,
        redirect_uri=redirect_uri,
        session_id=session_id,
        salt=effective_salt,
        issuer=issuer,
    )
    parsed_expected = parse_session_state(effective_expected)
    if parsed_expected is None:
        return SessionStateValidation(
            valid=False,
            reason="invalid_expected_session_state",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=effective_expected,
        )
    expected_digest, expected_salt = parsed_expected
    if presented_salt != expected_salt:
        return SessionStateValidation(
            valid=False,
            reason="salt_mismatch",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=effective_expected,
        )
    if presented_digest != expected_digest:
        return SessionStateValidation(
            valid=False,
            reason="hash_mismatch",
            origin=origin,
            presented_session_state=presented_session_state,
            expected_session_state=effective_expected,
        )
    return SessionStateValidation(
        valid=True,
        reason="validated",
        origin=origin,
        presented_session_state=presented_session_state,
        expected_session_state=effective_expected,
    )


def session_state_for_client(
    session_row,
    *,
    client_id: str,
    redirect_uri: str,
    deployment=None,
    issuer: str | None = None,
) -> str | None:
    if session_row is None:
        return None
    if deployment is None:
        raise TypeError("session_state_for_client requires an injected deployment")
    if not deployment.flag_enabled("enable_oidc_session_management"):
        return None
    salt = getattr(session_row, "session_state_salt", None)
    if not salt:
        return None
    return compute_session_state(
        client_id=client_id,
        redirect_uri=redirect_uri,
        session_id=session_row.id,
        salt=salt,
        issuer=issuer or getattr(deployment, "issuer", None),
    )


def validate_session_state_for_client(
    session_row,
    *,
    presented_session_state: str | None,
    client_id: str,
    redirect_uri: str,
    deployment=None,
    issuer: str | None = None,
) -> SessionStateValidation:
    if session_row is None:
        return SessionStateValidation(
            valid=False,
            reason="no_session",
            origin=_origin(redirect_uri),
            presented_session_state=presented_session_state,
            expected_session_state=None,
        )
    return validate_session_state(
        presented_session_state=presented_session_state,
        client_id=client_id,
        redirect_uri=redirect_uri,
        session_id=session_row.id,
        salt=getattr(session_row, "session_state_salt", None),
        issuer=issuer or getattr(deployment, "issuer", None),
    )


def describe(*, cross_site_logout_enabled: bool = True) -> dict[str, object]:
    return describe_owner(
        OWNER,
        session_state_validation_supported=True,
        session_state_origin_bound=True,
        auth_code_linkage_supported=True,
        check_session_iframe_claimed=False,
        cross_site_logout_enabled=cross_site_logout_enabled,
    )


__all__ = [
    "STATUS",
    "SessionStateValidation",
    "StandardOwner",
    "OWNER",
    "compute_session_state",
    "describe",
    "parse_session_state",
    "session_client_origin",
    "session_state_for_client",
    "validate_session_state",
    "validate_session_state_for_client",
]
