"""OIDC front-channel and RP-initiated logout ports."""

from __future__ import annotations

from typing import Protocol

from ..schemas import LogoutIn, LogoutOut, LogoutStateReadResponse
from . import LogoutRequest, LogoutRequestContext, LogoutPlan


class FrontChannelLogoutPort(Protocol):
    async def frontchannel_logout(self, request: LogoutRequest, /) -> LogoutPlan: ...


class RpInitiatedLogoutPort(Protocol):
    async def rp_initiated_logout(
        self,
        request: LogoutIn,
        /,
        *,
        context: LogoutRequestContext | None = None,
    ) -> LogoutOut: ...


__all__ = [
    "FrontChannelLogoutPort",
    "LogoutIn",
    "LogoutOut",
    "LogoutPlan",
    "LogoutRequest",
    "LogoutRequestContext",
    "LogoutStateReadResponse",
    "RpInitiatedLogoutPort",
]
