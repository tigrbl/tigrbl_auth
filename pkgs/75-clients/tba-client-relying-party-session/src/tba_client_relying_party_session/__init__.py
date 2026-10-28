from dataclasses import dataclass
from typing import Callable, Mapping

@dataclass(frozen=True)
class RelyingPartySessionClient:
    request: Callable[[str], Mapping[str, object]]
    def begin(self) -> Mapping[str, object]:
        return self.request("/v1/rp/login")
    def session(self) -> Mapping[str, object]:
        return self.request("/v1/rp/session")

__all__ = ["RelyingPartySessionClient"]
