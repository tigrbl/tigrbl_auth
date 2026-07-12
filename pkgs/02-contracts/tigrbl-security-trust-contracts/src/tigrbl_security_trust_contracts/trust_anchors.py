from dataclasses import dataclass
from typing import Protocol, Sequence


@dataclass(frozen=True, slots=True)
class TrustAnchor:
    identifier: str
    certificate_der: bytes
    profiles: Sequence[str]


class TrustAnchorProviderPort(Protocol):
    def anchors_for(self, profile: str, /) -> Sequence[TrustAnchor]: ...


__all__ = ["TrustAnchor", "TrustAnchorProviderPort"]
