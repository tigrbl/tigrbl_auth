"""OIDC front-channel and RP-initiated logout ports."""

from __future__ import annotations

from typing import Protocol

from . import LogoutRequest, LogoutRequestContext, LogoutPlan
from .session import LogoutStateRecord


class FrontChannelLogoutPort(Protocol):
    async def frontchannel_logout(self, request: LogoutRequest, /) -> LogoutPlan: ...


class RpInitiatedLogoutPort(Protocol):
    async def rp_initiated_logout(
        self,
        request: LogoutRequest,
        /,
        *,
        context: LogoutRequestContext | None = None,
    ) -> LogoutPlan: ...


__all__ = [
    "FrontChannelLogoutPort",
    "LogoutPlan",
    "LogoutRequest",
    "LogoutRequestContext",
    "LogoutStateRecord",
    "RpInitiatedLogoutPort",
]
