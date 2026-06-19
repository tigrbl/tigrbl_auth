from __future__ import annotations

"""OpenID Connect Back-Channel Logout planning and durable completion tracking."""

import base64
import hashlib
import hmac
import json
import threading
from datetime import datetime, timedelta, timezone
from typing import Any, Final
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from uuid import UUID, uuid4

from tigrbl_identity_runtime.settings import settings

STATUS: Final[str] = "backchannel-logout-fanout-runtime"
_BACKCHANNEL_EVENT: Final[str] = "http://schemas.openid.net/event/backchannel-logout"
_DEFAULT_MAX_RETRIES: Final[int] = 3
_ALLOWED_CLOCK_SKEW: Final[int] = 300




class _BackchannelReplayStore:
    def __init__(self) -> None:
        self._items: dict[str, datetime] = {}
        self._lock = threading.Lock()

    def _cleanup(self, now: datetime) -> None:
        for key in [item for item, expiry in self._items.items() if expiry <= now]:
            self._items.pop(key, None)

    def register(self, jti: str, *, exp: datetime, now: datetime) -> None:
        with self._lock:
            self._cleanup(now)
            if jti in self._items and self._items[jti] > now:
                raise ValueError("replayed logout token")
            self._items[jti] = exp

    def snapshot(self) -> dict[str, int]:
        now = datetime.now(timezone.utc)
        with self._lock:
            self._cleanup(now)
            return {"active_logout_jti": len(self._items)}


_REPLAY_STORE = _BackchannelReplayStore()

OWNER = StandardOwner(
    label="OIDC Back-Channel Logout",
    title="OpenID Connect Back-Channel Logout",
    runtime_status=STATUS,
    public_surface=("/logout",),
    notes=(
        "Back-channel logout planning is implementation-backed. Client registration metadata can declare "
        "backchannel_logout_uri and the module mints repository-owned logout tokens with replay protection, durable delivery state, and bounded retry metadata."
    ),
)


def _persistence():
    from tigrbl_identity_storage import persistence as persistence_module

    return persistence_module


def _jwt_coder_cls():
    from tigrbl_authn_credentials.token_service import JWTCoder

    return JWTCoder


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _encode_checkpoint_logout_token(claims: dict[str, Any]) -> str:
    header = {"alg": "HS256", "typ": "logout+jwt"}
    signing_input = ".".join(
        (
            _b64url(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")),
            _b64url(json.dumps(claims, separators=(",", ":"), sort_keys=True).encode("utf-8")),
        )
    )
    secret = str(getattr(settings, "jwt_secret", "capability-backchannel-secret")).encode("utf-8")
    signature = hmac.new(secret, signing_input.encode("ascii"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url(signature)}"


def _decode_checkpoint_logout_token(token: str) -> dict[str, Any]:
    parts = str(token).split(".")
    if len(parts) != 3:
        raise ValueError("malformed logout token")
    signing_input = f"{parts[0]}.{parts[1]}"
    secret = str(getattr(settings, "jwt_secret", "capability-backchannel-secret")).encode("utf-8")
    expected = hmac.new(secret, signing_input.encode("ascii"), hashlib.sha256).digest()
    if not hmac.compare_digest(expected, _b64url_decode(parts[2])):
        raise ValueError("logout token signature mismatch")
    payload = json.loads(_b64url_decode(parts[1]).decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("logout token payload malformed")
    return payload


async def _mint_logout_token(*, claims: dict[str, Any], issuer: str, audience: str) -> str:
    """Mint a self-contained logout token.

    Back-channel logout validation must remain functional in dependency-complete
    checkpoint environments even when the durable token-record tables are not
    initialized. The repository-owned checkpoint format is therefore the primary
    path for logout-token minting, with local HMAC signing plus replay tracking.
    """

    return _encode_checkpoint_logout_token(claims)


async def build_backchannel_descriptor(*, client_id: UUID, sid: str, sub: str, iss: str | None = None, logout_id: UUID | None = None) -> dict[str, object] | None:
    registration = await _persistence().get_client_registration_async(client_id)
    metadata = dict(getattr(registration, "registration_metadata", {}) or {})
    logout_uri = metadata.get("backchannel_logout_uri")
    if not logout_uri:
        return None
    include_sid = bool(metadata.get("backchannel_logout_session_required", True))
    issuer = iss or settings.issuer
    claims: dict[str, Any] = {
        "events": {_BACKCHANNEL_EVENT: {}},
        "jti": str(uuid4()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "iss": issuer,
        "aud": [str(client_id)],
        "sub": sub,
    }
    if include_sid:
        claims["sid"] = sid
    logout_token = await _mint_logout_token(claims=claims, issuer=issuer, audience=str(client_id))
    return {
        "client_id": str(client_id),
        "logout_uri": str(logout_uri),
        "logout_token": logout_token,
        "iss": issuer,
        "sid_included": include_sid,
        "sid": sid if include_sid else None,
        "logout_id": str(logout_id) if logout_id is not None else None,
        "delivery": {
            "channel": "backchannel",
            "status": "pending",
            "attempts": 0,
            "max_retries": _DEFAULT_MAX_RETRIES,
            "replay_protected": True,
        },
    }


async def validate_backchannel_logout_token(
    logout_token: str,
    *,
    client_id: UUID | str,
    issuer: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    effective_issuer = issuer or settings.issuer
    current = now or datetime.now(timezone.utc)
    try:
        claims = _decode_checkpoint_logout_token(logout_token)
    except Exception:
        jwt_coder = _jwt_coder_cls().default()
        claims = await jwt_coder.async_decode(logout_token, verify_exp=True, audience=str(client_id), issuer=effective_issuer)
    claims = dict(claims)
    if claims.get("iss") not in {None, effective_issuer}:
        raise ValueError("logout token issuer mismatch")
    events = claims.get("events")
    if not isinstance(events, dict) or _BACKCHANNEL_EVENT not in events:
        raise ValueError("logout token missing backchannel event")
    if "nonce" in claims:
        raise ValueError("logout token must not contain nonce")
    if not claims.get("sid") and not claims.get("sub"):
        raise ValueError("logout token requires sid or sub")
    audiences = claims.get("aud")
    if isinstance(audiences, str):
        audiences = [audiences]
    if str(client_id) not in [str(item) for item in list(audiences or [])]:
        raise ValueError("logout token audience mismatch")
    exp = claims.get("exp")
    if exp is not None:
        exp_dt = datetime.fromtimestamp(int(exp), tz=timezone.utc)
        if exp_dt <= current:
            raise ValueError("logout token expired")
    iat = claims.get("iat")
    if iat is not None and abs(int(current.timestamp()) - int(iat)) > _ALLOWED_CLOCK_SKEW + 300:
        raise ValueError("logout token stale")
    jti = str(claims.get("jti") or "").strip()
    if not jti:
        raise ValueError("logout token missing jti")
    expiry = datetime.fromtimestamp(int(exp), tz=timezone.utc) if exp is not None else current + timedelta(minutes=5)
    _REPLAY_STORE.register(jti, exp=expiry, now=current)
    return claims


async def mark_backchannel_complete(logout_id: UUID):
    return await _persistence().mark_logout_channel_async(logout_id, channel="backchannel", status="complete")


async def mark_backchannel_failed(logout_id: UUID, *, error: str | None = None, retry_after_seconds: int | None = None):
    return await _persistence().mark_logout_channel_async(
        logout_id,
        channel="backchannel",
        status="retryable_error",
        reason=error,
        retry_after_seconds=retry_after_seconds,
    )


def replay_store_snapshot() -> dict[str, int]:
    return _REPLAY_STORE.snapshot()


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        logout_token_validation_supported=True,
        replay_protection=True,
        delivery_state_persisted=True,
        retry_semantics_supported=True,
    )


__all__ = [
    "STATUS",
    "StandardOwner",
    "OWNER",
    "build_backchannel_descriptor",
    "mark_backchannel_complete",
    "mark_backchannel_failed",
    "replay_store_snapshot",
    "validate_backchannel_logout_token",
    "describe",
]
