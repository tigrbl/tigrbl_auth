"""OAuth token-exchange flow contracts."""

from __future__ import annotations

from typing import Any, Mapping, Protocol


class TokenExchangeServicePort(Protocol):
    async def exchange(
        self,
        request: Mapping[str, Any],
        /,
        *,
        headers: Mapping[str, str] | None = None,
    ) -> Mapping[str, Any]: ...


__all__ = ["TokenExchangeServicePort"]
