"""RFC 8935 push and RFC 8936 poll delivery contracts for RFC 8417 SETs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SetPushRequest:
    set_token: str

    def form(self) -> Mapping[str, str]:
        if self.set_token.count(".") != 2:
            raise ValueError("SET push payload must be a compact JWT")
        return {"SET": self.set_token}


@dataclass(frozen=True, slots=True)
class SetPollRequest:
    max_events: int | None = None
    return_immediately: bool | None = None
    acks: tuple[str, ...] = ()
    set_errs: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if self.max_events is not None and self.max_events <= 0:
            raise ValueError("max_events must be positive")


__all__ = ["SetPollRequest", "SetPushRequest"]
