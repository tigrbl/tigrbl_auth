"""OAuth 2.0 Device Authorization Grant owner and helper module."""

from __future__ import annotations

import re
import secrets
import string
from datetime import datetime, timezone
from typing import Final, Literal
from tigrbl_identity_core.standards import StandardOwner, describe_owner

from tigrbl_identity_runtime.settings import settings

try:  # pragma: no cover - exercised when full runtime deps are installed
    from tigrbl.types import BaseModel
except Exception:  # pragma: no cover - dependency-light fallback for checkpoint tests/evidence
    from pydantic import BaseModel


STATUS: Final[str] = "persistence-backed-device-flow-runtime"
RFC8628_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc8628"
DEVICE_VERIFICATION_URI: Final[str] = "https://example.com/device"
DEVICE_CODE_GRANT_TYPE: Final[str] = "urn:ietf:params:oauth:grant-type:device_code"
DEVICE_CODE_EXPIRES_IN: Final[int] = 600
DEVICE_CODE_INTERVAL: Final[int] = 5
DEVICE_CODE_SLOW_DOWN_INCREMENT: Final[int] = 5
_USER_CODE_CHARSET: Final[str] = string.ascii_uppercase + string.digits
_USER_CODE_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Z0-9]{8,}$")




OWNER = StandardOwner(
    label="RFC 8628",
    title="OAuth 2.0 Device Authorization Grant",
    runtime_status=STATUS,
    public_surface=("/device_authorization", "/token"),
    notes=(
        "Canonical standards-tree owner module for device-code lifecycle helpers. "
        "The canonical /device_authorization and /token grant path are now "
        "persistence-backed with authorization_pending / slow_down / access_denied / "
        "expired_token semantics, replay protection, and audit-observable approval/denial state."
    ),
)


class DeviceAuthIn(BaseModel):
    client_id: str
    scope: str | None = None


class DeviceAuthOut(BaseModel):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


class DeviceGrantForm(BaseModel):
    grant_type: Literal["urn:ietf:params:oauth:grant-type:device_code"]
    device_code: str
    client_id: str




def generate_user_code(length: int = 8) -> str:
    if length <= 0:
        raise ValueError("length must be positive")
    return "".join(secrets.choice(_USER_CODE_CHARSET) for _ in range(length))



def validate_user_code(code: str) -> bool:
    if not settings.enable_rfc8628:
        return True
    return bool(_USER_CODE_RE.fullmatch(code))



def generate_device_code() -> str:
    return secrets.token_urlsafe(32)



def next_device_poll_interval(current_interval: int | None = None, *, slow_down_count: int = 0) -> int:
    base = max(int(current_interval or DEVICE_CODE_INTERVAL), DEVICE_CODE_INTERVAL)
    if slow_down_count <= 0:
        return base
    return base + (DEVICE_CODE_SLOW_DOWN_INCREMENT * int(slow_down_count))



def poll_too_frequently(*, last_polled_at: datetime | None, now: datetime, interval: int | None = None) -> bool:
    if last_polled_at is None:
        return False
    effective_interval = max(int(interval or DEVICE_CODE_INTERVAL), DEVICE_CODE_INTERVAL)
    last = last_polled_at if last_polled_at.tzinfo is not None else last_polled_at.replace(tzinfo=timezone.utc)
    return (now - last).total_seconds() < effective_interval



def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        poll_interval_seconds=DEVICE_CODE_INTERVAL,
        slow_down_increment_seconds=DEVICE_CODE_SLOW_DOWN_INCREMENT,
        replay_protection_supported=True,
        approval_denial_supported=True,
        spec_url=RFC8628_SPEC_URL,
    )


__all__ = [
    "STATUS",
    "RFC8628_SPEC_URL",
    "DEVICE_VERIFICATION_URI",
    "DEVICE_CODE_GRANT_TYPE",
    "DEVICE_CODE_EXPIRES_IN",
    "DEVICE_CODE_INTERVAL",
    "DEVICE_CODE_SLOW_DOWN_INCREMENT",
    "StandardOwner",
    "OWNER",
    "DeviceAuthIn",
    "DeviceAuthOut",
    "DeviceGrantForm",
    "generate_user_code",
    "validate_user_code",
    "generate_device_code",
    "next_device_poll_interval",
    "poll_too_frequently",
    "describe",
]
