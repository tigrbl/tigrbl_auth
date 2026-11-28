"""WebFinger discovery contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class WebFingerRequest:
    resource: str
    rel: str | None = "http://openid.net/specs/connect/1.0/issuer"


@dataclass(frozen=True, slots=True)
class WebFingerResult:
    subject: str
    links: tuple[Mapping[str, Any], ...]


class WebFingerResolverPort(Protocol):
    async def resolve(self, request: WebFingerRequest, /) -> WebFingerResult: ...


__all__ = ["WebFingerRequest", "WebFingerResolverPort", "WebFingerResult"]
