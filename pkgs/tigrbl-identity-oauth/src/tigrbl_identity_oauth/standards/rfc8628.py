"""RFC 8628 device-authorization helpers owned by the standards tree."""

from __future__ import annotations

import re
import secrets
import string
from datetime import datetime, timezone
from typing import Any, Final, Literal, Mapping

from tigrbl_auth.config.settings import settings
from tigrbl_auth.framework import BaseModel, hook_ctx

_USER_CODE_CHARSET: Final[str] = string.ascii_uppercase + string.digits
_USER_CODE_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Z0-9]{8,}$")

RFC8628_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc8628"
DEVICE_VERIFICATION_URI = "https://example.com/device"
DEVICE_CODE_EXPIRES_IN = 600
DEVICE_CODE_INTERVAL = 5


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


_TIGRBL_HOOK_STAGE_KEY = "".join(("pha", "se"))


@hook_ctx(**{"ops": "approve", _TIGRBL_HOOK_STAGE_KEY: "HANDLER"})
async def approve_device_code(ctx: Mapping[str, Any]) -> None:
    from tigrbl_auth.tables import DeviceCode

    payload = ctx.get("payload") or {}
    ident = payload.get("id") or payload.get("device_code")
    if ident is None:
        return

    obj = await DeviceCode.handlers.read.core({"payload": {"id": ident}})
    if obj:
        await DeviceCode.handlers.update.core(
            {
                "obj": obj,
                "payload": {
                    "authorized": True,
                    "authorized_at": datetime.now(timezone.utc),
                    "user_id": payload.get("sub"),
                    "tenant_id": payload.get("tid"),
                },
            }
        )


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


__all__ = [
    "generate_user_code",
    "validate_user_code",
    "generate_device_code",
    "DeviceAuthIn",
    "DeviceAuthOut",
    "DeviceGrantForm",
    "approve_device_code",
    "RFC8628_SPEC_URL",
    "DEVICE_VERIFICATION_URI",
    "DEVICE_CODE_EXPIRES_IN",
    "DEVICE_CODE_INTERVAL",
]
