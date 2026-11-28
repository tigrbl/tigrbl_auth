"""OIDC UserInfo provider contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from .claims import ClaimsRequest, ClaimsResult


@dataclass(frozen=True, slots=True)
class UserInfoRequest:
    claims_request: ClaimsRequest
    access_token_claims: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class UserInfoResult:
    claims: Mapping[str, Any]


class UserInfoProviderPort(Protocol):
    async def userinfo(self, request: UserInfoRequest, /) -> UserInfoResult: ...


__all__ = [
    "ClaimsRequest",
    "ClaimsResult",
    "UserInfoProviderPort",
    "UserInfoRequest",
    "UserInfoResult",
]
