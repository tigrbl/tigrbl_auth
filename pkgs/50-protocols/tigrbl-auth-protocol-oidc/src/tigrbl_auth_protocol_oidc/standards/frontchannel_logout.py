"""OpenID Connect Front-Channel Logout planning and durable completion tracking."""

from __future__ import annotations

from typing import Any, Final, Mapping
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from urllib.parse import urlencode
from uuid import UUID

from tigrbl_identity_contracts.protocol_configuration import (
    protocol_settings as settings,
)

STATUS: Final[str] = "frontchannel-logout-fanout-runtime"
_DEFAULT_MAX_RETRIES: Final[int] = 3


OWNER = StandardOwner(
    label="OIDC Front-Channel Logout",
    title="OpenID Connect Front-Channel Logout",
    runtime_status=STATUS,
    public_surface=("/logout",),
    notes=(
        "Logout fanout planning is implementation-backed. Client registration metadata can declare "
        "frontchannel_logout_uri, optional sid inclusion, bounded retry policy, and durable delivery state on logout_state metadata."
    ),
)


async def build_frontchannel_descriptor(
    *,
    client_id: UUID,
    sid: str,
    iss: str | None = None,
    logout_id: UUID | None = None,
    registration_metadata: Mapping[str, Any],
) -> dict[str, object] | None:
    metadata = dict(registration_metadata)
    logout_uri = metadata.get("frontchannel_logout_uri")
    if not logout_uri:
        return None
    include_sid = bool(metadata.get("frontchannel_logout_session_required", True))
    retry_window_s = int(metadata.get("frontchannel_retry_window_seconds", 30) or 30)
    params = {"iss": iss or settings.issuer}
    if logout_id is not None:
        params["logout_id"] = str(logout_id)
    if include_sid:
        params["sid"] = sid
    joiner = "&" if "?" in str(logout_uri) else "?"
    redirect_uri = (
        f"{logout_uri}{joiner}{urlencode(params)}" if params else str(logout_uri)
    )
    return {
        "client_id": str(client_id),
        "logout_uri": str(logout_uri),
        "redirect_uri": redirect_uri,
        "iss": params["iss"],
        "sid_included": include_sid,
        "sid": sid if include_sid else None,
        "logout_id": str(logout_id) if logout_id is not None else None,
        "delivery": {
            "channel": "frontchannel",
            "status": "pending",
            "attempts": 0,
            "max_retries": _DEFAULT_MAX_RETRIES,
            "retry_window_seconds": retry_window_s,
            "replay_protected": True,
        },
    }


def validate_frontchannel_request(
    *,
    params: dict[str, Any],
    expected_sid: str | None = None,
    expected_iss: str | None = None,
    expected_logout_id: UUID | str | None = None,
) -> dict[str, Any]:
    payload = {str(key): value for key, value in dict(params or {}).items()}
    if expected_iss is not None and str(payload.get("iss") or "") != str(expected_iss):
        raise ValueError("frontchannel issuer mismatch")
    if expected_sid is not None and str(payload.get("sid") or "") != str(expected_sid):
        raise ValueError("frontchannel sid mismatch")
    if expected_logout_id is not None and str(payload.get("logout_id") or "") != str(
        expected_logout_id
    ):
        raise ValueError("frontchannel logout_id mismatch")
    return payload


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        fanout_supported=True,
        delivery_state_persisted=True,
        retry_semantics_supported=True,
    )


__all__ = [
    "STATUS",
    "StandardOwner",
    "OWNER",
    "build_frontchannel_descriptor",
    "validate_frontchannel_request",
    "describe",
]
